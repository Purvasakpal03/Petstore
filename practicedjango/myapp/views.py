from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .models import Taskapp
from django.urls import reverse_lazy
from .forms import createform

# Create your views here.
def hello(request):
    return HttpResponse("hello guys")

class tasklist(ListView):
    model=Taskapp
    template_name='showtask.html'
    context_object_name='to'

class createtask(CreateView):
    model=Taskapp
    form_class = createform
    template_name='createtask.html'
    success_url = reverse_lazy('tasklist')


class updatetask(UpdateView):
    model=Taskapp
    form_class = createform
    template_name='updatetask.html'
    success_url = reverse_lazy('tasklist')


class detailtask(DetailView):
    model=Taskapp
    template_name='taskdetails.html'
    context_object_name='i'

class deletetask(DeleteView):
    model=Taskapp
    template_name='deletetask.html'
    success_url = reverse_lazy('tasklist')