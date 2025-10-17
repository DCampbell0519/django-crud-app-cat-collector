from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView   
from .models import Cat, Toy
from .forms import FeedingForm

# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# cats = [
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') # DTL - Django Template Language

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats }) # context is a dictionary

def cat_detail(request, cat_id):  # Cat id is the url parameter of the cat's id
    cat = Cat.objects.get(id=cat_id)
    toys = Toy.objects.all()
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys })

def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)

    # validate the form
    if form.is_valid():
        # don't save the form to the db until it has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)

class CatCreate(CreateView):  # ModelForm
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # fields = '__all__'
    # success_url = '/cats/'

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

# class CatList(ListView):
#     model = Cat
#     template_name = 'cats/index.html'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
