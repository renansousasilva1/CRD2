from django.urls import path, include
from .views import NoticiaView, home, ArtigoView, ferramentas, noticia_detail, ArtigoDetail, News, NewArtigo, artigos_por_tag, BuscaGeralView, maisforte, previsao_tempo, mapa2,zo,zc,zs,zn
from django.views.generic import TemplateView 
from accounts.views import register_view, login_view, logout_view

urlpatterns = [
    path('', include('accounts.urls')),
    path('register/', register_view, name="register/"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('especial/1', maisforte, name='maisforte'),
    path('mapa2', mapa2, name='mapa2'),
    path('zo', zo, name='zo'),
    path('zc', zc, name='zc'),
    path('zs', zs, name='zs'),
    path('zn', zn, name='zn'),
    path('', home, name='home'),
    path('previsao/', previsao_tempo, name='previsao_tempo'),
    path('noticias/', NoticiaView.as_view(), name='noticias'), 
    path('noticias/<int:id>/', noticia_detail, name='noticia_detail'), 
    path('artigos/', ArtigoView.as_view(), name='artigos'),  
    path('artigos/tag/<str:tag_nome>/', artigos_por_tag, name='artigos_por_tag'), 
    path('artigos/<int:pk>/', ArtigoDetail.as_view(), name='artigo_detail'), 
    path('swen', News.as_view(), name='news'),
    path('swen2/', NewArtigo.as_view(), name='tra'),
    path('buscar/', BuscaGeralView.as_view(), name='busca_geral'),
    path('ferramentas/', ferramentas, name='ferramentas'),
        
] 