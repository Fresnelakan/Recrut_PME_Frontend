from django.shortcuts import redirect, render
from django.http import JsonResponse

from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import requests
from django.shortcuts import render
from django.conf import settings 

def index(request):
    return render(request, 'index.html')




from django.contrib import messages

API_URL = "http://127.0.0.1:8001/api/candidat/profil/candidat/"  # remplace cette URL par l’URL réelle de ton API




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
        return redirect("login_page")

    api_url = "http://127.0.0.1:8001/api/pme/offres/"
    offres = []
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print("Données de l'API brutes:", data) # Débogage pour voir la date brute
        if isinstance(data, dict) and 'results' in data:
            offres_brutes = data.get('results', [])
        else:
            offres_brutes = data

        # --- Traitement des offres pour formater la date ---
        for offre in offres_brutes:
            if 'date_publication' in offre and offre['date_publication']:
                try:
                    # Parse la chaîne ISO 8601 avec les microsecondes et le 'Z'
                    # fromisoformat gère très bien ce format
                    # .replace('Z', '+00:00') est une astuce si fromisoformat rencontre des problèmes avec 'Z' direct
                    # Ou utiliser dateutil.parser.isoparse si installé (pip install python-dateutil)
                    # Pour Python 3.7+, datetime.fromisoformat gère le 'Z' si l'API est stricte.
                    # Si non, on peut faire un strip('Z') puis ajouter '+00:00'
                    date_str = offre['date_publication'].replace('Z', '+00:00')
                    date_obj = datetime.fromisoformat(date_str)

                    # Optionnel: convertir au fuseau horaire local si USE_TZ = True dans settings.py
                    # from django.utils import timezone
                    # date_obj = timezone.localtime(date_obj)

                    # Formate la date comme souhaité : "JJ-MM-AAAA à HH:MM:SS"
                    offre['date_publication_formatee'] = date_obj.strftime("%d-%m-%Y à %H:%M:%S")
                except ValueError as ve:
                    print(f"Erreur de formatage de date pour {offre.get('titre')}: {offre['date_publication']} - {ve}")
                    offre['date_publication_formatee'] = "Date invalide"
                except Exception as e:
                    print(f"Erreur inattendue lors du traitement de la date pour {offre.get('titre')}: {e}")
                    offre['date_publication_formatee'] = "Erreur de date"
            else:
                offre['date_publication_formatee'] = "Non spécifiée"
            offres.append(offre) # Ajoute l'offre traitée à la liste finale
        # --- Fin du traitement ---

    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer les offres depuis le backend : {e}"
        print(f"Erreur lors de l'appel API pour la liste des offres : {e}")

    context = {
        'offres': offres, # C'est maintenant la liste des offres AVEC la date formatée
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
def profile_view_candidat(request):
    access_token = request.session.get("accessToken")

    if not access_token:
        # Gérer l'absence de token (rediriger vers login, message d'erreur, etc.)
        # return redirect('login_page') # Exemple
        return render(request, 'dashboardCan_templates/profil.html', {"error_message": "Veuillez vous connecter pour voir votre profil."})

    headers = {"Authorization": f"Bearer {access_token}"}
    profile_data = {} # Initialise un dictionnaire vide pour les données du profil

    # --- Récupération du profil (GET) ---
    try:
        response_get = requests.get(f"http://127.0.0.1:8001/api/auth/profile/", headers=headers)

        if response_get.status_code == 200:
            profile_data = response_get.json()
            # Pour l'affichage des CV: vérifie si ton API renvoie un champ 'cv_url' ou 'cv_filename'
            # profile_data['cv_filename'] = profile_data.get('cv', '').split('/')[-1] if profile_data.get('cv') else ''
            # profile_data['cv_url'] = profile_data.get('cv', '') # Assurez-vous que l'API renvoie l'URL complète
        else:
            # Gérer les erreurs GET
            error_message = f"Erreur lors de la récupération du profil: {response_get.status_code} - {response_get.text}"
            if response_get.status_code == 401:
                request.session.pop("accessToken", None)
                error_message = "Votre session a expiré ou est invalide. Veuillez vous reconnecter."
            return render(request, 'dashboardCan_templates/profil.html', {"error_message": error_message})

    except requests.exceptions.ConnectionError:
        return render(request, 'dashboardCan_templates/profil.html', {"error_message": "Impossible de se connecter à l'API du profil."})
    except Exception as e:
        return render(request, 'dashboardCan_templates/profil.html', {"error_message": f"Une erreur inattendue est survenue: {e}"})

    # --- Gestion de la mise à jour du profil (POST pour les infos de contact) ---
    if request.method == "POST":
        # Vérifie si le formulaire POST est celui des infos de contact
        if 'full_name' in request.POST: # Un champ unique au formulaire de contact
            # Récupération des données du formulaire
            updated_data = {
                "full_name": request.POST.get("full_name"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("phone"),
                "mobile": request.POST.get("mobile"),
                "address": request.POST.get("address"),
                # Ajoute d'autres champs de profil modifiables ici
            }
            # Supprime les valeurs None pour éviter d'écraser des données si un champ est vide
            updated_data = {k: v for k, v in updated_data.items() if v is not None}

            try:
                # Utilise requests.put si c'est une mise à jour complète (remplace tout le profil)
                # ou requests.patch si c'est une mise à jour partielle (modifie juste les champs envoyés)
                # Assure-toi que l'URL de ton API est correcte pour la mise à jour (souvent le même /profile/)
                response_put = requests.put(f"http://127.0.0.1:8001/api/auth/profile/", json=updated_data, headers=headers)

                if response_put.status_code == 200:
                    profile_data = response_put.json() # Met à jour les données affichées avec la nouvelle réponse
                    return render(request, 'dashboardCan_templates/profil.html', {
                        "profile": profile_data,
                        "success_message": "Profil mis à jour avec succès !"
                    })
                else:
                    error_message = f"Échec de la mise à jour du profil: {response_put.status_code} - {response_put.text}"
                    return render(request, 'dashboardCan_templates/profil.html', {
                        "profile": profile_data, # Retourne les dernières données connues
                        "error_message": error_message
                    })
            except requests.exceptions.ConnectionError:
                return render(request, 'dashboardCan_templates/profil.html', {"profile": profile_data, "error_message": "Impossible de se connecter à l'API pour la mise à jour."})
            except Exception as e:
                return render(request, 'dashboardCan_templates/profil.html', {"profile": profile_data, "error_message": f"Erreur inattendue lors de la mise à jour: {e}"})

        # --- Gestion de l'upload de CV (POST pour le CV) ---
        elif 'cv_file' in request.FILES: # Vérifie si le formulaire POST est celui du CV
            cv_file = request.FILES['cv_file']
            files = {'cv': (cv_file.name, cv_file.read(), cv_file.content_type)}

            try:
                # Assure-toi que ton API a un endpoint spécifique pour l'upload de CV
                # ou que le endpoint de profil gère les uploads de fichiers
                response_cv_upload = requests.put(f"http://127.0.0.1:8001/api/auth/profile/", files=files, headers=headers) # Utilise PUT/PATCH si le CV est une partie du profil

                if response_cv_upload.status_code == 200:
                    profile_data = response_cv_upload.json()
                    return render(request, 'dashboardCan_templates/profil.html', {
                        "profile": profile_data,
                        "success_message": "CV téléversé avec succès !"
                    })
                else:
                    error_message = f"Échec du téléversement du CV: {response_cv_upload.status_code} - {response_cv_upload.text}"
                    return render(request, 'dashboardCan_templates/profil.html', {
                        "profile": profile_data,
                        "error_message": error_message
                    })
            except requests.exceptions.ConnectionError:
                return render(request, 'dashboardCan_templates/profil.html', {"profile": profile_data, "error_message": "Impossible de se connecter à l'API pour le CV."})
            except Exception as e:
                return render(request, 'dashboardCan_templates/profil.html', {"profile": profile_data, "error_message": f"Erreur inattendue lors de l'upload du CV: {e}"})

    # Si la requête n'est ni GET ni POST, ou si POST n'est pas géré 
    return render(request, 'dashboardCan_templates/profil.html', {"profile": profile_data})

       
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
    


from django.core.paginator import Paginator

def profile_view_pme(request):
    access_token = request.session.get("accessToken")
    headers = {"Authorization": f"Bearer {access_token}"}
    

    response = requests.get(
        "http://127.0.0.1:8001/api/auth/profile/",
        headers=headers
    )
    
    if(response.status_code == 200):
        profile = response.json().get("results")
        
        return render(request, 'dashboardCan_templates/profil.html', {"profile" :profile})
    
    else :
        return render(request, 'dashboardCan_templates/profil.html', {"erreur" :"Shit neggae"})
    

## A revoir pour plus tard

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


# views.py
def profile_candidat_view(request):
    """Récupère le profil candidat"""
    token = request.session.get("accessToken")
    if not token:
        return redirect('login')
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Récupération du profil complet
        response = requests.get(
            "http://127.0.0.1:8001/api/candidat/profil/candidat/",
            headers=headers
        )
        if response.status_code == 200:
            return render(request, 'dashboardCan_templates/profil.html', {
                'profile': response.json()
            })
    except requests.exceptions.RequestException as e:
        print(f"Erreur API: {e}")
    
    return render(request, 'dashboardCan_templates/profil.html', {
        'error_message': "Erreur lors de la récupération du profil"
    })

def update_profil_candidat(request):
    """Met à jour les infos du candidat"""
    if request.method == 'POST':
        token = request.session.get("accessToken")
        if not token:
            return JsonResponse({'error': 'Non authentifié'}, status=401)
        
        data = {
            'nom_complet': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'adresse': request.POST.get('address'),
            'role': request.POST.get('role')
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                "http://127.0.0.1:8001/api/candidat/profil/candidat/",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return JsonResponse({'success': True})
            return JsonResponse({'error': response.text}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def upload_cv_candidat(request):
    """Gère l'upload du CV"""
    if request.method == 'POST' and request.FILES.get('cv_file'):
        token = request.session.get("accessToken")
        if not token:
            return JsonResponse({'error': 'Non authentifié'}, status=401)
        
        cv_file = request.FILES['cv_file']
        files = {'cv': (cv_file.name, cv_file.read(), cv_file.content_type)}
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.post(
                "http://127.0.0.1:8001/api/candidat/profil/candidat/",
                files=files,
                headers=headers
            )
            
            if response.status_code == 200:
                return JsonResponse({'success': True, 'filename': cv_file.name})
            return JsonResponse({'error': response.text}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Fichier manquant'}, status=400)


def supprimer_offre(request, offre_id):
    token = request.session.get("accessToken")
    if not token:
        # Pour une requête AJAX, renvoyer un statut 401 Unauthorized
        return JsonResponse({"success": False, "message": "Veuillez vous connecter pour supprimer une offre."}, status=401)

    api_url = f"http://127.0.0.1:8001/api/pme/offres/{offre_id}/"

    if request.method == "DELETE": # Utiliser la méthode DELETE pour l'API REST
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.delete(api_url, headers=headers)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

            # Si tout est bon, renvoyer une réponse JSON de succès
            return JsonResponse({"success": True, "message": "Offre supprimée avec succès !"})
        except requests.exceptions.RequestException as e:
            error_message = f"Erreur lors de la suppression de l’offre : {e}"
            print(f"Erreur lors de l'appel API pour la suppression : {e}")
            # Renvoyer une réponse JSON d'erreur avec un statut approprié
            return JsonResponse({"success": False, "message": error_message}, status=response.status_code if response else 500)
    else:
        # Si la méthode n'est pas DELETE, renvoyer une erreur 405 Method Not Allowed
        return JsonResponse({"success": False, "message": "Méthode non autorisée pour la suppression."}, status=405)
    

def liste_candidatures_candidat(request):
    token = request.session.get("accessToken")
    if not token:
        messages.warning(request, "Veuillez vous connecter pour voir vos candidatures.")
        return redirect("login_page") # Redirige vers la page de connexion si pas de token

    api_url = "http://127.0.0.1:8001/api/candidat/applications/"
    candidatures = []
    error_message = None

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP

        data = response.json()
        candidatures_brutes = data.get('results', []) # L'API renvoie un dictionnaire avec 'results'

        for candidature in candidatures_brutes:
            # Traitement de la date de soumission
            if 'date_soumission' in candidature and candidature['date_soumission']:
                try:
                    # Parse la chaîne ISO 8601
                    date_str = candidature['date_soumission'].replace('Z', '+00:00')
                    date_obj = datetime.fromisoformat(date_str)
                    candidature['date_soumission_formatee'] = date_obj.strftime("%d-%m-%Y à %H:%M:%S")
                except ValueError as ve:
                    print(f"Erreur de formatage de date pour candidature {candidature.get('id')}: {candidature['date_soumission']} - {ve}")
                    candidature['date_soumission_formatee'] = "Date invalide"
                except Exception as e:
                    print(f"Erreur inattendue lors du traitement de la date pour candidature {candidature.get('id')}: {e}")
                    candidature['date_soumission_formatee'] = "Erreur de date"
            else:
                candidature['date_soumission_formatee'] = "Non spécifiée"
            candidatures.append(candidature)

    except requests.exceptions.RequestException as e:
        error_message = f"Impossible de récupérer vos candidatures : {e}"
        print(f"Erreur lors de l'appel API pour les candidatures du candidat : {e}")
    except Exception as e:
        error_message = f"Une erreur inattendue s'est produite lors de la récupération des candidatures : {e}"
        print(f"Erreur inattendue : {e}")

    context = {
        'candidatures': candidatures,
        'error_message': error_message,
        'titre_page': "Mes Candidatures",
    }

    # Le nouveau template sera dans 'dashboardCan_templates'
    return render(request, 'dashboardCan_templates/candidatures_candidat.html', context)




def telecharger_offre(request):
    """Vue temporaire en attendant l'implémentation complète"""
    # TODO: À implémenter par [nom du collègue]
    context = {}  # contexte vide pour l'instant
    return render(request, 'main_app/offres_emploi_can.html', context)