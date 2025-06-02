from django.shortcuts import redirect, render
from django.http import JsonResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import requests
def index(request):
    return render(request, 'index.html')




from django.contrib import messages

API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"  # remplace cette URL par l’URL réelle de ton API


import requests
from django.shortcuts import render
from django.conf import settings # Importer settings

def offres_emploi(request):
    offres = []
    error_message = None # Initialiser une variable pour le message d'erreur

    try:
        # Utiliser un paramètre de configuration (setting) pour l'URL du backend
        backend_url = f"http://127.0.0.1:8001/api/candidat/offres_emploi/"
        response = requests.get(backend_url) 

        # Vérifier si la requête a réussi (code de statut 2xx)
        response.raise_for_status()

        offres = response.json()

    except requests.exceptions.RequestException as e:
        # Gérer les exceptions spécifiques aux requêtes
        error_message = f"Erreur lors de la récupération des offres d'emploi : {e}"
        # Loguer l'erreur pour le débogage
        print(f"Erreur lors de la récupération des offres d'emploi depuis le backend : {e}")
    except ValueError:
        # Gérer les erreurs potentielles de décodage JSON
        error_message = "Erreur lors du décodage des données des offres d'emploi."
        print(f"Erreur lors du décodage JSON depuis le backend : {response.text}")
    except Exception as e:
        # Attraper toute autre exception inattendue
        error_message = f"Une erreur inattendue s'est produite : {e}"
        print(f"Une erreur inattendue s'est produite : {e}")


    # Passer les données récupérées et le message d'erreur potentiel au template
    context = {
        'offres': offres,
        'error_message': error_message,
    }

    return render(request, 'offres_emploi/offres_emploi.html', context)




import requests
from django.shortcuts import render

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

import requests
from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator

def modifier_offre(request, offre_id):
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour modifier une offre.")
        return redirect("login_page")

    api_url = f"http://127.0.0.1:8001/api/pme/offres/{offre_id}/"
    offre = {}
    error_message = None
    success_message = None

    # Récupérer les données de l’offre existante
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        offre = response.json()
        
    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer les détails de l’offre : {e}"
        print(f"Erreur lors de l'appel API pour modifier : {e}")

    # Gérer la soumission du formulaire
    if request.method == "POST":
        offer_data = {
            'titre': request.POST.get('titre', ''),
            'description': request.POST.get('description', ''),
            'lieu': request.POST.get('lieu', ''),
            'type_contrat': request.POST.get('type_contrat', ''),
        }

        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.put(api_url, json=offer_data, headers=headers)  # Utilisez PUT ou PATCH selon votre API
            response.raise_for_status()
            success_message = "Offre modifiée avec succès !"
            return redirect('liste_offres_emploi')
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur lors de la modification de l’offre : {e}"
            print(f"Erreur lors de l'appel API pour sauvegarder : {e}")

    context = {
        'offre': offre,
        'error_message': error_message,
        'success_message': success_message,
        'titre_page': f"Modifier l'offre - {offre.get('titre', 'Inconnue')}"
    }

    return render(request, 'offres_emploi/modifier_offre.html', context)

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

def offre_detail(request, offre_id):
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour voir les détails.")
        return redirect("login_page")

    api_url = f"http://127.0.0.1:8001/api/pme/offres/{offre_id}/"  # Endpoint pour une offre spécifique
    offre = {}
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        offre = response.json()
        # if 'date_publication' in offre:
        #     date_obj = datetime.strptime(offre['date_publication'], '%Y-%m-%dT%H:%M:%SZ')
        #      offre['date_publication'] = date_obj.strftime('%d/%m/%Y %H:%M')

    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer les détails de l’offre : {e}"
        print(f"Erreur lors de l'appel API pour les détails : {e}")

    context = {
        'offre': offre,
        'error_message': error_message,
        'titre_page': f"Détails de l'offre - {offre.get('titre', 'Inconnue')}"
    }

    return render(request, 'offres_emploi/offre_detail.html', context)


def liste_offres_emploi(request):
    print("Contenu de la session :", request.session.items())  # Débogage
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour voir les offres.")
        return redirect("login_page")  # Utilisez 'login_page' comme dans creer_offre_emploi

    api_url = "http://127.0.0.1:8001/api/pme/offres/"
    offres = []
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print("Données de l'API :", data)  # Débogage
        if isinstance(data, dict) and 'results' in data:
            offres = data.get('results', [])
        else:
            offres = data

    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer les offres depuis le backend : {e}"
        print(f"Erreur lors de l'appel API pour la liste des offres : {e}")

    context = {
        'offres': offres,
        'error_message': error_message,
        'titre_page': "Liste des Offres d'Emploi",
    }

    return render(request, 'offres_emploi/liste_offres_emploi.html', context)
def liste_offres(request):
    print("Contenu de la session :", request.session.items())  # Débogage
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour voir les offres.")
        return redirect("login_page")  # Utilisez 'login_page' comme dans creer_offre_emploi

    api_url = "http://127.0.0.1:8001/api/pme/offres/"
    offres = []
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print("Données de l'API :", data)  # Débogage
        if isinstance(data, dict) and 'results' in data:
            offres = data.get('results', [])
        else:
            offres = data

    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer les offres depuis le backend : {e}"
        print(f"Erreur lors de l'appel API pour la liste des offres : {e}")

    context = {
        'offres': offres,
        'error_message': error_message,
        'titre_page': "Liste des Offres d'Emploi",
    }

    return render(request, 'offres_emploi/modification.html', context)
# votre_app/views.py



def creer_profil_entreprise(request):
    access_token = request.session.get("accessToken")
    
    # Initialize values for pre-filling the form in case of error or success
    nom_initial = ''
    description_initial = ''

    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        logo = request.FILES.get('logo') # Get the logo file

        # --- Data Validation ---
        if not nom:
            messages.error(request, "Le nom de l'entreprise est obligatoire.")
            nom_initial = nom
            description_initial = description
            return render(request, 'dashboardPME_templates/profile.html', {
                'nom': nom_initial,
                'description': description_initial
            })
        
        if not description:
            messages.error(request, "La description de l'entreprise est obligatoire.")
            nom_initial = nom
            description_initial = description
            return render(request, 'dashboardPME_templates/profile.html', {
                'nom': nom_initial,
                'description': description_initial
            })
            
        data = {
            "nom_entreprise" : nom,
            "description" : description,
        }

        # For file uploads with `requests`, you should use the `files` parameter, not `data`
        files = {}
        if logo:
            files['logo'] = logo

        api_url = "http://127.0.0.1:8001/api/pme/profil/entreprise/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            # --- Saving to the database ---
            # Use `files=files` for file uploads, and `data=data` for other form fields
            response = requests.post(api_url, headers=headers, data=data, files=files)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            messages.success(request, "Profil d'entreprise créé avec succès!")
            # Pre-fill the form with the successfully saved data
            nom_initial = nom
            description_initial = description
            
            return render(request, 'dashboardPME_templates/profile.html', {
                'nom': nom_initial,
                'description': description_initial
            })

        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                messages.error(request, "Cette PME a déjà créé un profil d'entreprise.")
            else:
                messages.error(request, f"Une erreur est survenue lors de l'enregistrement du profil : {e}")
            
            # Pre-fill the form in case of any error
            nom_initial = nom
            description_initial = description
            return render(request, 'dashboardPME_templates/profile.html', {
                'nom': nom_initial,
                'description': description_initial
            })
        except Exception as e:
            messages.error(request, f"Une erreur inattendue est survenue : {e}")
            nom_initial = nom
            description_initial = description
            return render(request, 'dashboardPME_templates/profile.html', {
                'nom': nom_initial,
                'description': description_initial
            })

    # If the request is GET (or any other non-POST method), display the empty form
    return render(request, 'dashboardPME_templates/profile.html')

def creer_offre_emploi(request):
    access_token = request.session.get("accessToken")

    if not access_token:
        return redirect('login_page')

    context = {
        'titre_page': "Créer une Offre d'Emploi",
        'error_message': None,
        'success_message': None,
    }

    if request.method == "POST":
        # --- Récupération des données du formulaire POST ---
        # print("Données POST reçues:", request.POST) # Utile pour le débogage

        offer_data = {
            'titre': request.POST.get('titre', ''),  # <-- C'est maintenant 'titre'
            'description': request.POST.get('description', ''),
            # 'location': request.POST.get('location', ''), # Si vous avez ces champs dans votre modèle et API
            # 'salary': request.POST.get('salary', None), # Si vous avez ces champs dans votre modèle et API
            # 'contract_type': request.POST.get('contract_type', ''), # Si vous avez ces champs dans votre modèle et API
            # 'experience_level': request.POST.get('experience_level', ''), # Si vous avez ces champs dans votre modèle et API
            # 'application_url': request.POST.get('application_url', ''), # Si vous avez ces champs dans votre modèle et API
        }

        # Conversion du salaire si nécessaire (si votre API l'attend comme un nombre)
        # if offer_data['salary']:
        #     try:
        #         offer_data['salary'] = float(offer_data['salary']) # Ou int() si c'est un entier
        #     except ValueError:
        #         context['error_message'] = "Le salaire doit être un nombre valide."
        #         return render(request, 'offres_emploi/offres_emploi.html', context)
        # else:
        #     del offer_data['salary'] # Supprimer si c'est None et que l'API n'attend pas de valeur nulle

        

       
        api_url = f"http://127.0.0.1:8001/api/pme/offres/" # Confirmez l'URL exacte de votre endpoint de création d'offres

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
            
        try:
            response = requests.post(api_url, json=offer_data, headers=headers)

            if response.status_code == 201: # 201 Created pour un succès
                context['success_message'] = "Votre offre a été créée avec succès !"
                
            else:
                error_details = response.json() 
                if response.status_code == 400: # Bad Request (erreurs de validation DRF)
                    message = "Erreur(s) de validation :<br>"
                    # Parcourt les erreurs renvoyées par le serializer DRF
                    for field, errors in error_details.items():
                        # Si l'erreur est sur le champ 'entreprise' (par ex. si l'ID n'est pas valide ou absent)
                        if field == 'entreprise':
                            message += f"<strong>Entreprise :</strong> {' '.join(errors)}<br>"
                        else:
                            # Assurez-vous que le nom du champ ici correspond à ce que l'API renvoie
                            message += f"<strong>{field} :</strong> {' '.join(errors)}<br>"
                    context['error_message'] = message
                elif response.status_code == 401: # Unauthorized
                    context['error_message'] = "Vous n'êtes pas authentifié. Veuillez vous reconnecter."
                    return redirect('login') # Redirection forte en cas d'authentification invalide
                elif response.status_code == 403: # Forbidden
                    context['error_message'] = "Vous n'êtes pas autorisé à créer cette offre. Vérifiez vos permissions."
                else:
                    context['error_message'] = f"Une erreur est survenue côté serveur: {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as e:
            context['error_message'] = f"Impossible de se connecter au serveur API : {e}"

    return render(request, 'offres_emploi/offres_emploi.html', context)


def candidat_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        description = request.POST.get('description')
        telephone = request.POST.get('telephone')
        pays = request.POST.get('pays')
        langue = request.POST.get('langue')
        fichier_cv = request.FILES.get('cv')

        data = {
            'nom': nom,
            'email': email,
            'adresse': adresse,
            'description': description,
            'telephone': telephone,
            'pays': pays,
            'langue': langue,
        }

        files = {}
        if fichier_cv:
            files['cv'] = (fichier_cv.name, fichier_cv.read(), fichier_cv.content_type)

        try:
            response = requests.post(API_URL, data=data, files=files)
            if response.status_code == 201:
                messages.success(request, "Candidat enregistré avec succès.")
                return redirect('candidat_create')  # ou une autre page
            else:
                messages.error(request, f"Erreur: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Connexion à l’API impossible : {str(e)}")

    return render(request, 'dashboardCandidats/profil.html')


def login_view(request):
    if request.method == "POST":
        data = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password")
        }

        response = requests.post(
            "http://127.0.0.1:8001/api/auth/login/",
            json=data
        )

        if response.status_code == 200:
            tokens = response.json()
            request.session["accessToken"] = tokens.get("access")
            request.session["refreshToken"] = tokens.get("refresh")

            access_token = request.session["accessToken"]
            headers = {"Authorization": f"Bearer {access_token}"}

            # Appel pour récupérer le profil utilisateur
            profile_response = requests.get(
                "http://127.0.0.1:8001/api/auth/profile/",
                headers=headers
            )

            if profile_response.status_code == 200:
                profile = profile_response.json()
                role = profile.get("role")  # Assurez-vous que le champ s'appelle bien 'role' dans l'API

                return redirect('dashboard')                

            else:
                return render(request, 'login.html', {"error": "Impossible de récupérer le profil."})
        else:
            return render(request, 'login.html', {"error": "Identifiants invalides."})

    return render(request, 'login.html')


def register(request):
    
    if (request.method == "POST") :
        data = {
            "email" : request.POST.get("email"),
            "password": request.POST.get("password"),
            "role" : request.POST.get("role")
        }
        
        response = requests.post(
            
            "http://127.0.0.1:8001/api/auth/register/", 
            json=data  
        )
        
        if(response.status_code == 201) :
            
            return redirect("login")
    
    
    
    return render(request, 'register.html')

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from requests.exceptions import RequestException

def dashboard_view(request):
    access_token = request.session.get("accessToken")
    if not access_token:
        messages.warning(request, "Veuillez vous connecter pour accéder au dashboard.")
        return redirect("login")

    headers = {"Authorization": f"Bearer {access_token}"}
    profile = {}
    offres = []
    error_message = None

    # Récupérer le profil utilisateur
    try:
        profile_response = requests.get("http://127.0.0.1:8001/api/auth/profile/", headers=headers)
        profile_response.raise_for_status()
        profile = profile_response.json()
        print("Profil récupéré :", profile)
    except RequestException as e:
        messages.error(request, f"Erreur lors de la récupération du profil : {e}")
        return redirect("login")

    # Vérifier le rôle
    role = profile.get("role")
    if role != "Candidat":
        return render(request, "dashboardPME_templates/index.html", {"profile": profile})

    # Récupérer les offres d'emploi
    try:
        api_url = "http://127.0.0.1:8001/api/pme/offres/"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print("Données des offres :", data)
        if isinstance(data, dict) and "results" in data:
            offres = data.get("results", [])
        else:
            offres = data

        # Formater les dates et le nom de l'entreprise
        for offre in offres:
            if "date_publication" in offre:
                date_obj = datetime.strptime(offre["date_publication"], "%Y-%m-%dT%H:%M:%SZ")
                offre["date_publication"] = date_obj.strftime("%d/%m/%Y %H:%M")

            if "entreprise" in offre and offre["entreprise"]:
                if isinstance(offre["entreprise"], dict) and "nom" in offre["entreprise"]:
                    offre["entreprise_nom"] = offre["entreprise"]["nom"]
                else:
                    offre["entreprise_nom"] = "Non spécifié"
            else:
                offre["entreprise_nom"] = "Non spécifié"

    except RequestException as e:
        error_message = f"Erreur lors de la récupération des offres : {e}"
        print(f"Erreur offres :", error_message)

    context = {
        "profile": profile,
        "offres": offres,
        "error_message": error_message,
        "titre_page": "Dashboard du Candidat",
    }

    return render(request, "dashboardCan_templates/index_can.html", context)
def edit_profile(request):
    return render(request, 'profile/edit_profile.html')

def profil_view(request):
    access_token = request.session.get("accessToken")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        "http://127.0.0.1:8001/api/auth/profile/",
        headers=headers
    )
    
    if(response.status_code == 200):
        profile = response.json()
        
        if(profile.get('role') == 'Candidat'):
            return render(request ,'dashboardCan_templates/profil.html', {"profile" :profile})
        else :
            return render(request ,'dashboardPME_templates/profil.html', {"profile" :profile})



def upload_cv_view(request):
    access_token = request.session.get("accessToken")

    if not access_token:
        # Rediriger vers la page de connexion ou afficher un message d'erreur
        return redirect('login_page') # Assurez-vous d'avoir une URL nommée 'login_page'

    if request.method == "POST":
        if 'cv_file' not in request.FILES:
            # Gérer l'erreur si aucun fichier n'a été sélectionné
            return render(request, 'dashboardCan_templates/profil.html', {
                "error_message": "Veuillez sélectionner un fichier CV.",
                "profile": {} # Passe les données du profil si tu en as besoin pour réafficher la page
            })

        cv_file = request.FILES['cv_file']
        # Vérifiez le type de fichier si nécessaire (ex: si tu n'autorises que PDF)
        # if not cv_file.name.lower().endswith(('.pdf', '.doc', '.docx')):
        #     return render(request, 'dashboardCan_templates/profil.html', {
        #         "error_message": "Seuls les fichiers PDF, DOC et DOCX sont autorisés.",
        #         "profile": {}
        #     })

        headers = {"Authorization": f"Bearer {access_token}"}
        # Les fichiers doivent être envoyés dans le paramètre 'files' de requests.put/post
        # La clé 'cv' doit correspondre au nom de champ attendu par ton API pour le CV
        files = {'cv': (cv_file.name, cv_file.read(), cv_file.content_type)}

        try:
            # Si ton API gère le CV comme un champ du profil principal (PATCH pour mise à jour partielle)
            # Ou un endpoint spécifique si l'API l'attend
            response_cv_upload = requests.patch(f"{settings.API_BASE_URL}profile/", files=files, headers=headers)
            # Remplace settings.API_BASE_URL par l'URL de base de ton API si elle n'est pas dans settings

            if response_cv_upload.status_code == 200:
                # Si l'API renvoie les données du profil mises à jour, tu peux les utiliser
                updated_profile_data = response_cv_upload.json()
                # Tu peux rediriger l'utilisateur vers la page de profil pour voir la mise à jour
                return redirect('profile_view_candidat') # Redirige vers ta vue principale de profil
                # Ou tu peux le rendre sur la même page avec un message de succès
                # return render(request, 'dashboardCan_templates/profil.html', {
                #     "profile": updated_profile_data,
                #     "success_message": "CV téléversé avec succès !"
                # })
            else:
                error_message = f"Échec du téléversement du CV: {response_cv_upload.status_code} - {response_cv_upload.text}"
                return render(request, 'dashboardCan_templates/profil.html', {
                    "error_message": error_message,
                    "profile": {} # Réaffiche la page avec les dernières données connues ou vide
                })

        except requests.exceptions.ConnectionError:
            return render(request, 'dashboardCan_templates/profil.html', {
                "error_message": "Impossible de se connecter à l'API pour le téléversement du CV.",
                "profile": {}
            })
        except Exception as e:
            return render(request, 'dashboardCan_templates/profil.html', {
                "error_message": f"Une erreur inattendue est survenue lors du téléversement du CV: {e}",
                "profile": {}
            })
    else:
        # Si quelqu'un essaie d'accéder à cette URL directement avec GET
        return redirect('profile_view_candidat') # Redirige vers la page de profil        
from django.shortcuts import render, redirect
import requests

from django.shortcuts import render, redirect
import requests
from django.shortcuts import render, redirect
import requests

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from requests.exceptions import RequestException
from django.conf import settings # Assurez-vous que settings est importé

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from requests.exceptions import RequestException
from django.conf import settings
import os # Import the os module

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import os # Importer le module os pour la manipulation des chemins

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import os

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import os

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import os

# URL de base de l'API pour les profils candidats
CANDIDAT_PROFILE_API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"

def profile_view_candidat(request):
    access_token = request.session.get("accessToken")

    # Rediriger si l'utilisateur n'est pas connecté
    if not access_token:
        messages.warning(request, "Veuillez vous connecter pour voir ou créer votre profil.")
        return redirect('login_view') 

    headers = {"Authorization": f"Bearer {access_token}"}
    profile_data = {} 
    profile_exists = False 

    context = {
        'titre_page': "Mon Profil Candidat",
        'profile_data': {}, 
        'error_message': None,
        'success_message': None,
        'info_message': None, # Ce sera le message affiché en cas de profil déjà existant
        'profile_exists': False, 
    }

    # --- Tenter de récupérer le profil existant (pour les requêtes GET) ---
    try:
        response_get = requests.get(CANDIDAT_PROFILE_API_URL, headers=headers)
        if response_get.status_code == 200:
            profile_data = response_get.json()
            profile_exists = True
            context['profile_exists'] = True 
            # context['info_message'] = "Vous avez déjà un profil. Vous pouvez le modifier ci-dessous."
            if 'cv' in profile_data and profile_data['cv']:
                profile_data['cv_filename'] = os.path.basename(profile_data['cv'])
        elif response_get.status_code == 404:
            profile_exists = False
            context['profile_exists'] = False 
            context['info_message'] = "Vous n'avez pas encore de profil. Veuillez en créer un."
        else:
            error_message = f"Erreur lors de la récupération du profil: {response_get.status_code} - {response_get.text}"
            if response_get.status_code == 401:
                request.session.pop("accessToken", None) 
                messages.error(request, "Votre session a expiré ou est invalide. Veuillez vous reconnecter.")
                return redirect('login_view')
            context['error_message'] = error_message
            context['profile_data'] = profile_data 
            return render(request, 'dashboardCan_templates/profil.html', context)

    except requests.exceptions.ConnectionError:
        context['error_message'] = "Impossible de se connecter à l'API du profil. Veuillez vérifier que le backend est en cours d'exécution."
        context['profile_data'] = profile_data 
        return render(request, 'dashboardCan_templates/profil.html', context)
    except Exception as e:
        context['error_message'] = f"Vous avez deja un profil "
        context['profile_data'] = profile_data 
        return render(request, 'dashboardCan_templates/profil.html', context)

    context['profile_data'] = profile_data

    # --- Gérer la soumission du formulaire (requêtes POST) ---
    if request.method == "POST":
        form_data = {
            "nom_complet": request.POST.get("nom_complet", ""),
            "email": request.POST.get("email", ""),
            "description": request.POST.get("description", ""),
            
        }
        cv_file = request.FILES.get('cv')

        files = {}
        if cv_file:
            files['cv'] = (cv_file.name, cv_file.read(), cv_file.content_type)
        
        if not cv_file and 'cv_filename' in context['profile_data']:
            form_data['cv_filename'] = context['profile_data']['cv_filename']
        elif cv_file:
            form_data['cv_filename'] = cv_file.name

        try:
            response = requests.post(CANDIDAT_PROFILE_API_URL, data=form_data, files=files, headers=headers)
            
            action_message = "créé" 
            if profile_exists or response.status_code == 200:
                action_message = "mis à jour"

            if response.status_code in [200, 201]:
                profile_data_returned = response.json()
                if 'cv' in profile_data_returned and profile_data_returned['cv']:
                    profile_data_returned['cv_filename'] = os.path.basename(profile_data_returned['cv'])
                context['profile_data'] = profile_data_returned 
                context['success_message'] = f"Profil {action_message} avec succès !"
                context['profile_exists'] = True 
                # Si le profil a été mis à jour, nous réinitialisons info_message pour éviter la redondance
                context['info_message'] = "Vous avez déjà un profil. Vous pouvez le modifier ci-dessous." if profile_exists else None

            else:
                error_details = response.json() if response.content else {}
                validation_errors = []
                
                
                if response.status_code == 400 and "already exists" in response.text.lower():
                    context['info_message'] = "Vous avez déjà un profil. Veuillez le modifier plutôt que d'essayer d'en créer un nouveau."
                    context['profile_exists'] = True # On sait qu'un profil existe
                  
                    context['info_message'] = "Un profil existe déjà pour cet utilisateur. Veuillez le modifier."
                    context['profile_exists'] = True
                # --- FIN NOUVELLE LOGIQUE ---
                
                else: # Autres erreurs de validation ou d'API
                    if isinstance(error_details, dict):
                        for field, errors in error_details.items():
                            if field == 'detail':
                                validation_errors.append(errors)
                            elif isinstance(errors, list):
                                validation_errors.append(f"{field.capitalize()}: {' '.join(errors)}")
                            else:
                                validation_errors.append(f"{field.capitalize()}: {errors}")
                    else:
                        validation_errors.append(str(error_details))
                    context['error_message'] = "Erreurs de validation : <br>" + "<br>".join(validation_errors)
                
                context['profile_data'].update(form_data) 
                
        except requests.exceptions.ConnectionError:
            context['error_message'] = "Impossible de se connecter à l'API pour soumettre le profil."
        except Exception as e:
            context['error_message'] = f"Vous avez deja un profil"
        
    return render(request, 'dashboardCan_templates/profil.html', context)


def offres_emploi_can(request):
    """Affiche la liste des offres d'emploi actives pour les candidats"""
    access_token = request.session.get("accessToken")
    
    if not access_token:
        messages.error(request, "Vous devez être connecté pour accéder aux offres d'emploi")
        return render(request, 'main_app/offres_emploi_can.html', {
            'offres': [],
            'title': 'Accès non autorisé',
            'nombre_offres': 0,
        })

    try:
        # Appel à l'API backend avec authentification
        api_url = "http://127.0.0.1:8001/api/candidat/offres/"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        offres = data.get('results', [])
        
        # Filtrage des offres actives
        offres_actives = [offre for offre in offres if offre.get('est_actif', False)]
        
        # Pagination
        paginator = Paginator(offres_actives, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'offres': page_obj,
            'title': 'Offres d\'emploi disponibles',
            'nombre_offres': data.get('count', len(offres_actives)),
            'page_obj': page_obj,
        }
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            messages.error(request, "Session expirée. Veuillez vous reconnecter.")
        else:
            messages.error(request, f"Erreur serveur: {str(e)}")
        
        context = {
            'error': f"Erreur d'authentification: {str(e)}",
            'offres': [],
            'title': 'Erreur de chargement',
            'nombre_offres': 0,
        }
    
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Erreur de connexion au serveur: {str(e)}")
        context = {
            'error': f"Impossible de se connecter au serveur: {str(e)}",
            'offres': [],
            'title': 'Erreur de connexion',
            'nombre_offres': 0,
        }
    
    return render(request, 'dashboardCan_templates/offres_emploi_can.html', context)


def offre_detail_candidat(request, offre_id):
    """Vue spécifique pour les candidats"""
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour voir les détails.")
        return redirect("login_page")

    api_url = f"http://127.0.0.1:8001/api/candidat/offres/{offre_id}/"
    offre = {}
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        offre = response.json()
        # Formatage de la date si nécessaire
        if 'date_publication' in offre:
            date_obj = datetime.strptime(offre['date_publication'], '%Y-%m-%dT%H:%M:%S.%fZ')
            offre['date_publication'] = date_obj.strftime('%d/%m/%Y %H:%M')

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            error_message = "Cette offre n'existe pas ou a été supprimée"
        else:
            error_message = f"Erreur serveur: {e}"
        print(f"Erreur API (candidat): {e}")

    context = {
        'offre': offre,
        'error_message': error_message,
        'titre_page': f"Détails de l'offre - {offre.get('titre', 'Inconnue')}"
    }
    
    return render(request, 'dashboardCan_templates/offre_detail.html', context)


def postuler_offre(request, offre_id):
    token = request.session.get("accessToken")
    if not token:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Veuillez vous connecter pour postuler.'}, status=401)
        messages.warning(request, "Veuillez vous connecter pour postuler.")
        return redirect("login_page")

    headers = {"Authorization": f"Bearer {token}"}
    
    # Vérifier les candidatures existantes
    check_url = f"http://127.0.0.1:8001/api/candidat/applications/?offre={offre_id}"
    check_response = requests.get(check_url, headers=headers)
    
    if check_response.status_code == 200 and len(check_response.json().get('results', [])) > 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Vous avez déjà postulé à cette offre'}, status=400)
        messages.warning(request, "Vous avez déjà postulé à cette offre")
        return redirect('offre_detail_candidat', offre_id=offre_id)
    
    # Envoyer la candidature
    api_url = "http://127.0.0.1:8001/api/candidat/applications/"
    data = {"offre": offre_id}
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 201:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "Votre candidature a bien été enregistrée !")
        else:
            error = response.json().get('detail', 'Échec de la candidature')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error}, status=400)
            messages.error(request, f"Erreur: {error}")
            
    except requests.exceptions.RequestException as e:
        error = f"Erreur de connexion: {str(e)}"
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': error}, status=500)
        messages.error(request, error)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Requête invalide'}, status=400)
    return redirect('offre_detail_candidat', offre_id=offre_id)



def telecharger_offre(request):
    """Vue temporaire en attendant l'implémentation complète"""
    # TODO: À implémenter par [nom du collègue]
    context = {}  # contexte vide pour l'instant
    return render(request, 'main_app/offres_emploi_can.html', context)
        
        