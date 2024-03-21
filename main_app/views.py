import uuid, boto3, os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Car, Photo, Profile, Review, CATEGORY
from django import forms
from .forms import UpdateUserForm, UpdateProfileForm, CarForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q


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

def car_list(request):
    car_by_category = {}
    for cat1, cat2 in CATEGORY:
        car_by_category[cat2] = Car.objects.filter(category=cat2)
    car_by_category = car_by_category.items()
    print ("categories", car_by_category)
    return render(request, 'cars/index.html', {'car_by_category': car_by_category})

def cars_detail(request, car_id):
  car = Car.objects.get(id=car_id)
  return render(request, 'cars/detail.html', {
    'car': car
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

# WENT WITH CLASS BASED VIEW
# def add_review(request, profile_id):
#     form = ReviewForm(request.POST)
#     # all user_id will probably be profile id
#     if form.is_valid():
#         new_review = form.save(commit=False)
#         new_review.user_receiver = profile_id
#         new_review.user_sender = request.user
#         new_review.save()
#     # must return to user prof
#     return redirect('detail', profile_id=profile_id)

# CARS CREATE AND UPDATE NEED TO REMOVE USER AND AUTO ADD

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
def add_listing(request):
    return render(request, 'add_listing.html')

def car_market(request):
    return render(request, 'car_market.html')

@login_required
def my_garage(request):
    user = request.user
    active_listings = Car.objects.filter(published_by=user, sold="For Sale")
    sold_history = Car.objects.filter(
        Q(published_by=user, sold="Sold") | Q(published_by=user, sold="Reserved")
    )
    reviews = Review.objects.filter(user_receiver=user)
    profile = Profile.objects.get(user=user)
    favorite_cars = profile.favorite_cars.all()
    return render(request, 'my_garage.html', {
        'profile': profile,
        'active_listings': active_listings,
        'sold_history': sold_history,
        'favorite_cars': favorite_cars,
        'reviews' : reviews,
    })

@login_required
def add_to_favorites(request, car_id):
    car = Car.objects.get(id=car_id)
    profile = Profile.objects.get(user=request.user)
    profile.favorite_cars.add(car)
    return redirect('index', car_id=car_id)

class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'content', 'user_receiver']
    success_url = '/my_garage'

    def form_valid(self, form):
        form.instance.user_sender = self.request.user
        # THIS NEEDS RECEIVING USER AS WELL ONCE PROFILE HAS
        return super().form_valid(form)
    
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
        return redirect('index')
      else:
        error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users-profile')
