# Documentação do Sistema — Jurassic Park API

Este documento explica o domínio da aplicação, as entidades, os relacionamentos e — principalmente — as **regras de negócio** implementadas. Para instruções de instalação e stack técnica, veja o [readme.md](readme.md).

## Visão geral

A API modela a operação de um parque de dinossauros: espécies e seus indivíduos, os cercados onde vivem, os funcionários responsáveis por cercados e veículos, e os veículos do parque (patrulha ou turismo).

O código segue uma arquitetura em camadas (detalhada no [readme.md](readme.md)):

```
Request → views.py (ViewSet) → service.py (regra de negócio) → models.py (banco)
                ↓
        serializers.py (validação de formato / (des)serialização)
                ↑
        filters.py (busca via querystring)
```

Toda regra de negócio (validações que dependem de outros registros no banco, não só do formato do dado) fica em `service.py`. Os `ViewSets` nunca falam com o ORM diretamente para criar/atualizar — sempre delegam ao Service correspondente.

## Entidades e relacionamentos

### `Funcionario`

| Campo | Tipo | Observação |
|---|---|---|
| `nome` | texto | |
| `data_nascimento` | data | |
| `cargo` | texto | ex: "Diretor", "Engenheiro", "Adestrador" |

Um funcionário pode ser responsável por vários `Cercado`s e vários `Carro`s (relação 1:N em ambos os casos).

### `Especie`

| Campo | Tipo | Observação |
|---|---|---|
| `nome` | texto único | ex: "Tyrannosaurus Rex" |
| `dieta` | escolha | `C` Carnívoro, `H` Herbívoro, `O` Onívoro |
| `nivel_periculosidade` | inteiro | escala de 1 a 10 |

### `Cercado`

| Campo | Tipo | Observação |
|---|---|---|
| `nome` | texto | ex: "Setor 4" |
| `voltagem_cerca` | inteiro | em kV |
| `dimensao_m2` | decimal | área do cercado |
| `funcionario` | FK → Funcionario | responsável pelo cercado |

### `Dinossauro`

| Campo | Tipo | Observação |
|---|---|---|
| `nome` | texto | |
| `data_nascimento` | texto | |
| `especie` | FK → Especie | |
| `cercado` | FK → Cercado | onde o dinossauro vive |

### `Carro`

Representa um veículo do parque (não um carro genérico de concessionária — não tem `ano`/`preço`/`marca`, pois isso não fazia sentido no domínio).

| Campo | Tipo | Observação |
|---|---|---|
| `modelo` | texto | ex: "Ford Explorer" |
| `tipo` | escolha | `G` Guarda (patrulha), `T` Turismo |
| `funcionario` | FK → Funcionario | quem dirige/é responsável pelo veículo |

## Regra de negócio: compatibilidade de dieta no cercado

A regra é aplicada tanto na **criação** (`POST`) quanto na **edição** (`PUT`/`PATCH`) — uma regra que só valesse na criação poderia ser burlada editando o registro depois, então ela foi replicada nos dois fluxos.

**Regra:** um dinossauro Carnívoro não pode dividir cercado com um dinossauro Herbívoro ou Onívoro (e vice-versa). Dois Carnívoros — mesmo de espécies diferentes — podem conviver.

**Onde:** `DinossauroService.validar_dieta_compativel(especie, cercado, ignorar_dinossauro_id=None)`.

**Como a verificação funciona, passo a passo:**

1. Busca no banco **todos os dinossauros que já estão no cercado de destino**:
   ```python
   dinos_no_cercado = Dinossauro.objects.filter(cercado=cercado).select_related('especie')
   ```
   O `select_related('especie')` traz a espécie de cada dinossauro na mesma query (evita disparar uma query extra por dinossauro só pra ler a dieta dele).

2. **Se for uma atualização** (edição de um dinossauro que já está no cercado), o próprio dinossauro é removido dessa lista antes de comparar:
   ```python
   if ignorar_dinossauro_id is not None:
       dinos_no_cercado = dinos_no_cercado.exclude(id=ignorar_dinossauro_id)
   ```
   Sem isso, ao editar um dinossauro que já está no cercado, ele apareceria na lista e seria comparado *contra si mesmo* — como a dieta dele é igual à dele mesmo, nunca daria conflito, mas é um caso de borda que vale eliminar explicitamente. Na criação (`ignorar_dinossauro_id=None`), esse passo é pulado, porque o dinossauro novo ainda não está na lista.

3. Para **cada** dinossauro que sobrou na lista, a dieta de cada lado é reduzida a uma pergunta binária — "é carnívoro ou não?" — porque a regra só se importa com essa fronteira (Herbívoro e Onívoro são tratados como "o mesmo lado"):
   ```python
   eh_carnivoro_novo = especie.dieta == 'C'
   eh_carnivoro_existente = dieta_existente == 'C'
   ```

4. Se os dois booleanos forem **diferentes** (um é carnívoro e o outro não), é um conflito — a função levanta `ValueError` imediatamente, com o nome do dinossauro que já está lá e as duas dietas envolvidas, e **para de checar** os demais (não precisa continuar, um conflito já é suficiente pra barrar a operação).

5. Se o laço terminar sem achar nenhum conflito, a função simplesmente retorna (não faz nada) — e quem chamou ela sabe que pode prosseguir com a criação/atualização.

**Quem chama essa validação, e quando:**
- `DinossauroService.criar()` chama **antes** de criar o registro no banco.
- `DinossauroService.atualizar()` chama **antes** de salvar, passando `ignorar_dinossauro_id=instance.id`.
- Em ambos os casos, é a `ViewSet` (`DinossauroViewSet.perform_create`/`perform_update`) quem captura o `ValueError` e o transforma num erro HTTP 400 — o Service em si não sabe nada sobre HTTP, só sobre a regra.

**Efeito colateral coberto — mudar a dieta da Espécie, não do dinossauro:**

Existe um segundo jeito de violar essa mesma regra: em vez de mover um dinossauro pra um cercado incompatível, você poderia mudar a **dieta da Espécie inteira** (ex: `PATCH /api/especies/3/` mudando `dieta` de Carnívoro pra Herbívoro) — e de repente todos os dinossauros daquela espécie, em todos os cercados onde estão, passam a ter uma dieta diferente da que tinham quando foram colocados lá. `EspecieService.validar_mudanca_dieta(instance, nova_dieta)` cobre esse caso:

1. Se a dieta nova for igual à atual, não há nada pra revalidar — retorna na hora.
2. Busca **todos os cercados que têm pelo menos um dinossauro dessa espécie**, atravessando o relacionamento reverso Dinossauro → Cercado:
   ```python
   cercados_com_essa_especie = Cercado.objects.filter(dinossauros__especie=instance).distinct()
   ```
3. Para cada um desses cercados, busca os **outros** dinossauros do cercado (excluindo os da própria espécie, já que todos eles vão mudar de dieta junto — não faz sentido compará-los entre si):
   ```python
   outros_dinos = Dinossauro.objects.filter(cercado=cercado).exclude(especie=instance).select_related('especie')
   ```
4. Roda a mesma comparação booleana carnívoro/não-carnívoro do passo 3 acima, contra a **dieta nova** (a que está tentando ser salva) — se achar conflito em qualquer cercado, levanta `ValueError` e bloqueia a mudança de dieta.

**Exemplo de erro (dinossauro indo pro cercado errado):**
```json
["Não é possível colocar um dinossauro de dieta 'Herbívoro' no cercado 'Setor 4', pois já existe lá o dinossauro 'Rexy', de dieta 'Carnívoro'."]
```

**Exemplo de erro (tentando mudar a dieta da espécie):**
```json
["Não é possível mudar a dieta de 'Velociraptor' para 'Herbívoro', pois no cercado 'Setor Teste' já existe o dinossauro 'Rexinho', de dieta incompatível ('Carnívoro')."]
```

### Como o `PATCH` (atualização parcial) consegue revalidar sem quebrar

Um detalhe que faz a regra funcionar também em atualizações **parciais** (`PATCH`, onde o cliente manda só os campos que quer mudar): antes de chamar o Service, a `ViewSet` monta o conjunto completo de valores — o que veio na requisição, ou o valor atual da instância se aquele campo não foi enviado:

```python
def perform_update(self, serializer):
    instance = serializer.instance
    dados = serializer.validated_data

    dieta = dados.get('dieta', instance.dieta)              # veio na requisição? usa. Não veio? usa o valor atual.
    nivel_periculosidade = dados.get('nivel_periculosidade', instance.nivel_periculosidade)
    ...
    EspecieService.atualizar(instance, nome, dieta, nivel_periculosidade)
```

Assim, um `PATCH { "dieta": "H" }` roda a validação sobre a dieta nova **combinada** com o `nome`/`nivel_periculosidade` que já estavam salvos — nunca sobre um objeto "incompleto".

### Por que a regra fica no Service, não no Serializer

O `Serializer` valida **formato** (campo obrigatório, tipo certo, choices válidas). Essa regra depende de **consultar outros registros no banco** (os outros dinossauros do cercado) — isso é lógica de negócio, então mora no `Service`. Quando uma regra é violada, o Service levanta um `ValueError` simples (sem depender do Django REST Framework), e a `ViewSet` é quem traduz isso para um erro HTTP `400` apropriado:

```python
try:
    serializer.instance = DinossauroService.criar(**serializer.validated_data)
except ValueError as e:
    raise ValidationError(str(e))
```

## Endpoints da API

Todos em `/api/`, seguindo o padrão REST do DRF (`ModelViewSet` via `DefaultRouter`):

| Recurso | Rota | Filtros disponíveis |
|---|---|---|
| Carros | `/api/carros/` | `?tipo=`, `?funcionario=`, `?modelo=` (parcial) |
| Funcionários | `/api/funcionarios/` | — |
| Espécies | `/api/especies/` | `?dieta=`, `?nome=` (parcial), `?periculosidade_min=`, `?periculosidade_max=` |
| Cercados | `/api/cercados/` | `?funcionario=` |
| Dinossauros | `/api/dinossauros/` | `?nome=` (parcial), `?especie=`, `?cercado=` |

Todos suportam `GET` (lista e detalhe), `POST`, `PUT`, `PATCH` e `DELETE`. A API navegável do DRF (abrir qualquer rota acima direto no navegador) já vem habilitada por padrão, sem configuração extra.
