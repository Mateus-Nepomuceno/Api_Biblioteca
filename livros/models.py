from django.db import models
from datetime import date
from django.conf import settings
from django.core.validators import MaxValueValidator

def ano_atual():
    return date.today().year

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    #retirei o campo idade
    
    def __str__(self):
        return self.nome
    
class Livro (models.Model):
    #atualização para "ManyToManyField" - permitir mais de um autor
    autores = models.ManyToManyField(Autor, related_name="livros", blank=True)
    titulo = models.CharField(max_length=200)
    resumo = models.TextField()
    ano_pub = models.IntegerField(validators=[MaxValueValidator(ano_atual())])
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo