from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.urls import reverse_lazy
# from bootstrap_modal_forms.generic import BSModalCreateView
# from .forms import CustomUserCreationForm




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
			return redirect('album_index')
		else:
			error_message = 'Invalid sign up - try again'
	# A bad POST or a GET request, so render signup.html with an empty form
	form = UserCreationForm()
	context = {'form': form, 'error_message': error_message}
	return render(request, 'registration/signup.html', context)


# Define the home view
def home(request):
	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

@login_required 
def albums_index(request):
	albums = Album.objects.filter(user=request.user)
	return render(request, 'albums.html', {'albums': albums})

@login_required 
def photos_index(request):
	photos = Photo.objects.all()
	return render(request, 'photos.html', {'photos': photos})

# @login_required 
# def albums_detail(request,album_id):
# 	album = Album.objects.get(id=album_id)
# 	photos_album_doesnt_have = Photo.objects.exclude(id__in = album.photos.all().values_list('id'))
# 	print (photos_album_doesnt_have)
# 	return render(request, 'albums/detail.html', {'album': album, 'photos': photos_album_doesnt_have})

# @login_required 
# def photos_detail(request, photo_id):
# 	photo = Photo.objects.get(id=photo_id)
# 	albums = Album.objects.all()
# 	# albums_photo_doesnt_have = Album.objects.exclude(photo_id__in = photo)
# 	return render(request, 'photos/detail.html', {'photo': photo, 'albums':albums})

# @login_required 
# def assoc_photo(request, album_id, photo_id):
# 	Album.objects.get(id=album_id).photos.add(photo_id)
# 	return redirect('albums_detail', album_id=album_id)

@login_required 
def albums_detail(request,album_id):
	album = Album.objects.get(id=album_id)
	# photos = Photo.objects.all()
	photos = album.photo_set.all()
	# photos_album_doesnt_have = Photo.objects.exclude(id__in = album.photos.all().values_list('id'))
	# print (photos_album_doesnt_have)
	return render(request, 'albums/detail.html', {'album': album, 'photos': photos})

@login_required 
def photos_detail(request, photo_id):
	photo = Photo.objects.get(id=photo_id)
	# albums = Album.objects.all()
	albums_photo_doesnt_have = Album.objects.exclude(id__in = photo.albums.all().values_list('id'))
	return render(request, 'photos/detail.html', {'photo': photo, 'albums': albums_photo_doesnt_have})

@login_required 
def assoc_photo(request, album_id, photo_id):
	Photo.objects.get(id=photo_id).albums.add(album_id)
	return redirect('photos_detail', photo_id=photo_id)




	

# def album_createalbum(request):
# 	# if request.method == 'POST':
# 	form = AlbumForm(request,POST)
# 	if form.is_valid():
# 		new_album = form.save(commit = False)
# 		new_album_id = album_id
# 		new_album.save()
# 	return redirect('albums', album_id = album_id)

@login_required 
def album_createalbum(request):
		# If a post request is made to this view function
		if request.method == 'POST':
				# We save the form data to a new variable
				form = AlbumForm(request.POST)
				# We make sure the data passes validations
				if form.is_valid():
						# If it does, associate album with logged in user and 
						# save it in the database
						album = form.save(commit=False)
						album.user = request.user
						album.save()
						# Redirect the user to the new album's detail page
						return redirect('albums_detail', album.id)
		else:
				# If it's a get request, load the form from forms.py
				form = AlbumForm()
		# Save the form to a new variable
		context = { 'form': form }
		# Render the album form template with the form
		return render(request, 'albums/album_form.html', context)

@login_required 
def photo_createphoto(request):
	form = PhotoForm(request,POST)
	if form.is_valid():
		new_photo = form.save(commit = False)
		new_photo_id = photo_id
		new_photo.save()
	return redirect('photos', photo_id = photo_id)


class PhotoList(LoginRequiredMixin, ListView):
		model = Photo

class PhotoDetail(LoginRequiredMixin, DetailView):
		model = Photo

class PhotoCreate(LoginRequiredMixin, CreateView):
		model = Photo
		fields = '__all__'
		success_url = '/photos/'

class PhotoUpdate(LoginRequiredMixin, UpdateView):
		model = Photo
		fields = ['name', 'description']
		success_url = '/photos/'

class PhotoDelete(LoginRequiredMixin, DeleteView):
		model = Photo
		success_url = '/photos/'

# @login_required 
# def choose_album(request, photo_id):
#   # create an instance of the model using the ModelForm and POST data
#   form = AlbumOptForm(request.POST)
#   # validate the form
#   if form.is_valid():
#     # first assign the Feeding to a photo using photo_id
#     new_feeding = form.save(commit=False)
#     new_feeding.photo_id = photo_id
#     new_feeding.save()
#   # redirect takes the name of the URL as the first arg, 
#   # and any required info as a kwarg after that
#   return redirect('detail', photo_id=photo_id)


# class SignUpView(BSModalCreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/signup.html'
#     success_message = 'Success: Sign up succeeded. You can now Log in.'
#     success_url = reverse_lazy('index')









