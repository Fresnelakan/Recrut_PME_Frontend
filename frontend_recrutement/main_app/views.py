from django.shortcuts import redirect, render


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


# main_app/views.py
from django.shortcuts import render, redirect

def liste_offres_emploi(request):
    # URL de l'API backend qui expose la liste des offres
    # Assurez-vous que settings.BACKEND_API_URL est défini dans votre settings.py
    # et que '/api/offres/' est le chemin correct dans le urls.py de votre backend
    api_url = f"http://127.0.0.1:8001/api/candidat/offres/4/"

    offres = [] # Cette liste stockera les offres sous forme de dictionnaires Python
    error_message = None # Pour afficher les erreurs API ou de connexion

    try:
        # Faire une requête GET à l'API backend
        # Si votre API requiert une authentification, ajoutez les headers nécessaires ici
        # Exemple avec un token en session :
        # headers = {'Authorization': f'Bearer {request.session.get("access_token")}'}
        # response = requests.get(api_url, headers=headers)

        response = requests.get(api_url) # Appel HTTP GET
        response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

        # Si la requête est un succès (statut 200 OK), décoder la réponse JSON
        data = response.json()

        # Les API DRF paginées renvoient souvent un objet avec une clé 'results'
        # Si votre API est paginée, les offres seront dans data['results']
        if isinstance(data, dict) and 'results' in data:
             offres = data.get('results', [])
        else:
             # Si l'API renvoie directement une liste d'objets
             offres = data

        # Note : Les offres ici sont des dictionnaires Python, pas des instances de modèle OffreEmploi.

    except requests.exceptions.RequestException as e:
        # Gérer les erreurs de connexion (backend non démarré/accessible) ou les erreurs HTTP
        error_message = f"Impossible de récupérer les offres depuis le backend : {e}"
        print(f"Erreur lors de l'appel API pour la liste des offres : {e}") # Loguer l'erreur

    # Préparer le contexte à passer au template
    context = {
        'offres': offres, # Ceci est une liste de dictionnaires/listes vide en cas d'erreur
        'error_message': error_message, # Sera None si pas d'erreur
        'titre_page': "Liste des Offres d'Emploi",
    }

    # Rendre le template d'affichage de la liste
    # Assurez-vous que 'offres_emploi/liste_offres.html' est le chemin correct
    # Votre template doit itérer sur la liste 'offres' (qui contient des dictionnaires)
    return render(request, 'offres_emploi/liste_offres_emploi.html', context) # Nouveau : template pour l4



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

def dashboard_view(request):
    access_token = request.session.get("accessToken")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        "http://127.0.0.1:8001/api/auth/profile/",
        headers=headers
    )
    
    if(response.status_code == 200):
        profile = response.json()
        
        if(profile.get('role') == 'Candidat'):
            return render(request ,'dashboardCan_templates/index_can.html', {"profile" :profile})
        else :
            return render(request ,'dashboardPME_templates/index.html', {"profile" :profile})
            
            
    
    return render(request, 'dashboardPME_templates/index.html')

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
    headers = {"Authorization": f"Bearer {access_token}"}
    
    
    
    # if request.method == "POST":
    #     # Récupération des données
    #     nom_complet = request.POST.get("name")
    #     email = request.POST.get("email")
    #     role = request.POST.get("role")
    #     # cv_file = request.FILES.get("cv")  # attention : request.FILES pour les fichiers !

    #     # Préparation des données et fichiers
    #     data = {
    #         "name": nom_complet,
    #         "email": email,
    #         "role": role,
    #     }

        

        # Envoi de la requête POST en multipart/form-data
        # response = requests.put(
        #     "http://127.0.0.1:8001/api/profile/",
        #     data=data,
            
        #     headers=headers  # Ajoutez un token si nécessaire
        # )

        # print(response.status_code)
        # print(response.json())

        
        # if(response.status_code == 200) :
            
        #     profile = response.json()
        #     print(profile)
        #     return render(request, 'dashboardCan_templates/profil.html', {"profile" :profile})
        # else:
        #     return render(request, 'dashboardCan_templates/profil.html', {"erreur" :"Shit neggae"})
        
    
    

    response = requests.get(
        "http://127.0.0.1:8001/api/auth/profile/",
        headers=headers
    )
    
    if(response.status_code == 200):
        profile = response.json()
        print(profile)
        
        return render(request, 'dashboardCan_templates/profil.html', {"profile" :profile})
    
    else :
        return render(request, 'dashboardCan_templates/profil.html', {"erreur" :"Shit neggae"})
    


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
        
        