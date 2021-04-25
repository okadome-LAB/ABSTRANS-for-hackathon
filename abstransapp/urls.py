from django.urls import path
from .views import home, abstrans, search, exec_ajax
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', home, name='index'),
    path('search/', search, name='search'),
    path('abstrans/<path:doi>', cache_page(60 * 15)(abstrans), name='abstrans'),
    # Ajax処理
    path("exec/", exec_ajax, name='exec'),
]
