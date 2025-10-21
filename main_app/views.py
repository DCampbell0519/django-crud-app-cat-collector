from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView   
from .models import Cat, Toy
from .forms import FeedingForm, CustomUserCreationForm
from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
# This is used for function based views
from django.contrib.auth.decorators import login_required
# This is used for class based views
from django.contrib.auth.mixins import LoginRequiredMixin 


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how we create a 'user' form object that includes the data from the browser
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): 
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or GET request, so render signup.html with an empty form
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

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

# def home(request):
#     return render(request, 'home.html')

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html') # DTL - Django Template Language

@login_required
def cats_index(request):
    # cats = Cat.objects.all()
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', { 'cats': cats }) # context is a dictionary

@login_required
def cat_detail(request, cat_id):  # Cat id is the url parameter of the cat's id
    cat = Cat.objects.get(id=cat_id)
    # Only get the toys the cat does not have
    toys = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    # toys = Toy.objects.all()
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys })

@login_required
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

@login_required
def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

@login_required
def remove_toy(request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id)
    cat.toys.remove(toy_id)
    return redirect('cat-detail', cat_id=cat.id)

class CatCreate(LoginRequiredMixin, CreateView):  # ModelForm
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # fields = '__all__'
    # success_url = '/cats/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

# class CatList(ListView):
#     model = Cat
#     template_name = 'cats/index.html'
#     def get_queryset(self):
        # return super().get_queryset().filter(user=self.request.user)
#       

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'


