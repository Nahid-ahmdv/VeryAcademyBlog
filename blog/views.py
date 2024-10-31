from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Category
from .forms import NewCommentForm, PostSearchForm
from django.views.generic import ListView #'ListView' is a built-in generic class-based view provided by Django. It is designed to simplify the process of displaying a list of objects from a database model. By using 'ListView', you can quickly create views that handle common tasks such as retrieving records, paginating results, and rendering them in a template without writing repetitive code.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #we add all the scaffolding to easily create a pagination system #اینا رو برای اعمال پجینیشن ایمپورت کردیم
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
# Create your views here.  
def home(request):
    # return render(request, 'index.html')#this line is just returning 'index' page. #this is a simple view and just gonna return a template 'index.html'. and this 'request' object (The 'request' object is an instance of the 'HttpRequest' class) is used to generate the respose back to the user. so now we need to build this 'idex.html' template so it can return this page called 'index.html'. so first we need to create a 'templates' folder and then we need to tell Django where that 'templates' folder is. Django by default is looking for a folder called 'templates' that er built and inside of it we gonna have a file called 'index.html'.
    #all_posts = Post.objects.all() #This is basically doing an SQL statement that select all from the post table #by importing line 2 now we can access 'Post' model and run a simple query, so let's setup a very simple query that is gonna access all the post information in the 'Post' model. now we should pass this information to the template to output them on the page ('index.html' page).
    all_posts = Post.newmanager.all() #به این می‌گن کوئری #using custom manager that by default just retun posts that are 'published' and not 'draft'. ('models.py' line 7 and 22)
    return render(request, 'index.html', {'posts': all_posts}) #از کلید این دیکشنرب به عنوان اسمی برای صدا زدن ولیو استفاده میکنیم index.html در واقع از طریق یک دیکشنری اطلاعات را به تمپلیت‌مان پاس می‌دهیم و در تمپلیت مربوطه نیز یعنی   #In Django, when you use the 'render()' function, you typically pass a context as a dictionary. it's important to use a dictionary for the context rather than just passing a variable like 'all_posts' directly.
    # So what we've done is By line 6, we collect our data from the database in the 'Post' table and put it into 'all_posts' variable, and then obviously all the data is in this variable and then we're gonna pass it across to the template and referring to it as 'posts'. so now what we need to do is go to our HTML page 'index.html', and now basically we need to render out that information from what's been collected from the database and now it should be able to get access to our posts in our database and display them on our template.
    #what we need to do in our 'index.html' is to make a for loop (so we commented that 'Hello, world!' h1 element and writed our for loop there).
    #now after that we want to tackle the task of making titles of the posts showed on '127.0.0.1:8000/blog/' into links, so they go to the individual page for that particular post.We are going to create a new URL for this purpose, so when someone types in the name of for example the post like '127.0.0.1:8000/blog/slugofthepost/', that should take them to that post. for this purpose we gonna start with writing line 7 in 'urls.py' in 'blog' app.

def post_single(request, post): #this value here 'post' represents that value on 'urls.py' file (that 'post' in '<slug:post>/'). so now what we're going to do now is utilizing this information to make a query to the database. so in SQL terms the query that we're going to make is select all from 'Post' model (table) where slug is equal to whatever is in here ('post'). (but first we import "get_object_or_404" which is going to be utilized if the object doesn't exist the webpage is going to return 404)
    #mypost = get_object_or_404(Post, slug=post, status='published') #this query stores that individual post into variable 'mypost' and then by next line we pass it over to our template 'single.html' #select from the database 'Post', where post equals slug
    #return render(request, 'single.html', {'individualpost': mypost})  #so now we should build this 'single.html' page.
    #حالا که میخواهیم کامنت‌ها را نیز به صفحه سینگل پست‌مان اضافه کنیم و در واقع این ویو را اکستند کنیم دوباره از اول این ویو را می‌نویسیم
    mypost = get_object_or_404(Post, slug=post, status='published') #می‌ریزیم mypost ورودی تابع‌مان هست را جمع‌آوری کرده و در متغیری به نام post اطلاعات اون پستی را که اسلاگش برابر یا اسلاگ ذخیره شده در پارامتر
    previouscomments = mypost.comments.filter(status=True) #previouscomments است. تمام کامنت‌های مربوط به آن پست را جمع‌آوری و ذخیره می‌کنیم در متغییری به نام Comment تعریف شده در مدل related_name همون comments این 
    page = request.GET.get('page', 1)
    paginator = Paginator(previouscomments, 6)  #this is defining how many items (comments) you what to show on each page. so we want to divide the all comments by 3. so we're gonna show 3 items per page
    
    try:  #we're gonna try and get the comments and create the pagination
        comments = paginator.page(page)
    except PageNotAnInteger: #raised when page() is given a value that isn't an integer.
        comments = paginator.page(1)
    except EmptyPage: #raised when page() is given a valid value but no objects exist on that page.
        comments = paginator.page(paginator.num_pages)   #جایگزین کردیم و تمام comments را با previouscomments هر کدام در دو جا، عبارت beautifulmpttsingle.html و mpttsingle.html را جایگذاری کردیم و همینطور در دو تمپلیت 'comments': comments در تابع رندر مربوط به همین ویو،عبارت 'previouscomments':previouscomments برای اعمال این پجینیشن در کامنت‌های مربوط به هر صفحه از بلاگ‌مان، به جای 
    
    user_comment = None
    #so now someone types into the form(which we made for the purpose that our users could make comments on posts of our blog), their name, their email, and the content of their comment. 
    # so that's going to be sent to this function ('post_single') so what we need to do now is capture whether someone has actually made a comment. So we do that by creating an 'if' statement:
    if request.method == 'POST':  #اگه یکی کامنتی گذاشته بود
    # when we submit the form, we're making a 'POST' request. That 'POST' request is going to be sent to this function. So we're going to be able to
    # monitor whether the page was requested via 'POST' so we can run an 'if' statement to check that. So if someone has made a new comments then we're going to do something. so what we're going to do? so first of all we're going to
    # create a new variable here called 'comment_form'. so what we've done in the next line is we collected all the information from the POST data and we put it into variable 'comment_form'.
        comment_form = NewCommentForm(request.POST)  #همه اطلاعات مربوط به اون کامنت گذاشته شده را جمع‌آوری می‌کنیم
        if comment_form.is_valid(): #اگه اطلاعات ولید بود#so now we're going to check the data to make sure it's valid and we're gonna able to actually put it in our database
            user_comment = comment_form.save(commit=False)#سیوشون کن #we're gonna then start preparing and saving that data to commit to the database. you can see here we save that data we don't commit yet to the database, because we need one more piece of information. we need to associate that comment to a post so the post that they're working on currently, we need to 
            #capture that information and then we know what post to save this comment under or associate with. so we also then collect that post information so we use 'user_comment.post' equals the 'post'.
            user_comment.post = mypost
            user_comment.save()  #finally we save all that data to the database
            #so then we can now redirect them back to that particular post and that page will now be updated and will show the new post as being sunbitted or confirmed and viewable on to the page.
            return HttpResponseRedirect('/' +mypost.slug) #now the user returns to the page and we can see the comment
#just remember that this function will run every time that we go to a new page. so if someone "isn't" making a 'POST' request to this function, so 
#they're just viewing the page, then we want to do something else. we want to show the comment form so a new comment form.
        
    else:
        comment_form = NewCommentForm()
        #so what's gonna happen when the user enters the page is that we're gonna run the form and make that form available to the page. so once we've done that we need to just return all this data back to the page so that we can display it on the page. so 
        # what we return is (we send all the following information back to the front-end so that we can display it on the screen):
    return render(request, 'beautifulmpttsingle.html', {'individualpost': mypost, 'user_comment': user_comment, 'previouscomments': previouscomments,'comments': comments, 'comment_form': comment_form}) #ازشان استفاده شده single.html کلیدهای این دیکشنری همون اسم‌هایی هستند که در تمپلیت مربوطه یعنی

#we want to build a category page whereby we go to that category page and it shows us all the posts of a specific category. First of all for this purpose we need to import 'ListView' class(a class-based view) from 'django.views.generic' so that we can use class-based views. now we're gonna generate a new class-based view to extract the information from the database that's relevant to the URL. so what
#does that mean? what we want to do is when someone types in for example 'categories/F1/' it's gonna show all the F1 posts. so we're gonna be able to in our view extract the word 'F1' essentially and we're gonna use that to query the database. so let's go ahead and create a new class-based view 
class CatListView(ListView): # a class-based view (CBV) in Django using the 'ListView' to display a list of categories. This class inherits from Django's 'ListView'. This means it will inherit all the functionality of a list view, which is designed to display a list of objects from a specified model.
    # model = Category
    template_name = 'category.html'
    context_object_name = 'catlist' #This is where the data is being stored and inside of it we have got 'cat' and 'postsofacat'. #so when we pass a data back into our template we're gonna need some sort of context name for that data. So we're gonna be able to extract or collect that data on our template via the 'catlist' keyword. so that's how we can access our data on our 'category.html' page.
    #The attribute on the top line specifies the name of the variable that will be used in the template context to refer to the list of categories. Instead of using the default name (object_list), it will be accessible as 'catlist' in your template.
    # def get_queryset(self) -> QuerySet[Any]: #برای بازپس‌گرفتن اینستنس‌های یک مدل از دیتابیس
    #     return super().get_queryset()
    '''
    Overriding 'get_queryset()':
    The method 'def get_queryset(self) -> QuerySet[Any]:' is defined to customize the queryset that will be used to retrieve objects for this view.
    Inside this method, 'return super().get_queryset()' calls the parent class's (ListView) implementation of 'get_queryset()'. This means it will return all instances of the Category model by default.
    Purpose of Overriding 'get_queryset()':
    Customization: While this implementation simply calls the parent method, overriding 'get_queryset()' allows you to customize which objects are retrieved based on specific criteria. For example, you might want to filter categories based on certain conditions or order them in a specific way.
    Dynamic Querysets: You can add logic here to return different querysets based on user input, request parameters, or other dynamic factors.
    
    '-> QuerySet[Any]':
    The arrow (->) signifies that the method will return a value of a specified type. 
    'QuerySet':
    QuerySet is a class provided by Django that represents a collection of database queries. It is used to retrieve objects from the database in a way that allows for filtering, ordering, and other operations.
    By specifying QuerySet, you are indicating that the method will return a Django QuerySet object.
    The 'Any' indicates that the QuerySet can contain instances of any model or data type.
    '''
    def get_queryset(self): 
        content = {
            'cat': self.kwargs['category'], #This retrieves the value of 'category' from the URL parameters. For example, if your URL is '/categories/sports/', 'self.kwargs['category']' would return the string 'sports'.
            'postsofacat' : Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')#In Django, when filtering querysets based on related models, you must use the double underscore (__) syntax to traverse relationships. When you want to filter based on fields of a related model, you use the double underscore syntax. This allows Django to understand that you're referring to a field in a related model. #it means "filter posts where the related category's name matches the given value."
        }
        return content #within this 'content' we're gonna reference or collect the information within it via keywords 'cat' and 'postsofacat'
    '''
    In the context of Django class-based views (CBVs), 'self' refers to the instance of the class that is currently being used.
    In Django, when a request comes in, various useful attributes are set on 'self', including:
        self.request: The HTTP request object.
        self.args: Positional arguments from the URL.
        self.kwargs: Keyword arguments from the URL.
    Example in Context:
        Suppose you have a URL pattern defined as follows:
            path('categories/<str:category>/', CategoryPostListView.as_view(), name='category-posts')

        When a request is made to '/categories/sports/', Django creates an instance of 'CategoryPostListView'. Inside this instance, 'self.kwargs' would be populated with ('self.kwargs' means you're accessing the 'kwargs' attribute of the current instance of the view class.):
            {'category': 'sports'}

        Therefore, when you write 'self.kwargs['category']', you're accessing the value associated with the key 'category' in that instance's 'kwargs' (the 'kwargs' attribute of that instance).
    Summary
    'self' is a reference to the current instance of the class.
    It allows you to access instance attributes and methods, including 'kwargs'.
    In Django CBVs, it helps manage data passed through URLs and facilitates dynamic behavior based on user input
    '''



#بالای هر صفحه‌ی بلاگمان داشته باشیم که کتگوری‌های موجود را به ما نشان دهد. برای این منظور یک ویو می‌نویسیم navbar در drop-down menu حالا می‌خواهیم یک 
def Category_navbar(request):
    categorynavbar = Category.objects.exclude(name='default') #This is our query that's gonna query all the categories from the 'Category' table and then output everything put it into 'categorynavbar' variable, but it's going to exclude 'default' category. #we exclude 'default' category 'cause we don't want it to be in our drop-down list
    content = {
        "category_list": categorynavbar,
    }
    return content

def post_search(request):
    form = PostSearchForm() #we created a form (put the form inside of the variable 'form' and then we're sending it to the template)
    h = '' #we created a new variable and it's just empty. we filled it up shortly.
    cgry=''
    results = []
    query = Q()
    #کپچر کنیم AJAX request نوشتم و الان می‌خواهیم اطلاعات را از AJAXsearch.html در فایل an AJAX request in jQuery خط بعدی را بلافاصله پس از نوشتن  
    #first of all we're gonna put this inside of an 'if', so we're gonna check to see if there is actually a request that's been made:
    if request.POST.get('action') == 'post':  #l'm basically just checking to see if that's available. there's a few different ways that we can check if we're actually receiving an AJAX request. this is just simply one way. 
     #so if we do have a request then we're gonna do something,first we 're gonna store the data (that's been typed in from the user)
        search_string = str(request.POST.get('ss')) #so that's the data now captured. now we want to do sth with it (perform a query).
        if search_string is not None:
            search_string = Post.objects.filter( #we're gonna query the Post table (we output the data from the database into the variable 'search_string'so now this variable has all the data that's returned from a database). we probably don't want to return hundred items in a drop-down list as a search suggestion. so we can just type in a number here and just limit the amount that gets returned from the database.
                title__contains=search_string)[:4] #we're utilizing JavaScript and Python (of course by default they can't talk to each other so we need to prepare this data so it can be utilized by JavaScript, what we're gonna need to do now is serialize the data that's returned from the database, so we need to import the serializers)
            data = serializers.serialize('json', list(search_string), fields =('id', 'title', 'slug'))      #so we created a new variable called 'data' and we're gonna serialize the data that gets returned from the database (we store the output of the serialization) and we want to serialize in 'json', and then we define what data we want to serialize and what fields we want to get serialized (we probably don't want to return all the data from the database, we're not gonna need the content to be displayed in the drop-down list.)
            #so we just need to return this 'data' to the search page (AJAXsearch.html). so we're gonna return this 'data' in a json response (because we've serialized it as Json in the 'data' ) so we're gonna need to import the 'JsonResponse'
            return JsonResponse({'search_string': data})   #we're gonna send it back as reference to 'search_string' (that is the reference point to send the data back to, that's how we're gonna collect the data or where it's gonna be stored when we send it back to the search and what we're gonna send back is all the data inside of that(the data that we serialized))
            #است ذخیره میشود json که function در صورت موفقت‌آمیز بودن در ورودی AJAXsearch.html ایی که داریم برمی‌گرداریم به صفحه سرچ‌مان یعنی همانdata دقت کنید این



    if 'h' in request.GET: #we're gonna check to see if any data exists in the get request.If the data does exist in the get request (the 'q' data) then we're gonna process this information
        form = PostSearchForm(request.GET)
        if form.is_valid():
            h = form.cleaned_data['h'] #once the form has been checked the data is available from the 'cleaned_data'
            cgry = form.cleaned_data['cgry']  #cgry is gonna hold a value (the id of that category like 1,2,..) it is not gonna hold the category name. now now we need to use this data inside of our query. so we want to query the title contains 'h' and then what we want to do first of all is set up a new filter
            # results = Post.objects.filter(title__contains = h) #now we set up a simple query, we called this 'results' (a variable called 'results') and basically we need to query the 'Post' model and the we say 'objects' and we use a filter. so what we want to filter from the model is to look for all the data where the title contains 'q' (remember 'q' is what someone's typed into the search input).
            #we can use 'contain' assuming that someone's gonna type in single word or words that are grouped together to return the title or the post. Or we can utilize for example 
            #once we start moving to a postgres database we then have more facilities available to make much more complicated search.
            # results = Post.objects.filter(category=cgry).filter(title__contains = h)  #استفاده کنیم cgry این همان کوئری هست که گفتیم باید توش از اطلاعات کپچرشده در
    # return render(request, 'search.html', {'form': form, 'h':h, 'results':results})   #so next up we now have the form, we want to pass that now, we're gonna set up a http response, so we just return the form to the new page that we're gonna build called 'search.html', and then we're gonna send the form data to that template. حالا باید این تمپلیت را بسازیم
            #اگر بخواهیم فیلد مربوط به انتخاب کتگوری را اختیاری کنیم دیگر کوئری ساخته شده در دو خط بالا کار نمیکند به همان دلیلی که در فایل مربوط به فرمز توضیح دادم
            #so we're gonna modulize our query based upon different parameters
            if cgry is not None:
                query &= Q(category=cgry)
            if h is not None:
                query &= Q(title__contains=h)
            results = Post.objects.filter(query)
    return render(request, 'FAJAXsearch.html', {'form': form, 'h':h, 'results':results})