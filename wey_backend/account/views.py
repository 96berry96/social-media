from django.shortcuts import render
from django.http import HttpResponse

from .models import User

def activateemail(request):
    email = request.GET.get('email','')
    id = request.GET.get('id','')
    
    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
        
        return HttpResponse('The user is now activated. You can go ahead an log in.')
    else:
        return HttpResponse('Invalid activation link')

# Create your views here.
