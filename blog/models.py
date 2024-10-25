from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #when we made a new Django project it has a default database for users (a table or model called User) which we see once we start building a superuser and log in to the admin area.
from django.urls import reverse #وصل کنیم، از این تابع کمک می‌گیریم http://127.0.0.1:8000/blog/ به تایتل آن پست در صفحه ('single.html') پست‌ها را میبینیم، با کلیک روی تایتل هر پست وارد صفحه‌ای منحصر به همان پست شویم. برای این منظور به جای اینکه تک تک و به صورت دستی بیاییم لینک مربوط به صفحه محصربه‌فرد هر پست را http://127.0.0.1:8000/blog/ دلیل ایمپورت کردن این تابع این بود که ما می‌خواستیم وقتی از طریق این صفحه
#The top line imports the 'reverse()' function from Django’s 'urls' module. The 'reverse()' function is used to generate URLs based on the name of the view rather than hardcoding the URL paths.


# Create your models here.
def user_directory_path(instance, filename):
    return 'post_images/{0}/{1}'.format(instance.id, filename)  #so when we make a new post, the post is given an id, so that is something that happens behind the scenes because as you notice we haven't actually set an id field in our 'Post' model. 
# so there's an id primary key that's utilized on this table (Post) that we're not seeing in 'Post' table, but l make that visible surely. 
# So l'm gonna use that id (that unique id to every single post) and that's going to build a folder with that id({0}) and then also after that it's gonna be the file name ({1}) and that will place nicely inside of that folder. 
# and now l just need to reference this function inside of 'cardimage' field of our model 'Post'.



class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
#The first task for us is to develop a small database for our blog app. so we're gonna need to store posts so we're gonna make some posts and then we're gonna display those on the page, so that data needs to be stored in a database. so in here (models.py) basically we're gonna develop a database within this file. so how we do this is by extending or sub-classing an existing class in Django and we're gonna build a new class which is essentially a new table in our database.
class Post(models.Model):  #this is a new table (in the database) called Post. This is a model and each model in python is a python class that subclasses (models.Model), in other words: each model inherits from 'models.Model', which is the base class for all Django models. now we need to think about the attributes of this class. we just need to ask ourselves what do we need to store about each individual post: its "title", "url", "when it was published (publish date)", "who built the post (author)", "its content", and "status". ('status' here is referring to the fact that when we build a new post we might want to just keep it in a draft until we're ready to finish it, maybe we need to come back and finish it later and of course some posts are gnna be published so I need a way of determining whether a post is published or not to determine whether I should display it on the website).
    class NewManager(models.Manager):  #This is a custom manager 
        def get_queryset(self):
            return super().get_queryset().filter(status='published') #we're gonna create a kind of a custom query set
    options = (       #This tuple defines the possible status options for a post. Each tuple element consists of two values: The first value is the actual value stored in the database (e.g., 'draft' or 'published'). The second value is a human-readable name for that status (e.g., 'Draft' or 'Published').
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    #Fields:
    title = models.CharField(max_length=250) #Title Field. Type: 'CharField'. Purpose: Stores the title of the post.
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=3, related_name="posts")#ساختیم،هم جزو همین کتگوری قرار خواهند گرفت Category است. از طرفی تمام پست‌هایی هم که تا الان، قبل از ایجاد مدلdefault آیدی کتگوری دیفالت که 3 هست را بهش دادیم پس هر وقت پست جدیدی درست کنیم کتگوری دیفالتش #"PROTECT":Forbid the deletion of the referenced object. In this case, it means this is gonna forbid the deletion of our categories. This is gonna avoid people being able to delete any of our categories.    # we can't make a new post unless we give it a category.
    excerpt = models.TextField(null=True)
    # cardimage = models.ImageField(upload_to='post_images/', blank=True, null=True)
    cardimage = models.ImageField(upload_to=user_directory_path, blank=True, null=True)  #so now when l add a new image it should be uploaded to a directory that matches the id of that particular post and the name of the image.
    slug = models.SlugField(max_length=250, unique_for_date='publish_date') #Slug Field. Type: 'SlugField'. Purpose: Stores a URL-friendly version of the title, often used in URLs. #For example, if you have a blog post titled "Understanding Django Models," the slug might be 'understanding-django-models'. This makes the URL more user-friendly and easier to remember, such as:'example.com/posts/understanding-django-models #The 'unique_for_date='publish'' argument adds a significant constraint: This constraint guarantees that no two posts can have the same slug on the same publish date. For instance, if you publish two articles on the same day with similar titles, this prevents both from having the same slug. Benefits of Using Slugs: Readability: Slugs make URLs easier to read and understand for users. SEO(search engine optimization) Friendly: Search engines often favor URLs that include keywords relevant to the content. Avoiding IDs: Instead of using numeric IDs in URLs (which are not meaningful to users), slugs provide context about the content.
    publish_date = models.DateTimeField(default=timezone.now) #Publish Date Field. Type: 'DateTimeField'. Purpose: Stores the date and time when the post is published.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')#we created a foreignkey to the table 'User' #we're gonna store the username of that user who built the post into this field using foreignkey. #Author Field. Type: 'ForeignKey'. Purpose: Creates a relationship with the 'User' model, indicating who authored the post. On Delete Behavior: If the user is deleted, all their related posts will also be deleted (CASCADE). Related Name: Allows access to all posts by a user through 'user_instance.blog_posts'. The term 'related name' in Django refers to a convenient way to access related objects from the reverse side of a foreign key relationship. In your 'Post' model, this line indicates that each 'Post' is linked to a 'User' (the author). The 'related_name='blog_posts'' allows you to access all posts written by a specific user in a more intuitive manner.
    content = models.TextField() #Content Field. Type: 'TextField'. Purpose: Stores the main content of the blog post. This field can hold a large amount of text.
    status = models.CharField(max_length=10, choices=options, default='draft') #Status Field. Type: 'CharField'. Purpose: Indicates whether the post is in draft or published status.Choices: Limited to values defined in the options tuple. Default Value: Set to 'draft' when a post is created.
    objects = models.Manager() #default manager
    newmanager = NewManager()  #custom manager
    
    def __str__(self):  #for returning human-readable titles for our 'Post' instances (posts) in the admin area here we've set up this string conversion to return the title of the post.
        return self.title
    class Meta:  #we want to define the ordering of our list of 'Post' instances (or simply our posts). we want to order it by publish date.
        # ordering = ('publish_date',) #اگه این خط رو بنویسیم ترتیب لیست اینجوری می‌شه که پستی که اول نوشتیم بالای لیست قرار می‌گیره و پست‌های بعدی زیرش. اما ما می‌خواهیم اونی که اخیرا نوشتیم و جدیدتره اون بالا باشه. پس خط بعدی رو می‌نویسیم و اینو کامنت می‌کنیم
        ordering = ('-publish_date',)
    def get_absolute_url(self): #This method is typically included in a Django model and is used to return the canonical URL for an instance of that model. It allows you to easily retrieve the URL for an object without needing to know its specific path.
        return reverse('blog:post_single', args=[self.slug])
    '''
    reverse('blog:post_single', ...):
      The 'reverse()' function takes the name of the URL pattern as its first argument. In this case, 'blog:post_single' refers to a URL pattern defined in your 'urls.py' file under the namespace 'blog' named 'post_single'. This pattern should correspond to a view that handles displaying a single blog post.
    args=[self.slug]:
      The 'args' parameter is used to pass positional arguments to the URL. Here, 'self.slug' refers to the slug attribute of the model instance (e.g., a unique identifier for the blog post). This slug will be inserted into the URL where needed, allowing Django to construct the correct path for that specific post.
    example:When you call 'some_post.get_absolute_url()', where 'some_post' is an instance of 'Post' model, it will return a URL like '/blog/my-first-post/', assuming the slug for that post is 'my-first-post'.
    '''
#The next step now is to commit this model to our project (so actually building this table called 'Post'). 
# We do that by utilizing the Windows PowerShell. First we going to prepare the changes that we've made by running this command "python manage.py makemigrations" after pressing Enter we receive "No changes detected" because the first thing we need to do is to tell Django that we've created a new app called 'blog'. 
# so we need to go to 'settings.py' which is located in 'mysite' app and in 'INSTALLED_APPS' list and write "'blog'," and then again run that command in PowerShell and this time by pressing Enter changes are detected and we receive "Migrations for 'blog':blog\migrations\0001_initial.py - Create model Post" so now 'Post' table has been created on database. 
# now we can commit to that table. so we do that by typing "python manage.py migrate", that's applied all the changes that we've made and in the background now our table has been made and then we can move on to the next stage.
#now l think what would be useful now is to actually see this table. We can do that by accessing the Django admin area. so we access the admin area by first creating a superuser! so we run this command "python manage.py createsuperuser" then we must fill some fields like:
#Username (leave blank to use 'surfacelaptop'): admin
#Email address: a@a.com
#Password: admin
#by pressing Enter we receive: 'Superuser created successfully'. so what that means now, is if ....well l need to run the server first, so after that l can access the admin panel. using "python manage.py runserver" for running the server. then to get to the admin panel, we just type in "127.0.0.1:8000/admin" and it takes me to the admin panel. now l'm in 'Django administration" area.
#What we need to do next is now registering our table ("Post") so that it appears here in the administration area so that we can manage the table and add new things to the table, So for this purpose we need to get to 'admin.py' file in our 'blog' folder, there we can register our models so that we can access them on the administration area. (as far as l understand,the meaning of "registering a model" is that it appears on the Django administration area).(line 4 and 5 in 'admin.py' in 'blog' app)

'''
Summery till now: 
we've created a new app called 'blog' then gone into 'settings.py' file in 'mysite' app and added the name of our new app to 'INSTALLED_APPS' and after that we created a new database (model)
called 'Post' in 'models.py' then gone into the 'admin.py' of our 'blog' app to register it, then obviously we needed to apply that (using command "makemigrations") and then committed to
it (using command "migrate") and once we done all of those steps, we registered this 'Post' table and so it bocomes available in the Django administration area. Then we look at how we want to display the list of posts on Django administration or adding some metadata in 'admin.py' file.
First we created a superuser to get to the admin area\Django administration (using the command 'creatsuperuser'), then we ran the server and through '127.0.0.1:8000/admin/' we got into admin panel.
'''

#now we gonna create some instances of our 'Post' class\table\model\database through admin area.


#و بعد دوباره سرور را ران می‌کنیم to actually commit that change را وارد می‌کنیم migrate را بزنیم تا به جنگو اعلام کنیم تغییراتی را که ایجاد کردیم و بعد کامند مربوط به makemigrations به‌منظور متوقف کردن سرور، بعدش کامند مربوط به Ctrl + c حواست باشه هر تغییری که در مدل‌هامون می‌دیم حتما برای عملی شدنش باید بعد از فشردن کلیدهای

#خط 7 و 9 و 12 admin.py حالا می‌خواهیم اون لیست پست‌های ادمین پلن را کمی تغییر دهیم تا علاوه بر نشون دادن تایتل هر پست، یکسری اطلاعات دیگه‌‌ی هر پست هم نشون بده. برای این منظور می‌ریم توی فایل

#بعد از تکمیل کردن خلاصه بالا حالا به ادامه کار می‌پردازیم:
#The next thing is for us to retrieve this data (posts that we made) from the database ('Posts' model) and then to view it on the website. So before we go ahead and build webpages
#and display the information from the database (models) on our webpages and so on for our blog, let's just understand a little bit about what's happening here
#so we have got our browser window, we type in the URL to where we want to go, and that then basically sends a message to the Django (a request),
#so what happens is that Django captures that request and it first of all looks for the URL that's associated to the URL that's been typed in, so 
#that's really the first check and it needs that information then to direct the request to the right place so in our 'mysite' folder we have 'urls.py' file and in this file
#you can see that it says there's a path here and we got 'admin/' that take us to the admin page (admin panel). So basically that's controlling what's gonna happen when someone types in 'admin/', and you
#can see 'admin.site.urls' is the instruction of what to do. So what we're gonna do is we're gonna go into our 'blog' app and then we're  going to make a new file called 'urls.py' and we're
#gonna set up some URLs associated to this 'blog' app. So what we're gonna first do is basically add a new line of code in 'urls.py' in 'mysite' (line 21) which is gonna connect this URL page to that one in 'blog' app.
#so not only Django will look from "'urls.py' in 'mysite' app" for URLs (associated to what someone's typed in), it will now also look there ('urls.py' in 'blog' app).
#then we also associate a URL to a view so this view (information) will then go over to the view page. 'views.py' in 'blog' app, this is the glue really, l think it is the glue to this model.
#in the 'views.py' we're gonna define what happens and what we need to collect a few things. So we need to collect a template to put the data on (so that's gonna be our HTML and CSS) ,and then obviously we're gonna need some data (so it's gonna connect also to the model and collect some data), all of them put together in the view and then that goes back to the browser and then we display all the information in the browser. So in summery you're going to create a URL, then build your view, and then a template and if you need more tables, data in your model.
#so let's go back and now create a webpage that shows all the posts from our database ('Post' model). So let's start off by connecting up your 'urls.py' in your 'blog' app to your 'urls.py' in your 'mysite' app.(line 21)
#127.0.0.1:8000/blog/ ساختیم که از طریق این یوآرال index.html قبل از عملی کردن خط بالا صرفا برای امتحان یک
#بهش دسترسی پیدا میکردیم و هلو ورد برامون نمایش میداد. بعدش خط بعدی را آقاهه گفت
#now let's work out how to get information from our database and put it onto our page. so let's go back to our 'views.py'.(for this purpose, we extend our 'home' view. first of all we're gonna need to collect all the data from the database which in this case means select all the posts from 'Post' table. so first of all l need to make sure that this page (i think he means our HTML template) can access my model so we need to import "from .models import Post" in 'views.py' file, by importing that now we can access 'Post' model and run a simple query, so let's setup a very simple query that is access all the post information in the 'Post' model)

#now we need to store information about comments that users enter. So we need a new database\table\model, and we're gonna need to make a connection from 'Comment' table to the 'Post' table. The reason why that is, because we want to store the comments inside of this table but we need some sort of reference so that we know what comments are associated to what posts. So we're gonna create a foreign key. we're gonna create a new field called 'post' and create a new foreign key, so we're gonna connect this to the 'Post' model.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50) #our comment system is gonna need the user to type in a comment, a name of some sort and an email and then they can type in the actual comment (content) so we're gonna store that too inside of a textfield.
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True) #when we want to order the comments we can order them by published date.
    status = models.BooleanField(default=True) #you might later on want to be able to disable some of the comments or you might want to filter or administrate some of the comments that are inappropriate so instead of just deleting them we could put them in some sort of status area so we could change the status from True to False. S here if the status is True then the comment is live and if this boolean Field is False then the status iS False and the comment won't be shown to the users
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f"Comment by {self.name}"
    

#we need to create a ForeignKey between the 'Post' table and the 'Category' table. But the problem we got here is that we've already got data within our 'Post' table so if l now were to create a ForeignKey between the 'Post' and the 'Category' then that could cause potential problems.
#It just makes it more difficult to make this model because there has to be something inside of the 'Post'and there has to be something inside the category and at the moment there are no categories so we can't really make that link between the 'Post' table and the 'Category' table. so because we're working on a live database
#in this case it's probably best for us to just migrate and set the 'Category' table first, then build some categories and then go ahead and create our ForeignKey between the 'Post' table and the 'Category' table. so let's go ahead and go to the admin.py and make our new model available in the admin area\admin panel(127.0.0.1:8000/admin/) so that we can add some categories.
#so we go to 'admin.py' and write 'admin.site.register(models.Category)' and after that we should use these commands respectively: 'python manage.py makemigrations' then 'python manage.py migrate', after running the server now we can see 'Category' section in admin area. so let's go and build some categories. so first we're going to set a new category called default. so that's just a default category for any post that will be generated.maybe we forget to add it to a category or we are not sure yet, so we're gonna need to add it to something so therefore we creates a default category.
#so that all posts by default will be part of the 'default' category and then we can change it as we wish.
#so now we create one category and we can now create a ForeignKey between the 'Post' table and the 'Category' table. after that we added some more categories. now we need to create some sort of category page so then l could have a drop-down and click on each of the categories and then it shows me all the posts that are connected to that category. so for this purpose we need to create a new view, so let's go to 'views.py'. now we create a CBV named 'CatListView', after that we go into 'urls.py' 'cause we need to make a path for this view, so let's go to 'urls.py'. 
#after we  set the path in 'urls.py' now that's done! so we run the server now. now if we insert this URL address "http://127.0.0.1:8000/categories/Default/" we encounter this error "emplateDoesNotExist at /categories/Default/", which means we should create our 'category.html'. so let's create a template for this to capture the information from our view 'CatListView'. so just remember that from our view we are sending back to our template. after that we create a drop-down menu for our categories in our navbar using 'Category_navbar' view. after creating "Category_navbar" view because we want it to be shown in navbar of all the pages, we go to 'settings.py' in 'mysite' app and in 'TEMPLATES' we can see 'context_processors' and we just need to add our view "Category_navbar" to that, so now this view gonna be available throughout our whole project.
#after that we go to 'base.html' and make a drop-down menu there in the nav element using Bootstrap drop-down fcility tools.
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name