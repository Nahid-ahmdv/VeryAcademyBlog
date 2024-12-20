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
from mptt.admin import MPTTModelAdmin




@admin.register(models.Post) #This decorator registers the 'Post' model with the Django admin site, allowing it to be managed through the admin interface.
class AuthorAdmin(admin.ModelAdmin): #This defines a custom admin class for the 'Post' model, inheriting from 'admin.ModelAdmin'. This allows for customization of how the model is displayed in the admin.
    list_display = ('title','id', 'category','status', 'slug', 'author')
    prepopulated_fields = {"slug":("title",),}#پر می‌شود slug وقتی یک پست بخواهیم درست کنیم، به محض وارد کردن تایتلش خودبه‌خود فیلد مربوط به #This attribute allows automatic generation of certain fields based on other fields. Here, it automatically populates the 'slug' field based on the value entered in the 'title' field.

# @admin.register(models.Comment) #This decorator registers the 'Comment' model with the Django admin site.
# class CommentAdmin(admin.ModelAdmin):  #This defines a custom admin class for managing comments.
#     list_display = ("post", "name", "email", "publish", "status") #This specifies which fields should be visible in the comment list view.
#     list_filter = ("status", "publish") #This attribute adds filters in the right sidebar of the comment list view, allowing you to filter comments by their status and publish date.
#     search_fields = ("name", "email", "content") #This allows you to search for comments based on specific fields. Here, you can search by name, email, or content of the comment.
# #مدل‌هامون رو نوشتیم و بعد اومدیم اینجا در ادمین پنل‌مون رجیسترشون کردیم و سر و شکل دادیم بهشون و بعد حالا باید بریم توی ویوهامون models.py ما اول رفتیم در فایل 
# #we now need to head over to the view and start thinking about how we're gonna integrate this within our system so that the user of our website can actually make comments.but before that let's create a new file called 'forms.py' and develop a simple form in that file.

#نوشتیم، رجیستریشنی متفاوت با اون مدل قبلی که برای کامنت داشتیم و در بالا نوشتیم، می‌نویسیم MPTT جدیدی که با استفاده از الگوریتم Comment برای مدل 
#مون نوشتیمComment در اپ بلاگ پاک کردیم و بعد ریجیستریشن جدید زیر رو برای مدلmigrations اول فایل مربوط به دیتابیس‌مون رو رفتیم پاک کردیم، بعد تمام مایگریشن‌ها رو رفتیم در فولدر
#را ایمپورت کنیم MPTTModelAdmin ابتدا باید
# admin.site.register(models.Comment, MPTTModelAdmin)  #we want to use the 'Comment' model and we want to apply the 'MPTTModelAdmin'. after that because we haven't included MPTT yet in our application, we go to 'mysite' folder which is the main directory for this project, go to 'settings.py' and add 'mptt' to our 'INSTALLED_APPS" list. this is gonna allow us to access the model within our admin area\admin panel. now at this point we actually have a model that's using MPTT. Now we just need to apply this hierarcical structure to our template so that we can utilize MPTT
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment  # Adjust import based on your project structure

class CommentAdmin(MPTTModelAdmin):
    list_display = ('name', 'post', 'publish', 'status')  # Include fields you want to display
    list_filter = ('post', 'status')  # Add filters for easier navigation
    search_fields = ('name', 'content')  # Enable search functionality

    def post(self, obj):
        return obj.post.title  # Display the title of the related post

    post.admin_order_field = 'post'  # Allow ordering by post title in admin

# Register the Comment model with the custom admin class
admin.site.register(Comment, CommentAdmin)


# admin.site.register(models.Category)  
# یا
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):  # Fixed the class name
    list_display = ("name", "get_posts")  # Use a method to get posts

    def get_posts(self, obj):
        return obj.posts.count()  # Count of related posts  #مون استPost تعریف شده در مدل related_name همون posts این
    get_posts.short_description = 'Number of Posts'  #اسم ستون مربوطه در ادمین پنل را مشخص می‌کند# Optional: Set a short description for the column
# یا
# @admin.register(models.Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "get_posts")  # Use a method to get posts

#     def get_posts(self, obj):
#         # Get all related posts
#         posts = obj.posts.all()
#         return ", ".join([post.title for post in posts])  # Join titles into a single string

#     get_posts.short_description = 'Related Posts'  # Optional: Set a short description for the column