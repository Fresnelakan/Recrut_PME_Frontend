from django.shortcuts import redirect, render
import requests

def index(request):
    return render(request, 'index.html')

def login_view(request):
    
    if (request.method == "POST") :
        data = {
            "email" : request.POST.get("email"),
            "password": request.POST.get("password")
        }
        
        response = requests.post(
            
            "http://127.0.0.1:8001/api/auth/login/", 
            json=data  
        )
        
        if(response.status_code == 200) :
            tokens= response.json()
            request.session["accessToken"] =tokens.get("access")
            request.session["refreshToken"] =tokens.get("refresh")
            return render( request,'dashboard.html')
        else :
            return render(request,'dashboard.html',{"error" : "identifiant invalide"})
    
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
    return render(request, 'dashboard.html')
