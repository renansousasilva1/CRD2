
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import noticia, Artigo, Tag
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crud.forms import NoticiaModelForm, ArtigoModelForm, noticia
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy
from bs4 import BeautifulSoup
import requests
import logging
from django.core.files.storage import default_storage
import os
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Artigo
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from .models import noticia, Artigo
import time
# Configure logging para exibir mensagens no console
logger = logging.getLogger(__name__)

def obter_previsao():
    url_temp = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj'
    url_sense = 'https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj'

    soup_temp = BeautifulSoup(requests.get(url_temp).text, 'html.parser')
    soup_sense = BeautifulSoup(requests.get(url_sense).text, 'html.parser')

    temp_min = soup_temp.find(id='min-temp-1').text.strip() if soup_temp.find(id='min-temp-1') else "N/A"
    temp_max = soup_temp.find(id='max-temp-1').text.strip() if soup_temp.find(id='max-temp-1') else "N/A"
    sensacao_termica = soup_sense.find(class_="no-gutters -gray _flex _justify-center _margin-t-20 _padding-b-20 _border-b-light-1").text.strip()

    return {
        "temp_min": temp_min,
        "temp_max": temp_max,
        "sensacao": sensacao_termica
    }

def previsao_tempo(request):
    dados = obter_previsao()
    return render(request, 'html/previsao.html', {'dados': dados})


def noticia_detail(request, id):
    noticia_selecionada = get_object_or_404(noticia, id=id)
    
    return render(request, 'html/noticia_detail.html', {
        'noticia': noticia_selecionada
    })

def artigo_detail(request, id):
    artigo_selecionado = get_object_or_404(Artigo, id=id)
    
    return render(request, 'html/artigo_detail.html', {
        'artigo': artigo_selecionado
    })


class ArtigoDetail(DetailView):
    model = Artigo
    template_name = 'html/artigo_detail.html'
    context_object_name = "artigos_detail"

    def get_object(self, queryset=None):
        """Retorna o artigo que será exibido. Se não encontrado, retorna um 404."""
        obj = get_object_or_404(Artigo, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        """Adiciona contexto adicional ao template."""
        context = super().get_context_data(**kwargs)
        # Adiciona artigos relacionados (excluindo o atual)
        context['related_articles'] = Artigo.objects.exclude(id=self.object.id)[:5]
        return context
    

class NoticiaView(ListView):
    model = noticia
    template_name = 'html/noticias.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_criacao')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(previo__icontains=search) |
                Q(conteudo__icontains=search) |
                Q(data_criacao__icontains=search)
            ).distinct()
        return queryset

def maisforte(request):
    return render(request, 'html/maisforte.html')
    
def zo(request):
    return render(request, 'html/zo.html')

def zc(request):
    return render(request, 'html/zc.html')

def zn(request):
    return render(request, 'html/zn.html')

def zs(request):
    return render(request, 'html/zs.html')


def mapa2(request):
    return render(request, 'html/mapa2.html')

def home(request):
    tags = Tag.objects.all()
    artigos = Artigo.objects.all().order_by('-data_criacao') [:3]
    noticias = noticia.objects.all().order_by('-data_criacao') [:5]  # Buscar todas as notícias no banco de dados
    noticias_outros = noticia.objects.all().order_by('-data_criacao')[5:]
    
    
    return render(request, 'html/home.html',{
        'noticias': noticias, 'noticias_outros': noticias_outros, 
        'artigos': artigos, 'tags': tags})

def ferramentas(request):
    return render(request, 'html/ferramentas.html')



class ArtigoView(ListView):
    model = Artigo
    template_name = 'html/artigos.html'
    context_object_name = 'artigos'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_criacao')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
            Q(titulo__icontains=search) |
            Q(previo__icontains=search) |
            Q(conteudo__icontains=search) |
            Q(data_criacao__icontains=search)
        ).distinct()
        
        return queryset

    
class News(CreateView):
    model = noticia
    form_class = NoticiaModelForm
    template_name = 'html/swen.html'
    success_url = reverse_lazy('news')
    

class NewArtigo(CreateView):
    model= Artigo
    form_class = ArtigoModelForm
    template_name = 'html/swen2.html'
    success_url = reverse_lazy('tra')



    

def artigos_por_tag(request, tag_nome):
    tag_nome = tag_nome.replace("_", " ").replace("-", " ") # Buscar a tag com o nome ajustado
    tag = get_object_or_404(Tag, Q(nome__iexact=tag_nome))  # Busca insensível a maiúsculas/minúsculas

    # Filtrar artigos associados a essa tag
    artigos = Artigo.objects.filter(tags=tag)

    return render(request, 'html/artigos_por_tag.html', {
        'tag': tag,
        'artigos': artigos,
    })


class BuscaGeralView(TemplateView):
    template_name = 'html/busca_geral.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        
        # Inicializar resultados vazios
        artigos = Artigo.objects.none()
        noticias = noticia.objects.none()
        tags = Tag.objects.none()

        if search:
            # Filtrar artigos, notícias e tags
            artigos = Artigo.objects.filter(
                Q(titulo__icontains=search) |
                Q(previo__icontains=search) |
                Q(conteudo__icontains=search)
            ).order_by('-data_criacao').distinct()

            noticias = noticia.objects.filter(
                Q(titulo__icontains=search) |
                Q(previo__icontains=search) |
                Q(conteudo__icontains=search)
            ).order_by('-data_criacao').distinct()

            tags = Tag.objects.filter(nome__icontains=search).distinct()

        # Paginar os resultados
        artigos_page = self.paginate_queryset(artigos, 9, 'artigos_page')
        noticias_page = self.paginate_queryset(noticias, 9, 'noticias_page')

        # Adicionar dados ao contexto
        context['artigos'] = artigos_page
        context['noticias'] = noticias_page
        context['tags'] = tags
        context['search'] = search
        return context

    def paginate_queryset(self, queryset, per_page, page_param):
        paginator = Paginator(queryset, per_page)
        page_number = self.request.GET.get(page_param, 1)
        return paginator.get_page(page_number)

    