from django.urls import path
from . import views
app_name = 'blog'  #same as the 'namespace' in 'urls.py' in 'mysite' app (line 21)

urlpatterns = [
    path('', views.home, name='homepage'), #by this line I expect that after typing in '127.0.0.1:8000/blog/' we redirect to the homepage. now we need to connect this URL view ("views.home") to the actual view in 'views.py' file in 'blog' app, so let's do that by creating a simple view which basically just going to return a simle template named 'index.html'.
    path('<slug:post>/', views.post_single, name='post_single') #'<slug:post>': The angle brackets < > indicate that this part of the URL is a variable that will be captured and passed to the view. 'slug': This is a path converter that specifies the type of variable being captured. 'post': This is the name of the variable that will hold the value captured from the URL. In this case, it represents a specific post identified by its slug. we take that information and pass it over to the view called 'post_single'. so we need to create a new view called 'post_single'. so let's do it!
]
