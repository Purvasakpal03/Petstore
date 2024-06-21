from django.shortcuts import render
from .models import pet,customer
from django.views.generic import DateDetailView,ListView,CreateView,DetailView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
class petview(ListView):
    model=pet
    template_name='petview.html'
    context_object_name='petobj'

def search(request):
    if request.method=="POST":
        searchdata=request.POST.get('searchquery')
        petobj=pet.objects.filter(Q(name__icontains=searchdata)|(Q(breed__icontains=searchdata)) | (Q(species__icontains=searchdata)))
        return render(request,'petview.html',{'petobj':petobj})
    
def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        epassword=make_password(password)

        cutobj=customer(name=name,email=email,phoneno=phoneno,password=epassword)
        cutobj.save()
        return render(request,'petview.html')

