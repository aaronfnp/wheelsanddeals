import uuid
import boto3
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Car, Photo, Profile

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

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
  return render(request, 'cars/detail.html', {
    'car': car
  })

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


# CARS CREATE AND UPDATE NEED TO REMOVE USER AND AUTO ADD

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'year', 'milage', 'previous_owners', 'condition', 'date_listed', 'color', 'price', 'category']
    success_url = '/cars'

    def form_valid(self, form):
        form.instance.published_by = self.request.user
        return super().form_valid(form)

class CarUpdate(UpdateView):
    model = Car
    fields = ['make', 'model', 'year', 'milage', 'previous_owners', 'condition', 'date_listed', 'color', 'price', 'category']
    success_url = '/cars'
    
class CarDelete(DeleteView):
    model = Car
    success_url = '/cars'

def add_listing(request):
    return render(request, 'add_listing.html')

def car_market(request):
    return render(request, 'car_market.html')

def my_garage(request):
    user = request.user
    active_listings = Car.objects.filter(published_by=user)
    sold_history = Car.objects.filter(published_by=user)
    profile = Profile.objects.get(user=user)
    favorite_cars = profile.favorite_cars.all()
    return render(request, 'my_garage.html', {
        'active_listings': active_listings,
        'sold_history': sold_history,
        'favorite_cars': favorite_cars,
    })

def add_to_favorites(request, car_id):
    car = Car.objects.get(id=car_id)
    profile = Profile.objects.get(user=request.user)
    profile.favorite_cars.add(car)
    return redirect('index', car_id=car_id)