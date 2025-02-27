from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

   

# Create your models here.
class noticia(models.Model):
    titulo = models.CharField(max_length=200)
    previo = models.CharField(max_length=70)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='crud/', blank = True, null = True)
    
    def __str__(self):
        return self.titulo

class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    previo = models.CharField(max_length=70)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='crud/', blank = True, null = True)
    tags = models.ManyToManyField('Tag', related_name='artigos', blank=True)
    
    def __str__(self):
        return self.titulo

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=120, blank = False, null =False)

    def __str__(self):
        return self.nome


class Colecao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='colecoes', blank=True)
    artigos = models.ManyToManyField(Artigo, related_name='colecoes', blank=True)

    def __str__(self):
        return self.nome

    def adicionar_artigo(self, artigo):
        # Adiciona um artigo à coleção se ele tiver tags correspondentes
        if any(tag in self.tags.all() for tag in artigo.tags.all()):
            self.artigos.add(artigo)