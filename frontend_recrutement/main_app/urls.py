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
    # path('profil/modifier/', views.profile_view_candidat, name='mise_a_jour_profil'),
    path('profil/cv',views.upload_cv_view,name='mise_a_jour_cv'),
    path('profil/', views.creer_profil_entreprise, name='profil'),
    path('/', views.creer_profil_entreprise, name='profil'),
    path('modifier-offre/<int:offre_id>/', views.modifier_offre, name='modifier_offre'),
    path('modification', views.liste_offres, name='modification'),
    path('offres-emploi-can/', views.offres_emploi_can, name='offres_emploi_can'),
    path('offre-candidat/<int:offre_id>/', views.offre_detail_candidat, name='offre_detail_candidat'),
    path('postuler-offre/<int:offre_id>/', views.postuler_offre, name='postuler_offre'),
    path('offres/supprimer/<int:offre_id>/', views.supprimer_offre, name='supprimer_offre'),
    path('candidatures/', views.liste_candidatures_candidat, name='liste_candidatures_candidat'),
    
    path('telecharger-offre/<int:offre_id>/', views.telecharger_offre, name='telecharger_offre'),
    path('offre-detail/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    # path("profile-candidat/", views.profile_view_candidat, name="profile-candidat"),
    #a supprimer maybe
    # path('profil/candidat/', views.profile_candidat_view, name='profil_candidat'),
    # path('profil/candidat/update/', views.update_profil_candidat, name='update_profil_candidat'),
    # path('profil/candidat/upload-cv/', views.upload_cv_candidat, name='upload_cv_candidat'),
]