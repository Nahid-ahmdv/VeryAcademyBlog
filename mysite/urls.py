"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include #we added 'include' because of line 21
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('account/', include('django.contrib.auth.urls')), #so as Django already has the tools and facilities for us to build an authentication system upon, all we need to do is activate them in a very simplistic way. first we need to add a new path, here we basically just gonna hook into the authentication space and we're gonna do that by creating a new path called 'account/' and we're gonna include the django contrib of urls. this essentially creates eight new urls that we can utilize to start thinking about creating a login system for our application. so if we go to '127.0.0.1:8000/account/login/' we can see these eight urls in the error page. so we're gonna be working with these eight urls and then we're gonna override them because we want to create our own templates and particularly we want to potentially extend some of the facilities that these offer. 
    #and for each of these eight urls behind the scenes there is also a view. So in actual fact all we might need to do to build a really simplistic login system is just add some templates to some of these urls and everything else would just work.
    #templates in Django authentication by default is looking for a folder called 'registration' (we can change that of course we don't have to use 'registration' we will look at how we can do that later) so we build this folder first called it 'templates' and inside of it we build another folder called 'registration' and this is gonna be the folder that holds the templates for our authentication system after that we create a new file called 'login.html' inside of it, now if we refresh '127.0.0.1:8000/account/login/' it isn't gonna work just yet, there's one final step that we need to do so we need to head over to the 'settings.py' inside of it we have an area called TEMPLATES and we should specify this directory in my application so we fill the 'DIR' in 'DIR' we define where we want our 'templates' folder to reside 
    #so in this case we're gonna add 'os.path.join(BASE_DIR, 'templates') in 'DIR'.
    #just notice that there was no need for us to manually create a url here like 'account/login/', we're just hooking on to the authentication system built-in.
    path('', include('blog.urls', namespace='blog')), #this line is for connecting up to 'urls.py' file in 'blog' app. It specifies that any URL starting with 'blog/' should be handled according to the rules defined in the included URL configuration. 'namespace='blog'' in your URL configuration helps prevent naming collisions between URL patterns across different apps. 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #it just tell Django where the 'media' folder is so that we can utilize it on the localhost

'''
path('account/', ...):
 This part defines a URL pattern. It specifies that any URL starting with 'account/' will be handled by the URLs defined in the included module.
 For example, if a user accesses '/account/login/', this pattern will match.
include('django.contrib.auth.urls'):
 The 'include()' function imports another URL configuration from the Django authentication framework(system) (django.contrib.auth).
 This module provides built-in views for handling user authentication, including login, logout, password change, and password reset.

What URLs Are Created?
 By including 'django.contrib.auth.urls', Django automatically creates several (eight) URL patterns for you. Specifically, it sets up the following URLs:
    Login URL: '/account/login/'
        Displays the login form.
    Logout URL: '/account/logout/'
        Logs the user out and redirects them to a specified page.
    Password Change URL: '/account/password_change/'
        Allows users to change their passwords.
    Password Change Done URL: '/account/password_change/done/'
        Displays a message confirming that the password has been changed successfully.
    Password Reset URL: '/account/password_reset/'
        Initiates the password reset process by sending an email with a reset link.
    Password Reset Done URL: '/account/password_reset/done/'
        Displays a message confirming that an email has been sent with instructions to reset the password.
    Password Reset Confirm URL: '/account/reset/<uidb64>/<token>/'
        Confirms the password reset using a unique identifier and token.
    Password Reset Complete URL: '/account/reset/done/'
        Displays a message confirming that the password has been successfully reset.
'''
