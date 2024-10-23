# from django.contrib import admin #This line imports the 'admin' module from Django's built-in 'contrib' package. The 'admin' module provides functionalities to create an admin interface for your models.

# # Register your models here.
# # from .models import Post
# # admin.site.register(Post) #This line registers the 'Post' model with the Django admin site. By doing this, Django will automatically create a user interface for managing 'Post' instances (i.e., creating, reading, updating, and deleting posts) in the admin panel.

# from . import models #is a relative import statement that allows you to access the 'models' module located in the same package as the current module.

# class Authoradmin(admin.ModelAdmin):  #و نویسنده‌شون نمایش داده بشه Slug و title لیست اون پست‌های ایجاد شده همراه با Admin Panel این کلاس رو برای این تعریف کردیم که در 
#     list_display = ('title','status', 'slug', 'author') # we define some Metadata here (data about data)

# admin.site.register(models.Post, Authoradmin) #نوشته شده را بتوانیم ببینیم Posts که زیرش نواری به نام BLOG این یک خط اساسا همونی هست که باعث میشه وقتی به پنل ادمین میریم نواری با نام 



#برای اضافه کردن کامنتها در جلسه سوم کلا بالا رو کامنت کردیم و به جاش پایینی ها رو نوشتیم

from django.contrib import admin  #This imports the Django admin module, which allows you to create an admin interface for your models. پس درستش ادمین اینترفیس هست نه ادمین پنل فکر کنم
# # Register your models here.
from . import models 

@admin.register(models.Post) #This decorator registers the 'Post' model with the Django admin site, allowing it to be managed through the admin interface.
class Authoradmin(admin.ModelAdmin): #This defines a custom admin class for the 'Post' model, inheriting from 'admin.ModelAdmin'. This allows for customization of how the model is displayed in the admin.
    list_display = ('title','status', 'slug', 'author')
    prepopulated_fields = {"slug":("title",),}#پر می‌شود slug وقتی یک پست بخواهیم درست کنیم، به محض وارد کردن تایتلش خودبه‌خود فیلد مربوط به #This attribute allows automatic generation of certain fields based on other fields. Here, it automatically populates the 'slug' field based on the value entered in the 'title' field.

@admin.register(models.Comment) #This decorator registers the 'Comment' model with the Django admin site.
class CommentAdmin(admin.ModelAdmin):  #This defines a custom admin class for managing comments.
    list_display = ("post", "name", "email", "publish", "status") #This specifies which fields should be visible in the comment list view.
    list_filter = ("status", "publish") #This attribute adds filters in the right sidebar of the comment list view, allowing you to filter comments by their status and publish date.
    search_fields = ("name", "email", "content") #This allows you to search for comments based on specific fields. Here, you can search by name, email, or content of the comment.
#مدل‌هامون رو نوشتیم و بعد اومدیم اینجا در ادمین پنل‌مون رجیسترشون کردیم و سر و شکل دادیم بهشون و بعد حالا باید بریم توی ویوهامون models.py ما اول رفتیم در فایل 
#we now need to head over to the view and start thinking about how we're gonna integrate this within our system so that the user of our website can actually make comments.but before that let's create a new file called 'forms.py' and develop a simple form in that file.