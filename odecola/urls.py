from django.urls import path
from . import views
from django.views import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('actualites/', views.blog, name='blog'),
    path('article/<str:article_slug>/', views.detail_article, name="detail_article"),
    path('connexion/', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('inscription/', views.inscription, name="inscription"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)