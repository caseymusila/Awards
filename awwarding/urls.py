from django.urls import path,include,re_path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('search_project/',views.search_project,name = 'search_project')
    re_path('profile/(?P<profile_id>\d+)',views.profile,name = 'profile'),
    path('create_project/',views.create_project,name = 'create_project'),
    re_path('edit_profile/<profile_id>',views.edit_profile,name='edit_profile'),
    path('email/', views.email, name='email'),
    path('disp_project/<project_id>',views.disp_project, name='disp_project'),
    
]


# disp_project,name = 'disp_project'),