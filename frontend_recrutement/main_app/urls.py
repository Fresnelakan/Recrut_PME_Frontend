from django.urls import path
from . import views 


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view_candidat, name='profile'),
    path('creer/', views.creer_offre_emploi, name='creer_offre_emploi'),
    path('offres-emploi/', views.offres_emploi, name='offres_emploi'),
    path('liste/', views.liste_offres_emploi, name='liste_offres_emploi'),
    path('pme/mes-offres/', views.liste_offres_pme_avec_candidatures, name='liste_offres_pme_candidatures'),
    path('pme/offres/<int:offre_id>/candidatures/', views.liste_candidatures_offre, name='liste_candidatures_offre'),
    
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
    
    path('offre-detail/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    path('pme/offres/<int:offre_id>/scoring/', views.scoring_resultat, name='scoring_resultat'),
]