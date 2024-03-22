import uuid
import boto3
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Car, Photo, Profile, Review, CATEGORY
from django import forms
from .forms import CarForm
from django.db.models import Q
from django.urls import reverse_lazy

# Define the home view
def home(request):
    cars = Car.objects.all()
    if len(cars) >= 4:
        cars_to_display = cars[len(cars)-4:]
    elif cars:
        cars_to_display = cars 
    else:
        cars_to_display = []
    return render(request, 'home.html', {
        'cars': cars_to_display
    })

def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

def cars_index(request):
  cars = Car.objects.all()
  return render(request, 'cars/index.html', {
    'cars': cars
  })

def cars_detail(request, car_id):
  car = Car.objects.get(id=car_id)
  user = request.user
  return render(request, 'cars/detail.html', {
    'car': car,
    'user': user
  })

@login_required
def add_photo(request, car_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, car_id=car_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', car_id=car_id)

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'year', 'milage', 'previous_owners', 'condition', 'color', 'price', 'category']
    success_url = '/cars/categories/'

    def form_valid(self, form):
        form.instance.published_by = self.request.user
        return super().form_valid(form)

class CarUpdate(LoginRequiredMixin, UpdateView):
    model = Car
    fields = ['make', 'model', 'year', 'milage', 'previous_owners', 'condition', 'color', 'price', 'category', 'sold']
    success_url = '/cars/categories/'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['sold'].required = False
        return form
    
class CarDelete(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = '/cars/categories/'

@login_required
def garage(request, user_id):
    viewer = request.user
    user = User.objects.get(id=user_id) 
    active_listings = Car.objects.filter(published_by=user, sold="For Sale")
    sold_history = Car.objects.filter(
        Q(published_by=user, sold="Sold") | Q(published_by=user, sold="Reserved")
    )
    reviews = Review.objects.filter(user_receiver=user)
    profile = Profile.objects.get(user=user)
    favorite_cars = profile.favorite_cars.all()
    return render(request, 'garage.html', {
        # avatar render
        'viewer': viewer,
        'profile': profile,
        'user': user,
        'active_listings': active_listings,
        'sold_history': sold_history,
        'favorite_cars': favorite_cars,
        'reviews' : reviews,
    })

@login_required
def add_avatar(request, user_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, user_id=user_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('garage', user_id=user_id)

@login_required
def add_to_favorites(request, car_id):
    if request.method == 'POST':
      car = Car.objects.get(id=car_id)
      profile = Profile.objects.get(user=request.user)
      profile.favorite_cars.add(car)
    return redirect('detail', car_id=car_id)

class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'content']
    success_url = None

    def form_valid(self, form):
        form.instance.user_sender = self.request.user
        user_id = self.kwargs['user_id']
        user_receiver = get_object_or_404(User, pk=user_id)
        form.instance.user_receiver = user_receiver
        return super().form_valid(form)
    
    def get_success_url(self):
        # get the original path without 'createreview' part
        return reverse_lazy('garage', kwargs={'user_id': self.kwargs['user_id']})
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
      # This is how to create a 'user' form object
      # that includes the data from the browser
      form = UserCreationForm(request.POST)
      if form.is_valid():
        # This will add the user to the database
        user = form.save()
        # This is how we log a user in via code
        login(request, user)
        return redirect('home')
      else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# Assuming you have a view like this
def car_list(request):
    car_by_category = {}
    for cat1, cat2 in CATEGORY:
        car_by_category[cat2] = Car.objects.filter(category=cat2)
    car_by_category = car_by_category.items()
    print ("categories", car_by_category)
    return render(request, 'cars/index.html', {'car_by_category': car_by_category})

