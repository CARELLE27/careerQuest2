from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register, name='register'),

    # Profil
    path('profil/', views.profil, name='profil'),

    # Compétences
    path('competences/', views.liste_competences, name='competences'),
    path('competences/mes/', views.mes_competences, name='mes_competences'),

    # Quêtes
    path('quetes/', views.mes_quetes, name='quetes'),
    path('quetes/<int:quete_id>/done/', views.completer_quete, name='completer_quete'),

    # Classement
    path('classement/', views.classement, name='classement'),

    # GitHub
    path('github/<str:username>/', views.github_repos, name='github'),
]
