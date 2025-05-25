from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view_candidat, name='profile'),
    path('creer/', views.creer_offre_emploi, name='creer_offre_emploi'),
    path('offres-emploi/', views.offres_emploi, name='offres_emploi'),
    path('liste/', views.liste_offres_emploi, name='liste_offres_emploi'),
    path('profil/modifier/', views.profile_view_candidat, name='mise_a_jour_profil'),
    path('profil/cv',views.upload_cv_view,name='mise_a_jour_cv'),
    path('profil/', views.creer_profil_entreprise, name='profil'),
    # path("profile-candidat/", views.profile_view_candidat, name="profile-candidat"),
   
]