from django.contrib import admin #This line imports the 'admin' module from Django's built-in 'contrib' package. The 'admin' module provides functionalities to create an admin interface for your models.

# Register your models here.
# from .models import Post
# admin.site.register(Post) #This line registers the 'Post' model with the Django admin site. By doing this, Django will automatically create a user interface for managing 'Post' instances (i.e., creating, reading, updating, and deleting posts) in the admin panel.

from . import models #is a relative import statement that allows you to access the 'models' module located in the same package as the current module.

class Authoradmin(admin.ModelAdmin):  #و نویسنده‌شون نمایش داده بشه Slug و title لیست اون پست‌های ایجاد شده همراه با Admin Panel این کلاس رو برای این تعریف کردیم که در 
    list_display = ('title','status', 'slug', 'author') # we define some Metadata here (data about data)

admin.site.register(models.Post, Authoradmin)