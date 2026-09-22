from django.db import models


class Marca(models.Model):
    nome = models.CharField(max_length=100)
    pais_origem = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Carro(models.Model):
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name="carros"
    )

    def __str__(self):
        return self.modelo
    
# novas classes, não retiradas para não dar erro
class Especie(models.Model):
    DIETA_CHOICES = [
        ('C', 'Carnívoro'),
        ('H', 'Herbívoro'),
        ('O', 'Onívoro'),
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    dieta = models.CharField(max_length=1, choices=DIETA_CHOICES)
    nivel_periculosidade = models.IntegerField(help_text="Escala de 1 a 10")

    def __str__(self):
        return self.nome

class Cercado(models.Model):
    nome = models.CharField(max_length=100)
    voltagem_cerca = models.IntegerField(help_text="Voltagem atual em kV")
    dimensao = models.CharField(max_length=100, help_text="Dimensões do cercado (ex: 20x30m)")

    def __str__(self):
        return f"{self.nome} (Energia: {'ON' if self.energia_ativa else 'OFF'})"

class Dinossauro(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.CharField(max_length=100)
    
    # Chaves Estrangeiras (1:N)
    especie = models.ForeignKey(
        Especie, 
        on_delete=models.CASCADE, 
        related_name='dinossauros'
    )
    cercado = models.ForeignKey(
        Cercado, 
        on_delete=models.CASCADE,
        related_name='dinossauros'
    )

    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    
    # Chave Muitos-para-Muitos (N:N)
    funcionario_responsavel = models.ForeignKey(
            Cercado, 
            on_delete=models.CASCADE, 
            related_name='cercados'
    )

    def __str__(self):
        return f"{self.nome} - {self.cargo}"