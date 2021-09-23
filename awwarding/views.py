from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile , Project , Rate
import datetime as dt
from .forms import CreateProfileForm , UpdateProfileForm,ProjectForm,RateForm,CreateUserForm
from django.http import HttpResponseRedirect, Http404
from .email import send_welcome_email
from django.contrib.auth import authenticate,login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.



#Creating a profile
@login_required(login_url="/accounts/login/")
def create_profile(request):
  title="Create Profile"
  current_user = request.user
  if request.method == "POST":
    form = CreateProfileForm(request.POST, request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = current_user
      profile.save()

    return HttpResponseRedirect("/")

  else:
    form = CreateProfileForm()
  return render(request, "profile/create_profile.html", {"form": form,"title": title})


# Email 
@login_required(login_url="/accounts/login/")
def email(request):
  current_user = request.user
  email = current_user.email
  name = current_user.username
  send_welcome_email(name, email)
  return redirect(create_profile)

# Display all projects 
@login_required(login_url="/accounts/login/")
def home(request):
  title="awwwards"
  date=dt.date.today()
  projects =Project.display_all_projects()
  return render(request, 'home.html', {"date":date, "title":title, "projects":projects})

#Search Project 
@login_required(login_url="/accounts/login/")
def search_project(request):
  if "project" in request.GET and request.GET["project"]:
    search_term= request.GET.get("project")
    # title="Search"
    searched_projects =Project.search_project(search_term)

    message=f"{search_term}"

    return render(request,'search_results.html', {"message":message,"searched_projects":searched_projects})
  
  else:
    
  
    return render(request, 'search_results.html')

# Display Profile 
@login_required(login_url="/accounts/login/")
def profile(request, profile_id):
  title="Profile"
  try:
    user=User.objects.get(pk=profile_id)
    profile=Profile.objects.get(user=user)
    title=profile.user.username
    projects = Project.get_user_projects(profile.id)
    project_count=projects.count()
  
  except Profile.DoesNotExist:
    raise Http404()
  return render(request, "profile/profile.html", {"profile":profile, "projects":projects, "count":project_count, "title":title})


# Update Profile
def edit_profile(request):
  current_user = request.user
  if request.method == "POST":
    form = UpdateProfileForm(request.POST, request.FILES)
    if form.is_valid():
      image = form.cleaned_data['image']
      bio  = form.cleaned_data['bio']
      email = form.cleaned_data['email']
      updated_profile = Profile.objects.get(user= current_user)
      updated_profile.image= image
      updated_profile.bio = bio
      updated_profile.email = email
      updated_profile.save()
    return redirect('profile')
  else:
    form = UpdateProfileForm()
  return render(request, 'profile/updateprofile.html', {"form": form})


# Add Project 
@login_required(login_url="/accounts/login/")
def create_project(request):
  title="Add Project"
  if request.method == "POST":
    form = ProjectForm(request.POST, request.FILES)
    current_user=request.user
    try:
      profile = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404()
    if form.is_valid():
      project = form.save(commit=False)
      project.profile = profile
      project.save()
    return redirect('home')
  else:
    form=ProjectForm()
  return render(request, 'projects/create_project.html',{"form": form, "title":title})


  # Display single project 
@login_required(login_url="/accounts/login/")
def disp_project(request,project_id):
  project=Project.objects.get(pk=project_id)
  title=project.name.title()
  ratings=Rate.objects.filter(user=request.user, project=project).first()
  rating_status=None
  if ratings is None:
    rating_status=False
  else:
    rating_status=True
  
  if request.method == 'POST':
    form=RateForm(request.POST)
    if form.is_valid():
      rate=form.save(commit=False)
      rate.user=request.user
      rate.project=project
      rate.save()
      project_ratings=Rate.objects.filter(project=project)

      design_ratings=[d.design for d in project_ratings]
      design_average=sum(design_ratings) / len(design_ratings)

      usability_ratings=[us.usability for us in project_ratings]
      usability_average = sum(usability_ratings) / len(usability_ratings)

      content_ratings = [content.content for content in project_ratings]
      content_average = sum(content_ratings) / len(content_ratings)

      score = (design_average + usability_average + content_average) / 3
      print(score)
      rate.design_average = round(design_average, 2)
      rate.usability_average = round(usability_average, 2)
      rate.content_average = round(content_average, 2)
      rate.score = round(score, 2)
      rate.save()

      return HttpResponseRedirect(request.path_info)
    
  else:
    form=RateForm()
  
  params = {
        'rating_form': form,
        'rating_status': rating_status

    }

  return render(request, 'projects/project.html', {"title": title, "project": project ,"rating_form": form, "rating_status": rating_status})

# Register
def registerPage(request):
  form = CreateUserForm(

  if request.method =='POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      user = form.cleaned_data.get('username')
      messages.success(request,'Account was created for ' + user)
      return redirect('login')



  context = {'form': form}
  return render(request, 'accounts/register.html',context)

# login
def loginPage(request):
	
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)