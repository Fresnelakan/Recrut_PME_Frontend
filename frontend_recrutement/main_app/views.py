from django.shortcuts import redirect, render
import requests
def index(request):
    return render(request, 'index.html')

import requests
from django.shortcuts import render, redirect

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

                # Redirection selon le rôle
                if role == "Candidat":
                    return render(request ,'dashboardCan_templates/index_can.html')  # Nom de votre URL vers le tableau de bord candidat
                else:
                    return render(request ,'dashboardPME_templates/index.html')  # Tableau de bord général/autre

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
        
        return render(request, 'dashboard_templates/index.html', {"profile" :profile})
    
    return render(request, 'dashboard_templates/index.html')
