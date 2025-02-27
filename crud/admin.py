from django.contrib import admin
from crud.models import noticia, Artigo, Tag, Colecao

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'previo', 'conteudo')
    search_fields = ('titulo', 'conteudo', 'previo')
    
class ArtAdmin(admin.ModelAdmin):
    list_display =('titulo','previo', 'conteudo')
    search_fields =('titulo', 'previo', 'conteudo')
    list_filter=('data_criacao',)
    filter_horizontal=('tags',)
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Admin para Coleções
@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('tags', 'artigos')  # Permitir selecionar múltiplas tags e artigos
    list_filter = ('tags',)  # Filtro baseado nas tags associadas

admin.site.register(noticia, NewsAdmin)

admin.site.register(Artigo, ArtAdmin)