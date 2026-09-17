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