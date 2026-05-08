"""
URLs para la app lexer
"""
from django.urls import path
from . import views

app_name = 'lexer'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_lexer, name='analyze'),
    path('arbol/', views.arbol_view, name='arbol'),
]
