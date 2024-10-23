from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post
from .forms import NewCommentForm
# Create your views here.
def home(request):
    # return render(request, 'index.html')#this line is just returning 'index' page. #this is a simple view and just gonna return a template 'index.html'. and this 'request' object (The 'request' object is an instance of the 'HttpRequest' class) is used to generate the respose back to the user. so now we need to build this 'idex.html' template so it can return this page called 'index.html'. so first we need to create a 'templates' folder and then we need to tell Django where that 'templates' folder is. Django by default is looking for a folder called 'templates' that er built and inside of it we gonna have a file called 'index.html'.
    #all_posts = Post.objects.all() #This is basically doing an SQL statement that select all from the post table #by importing line 2 now we can access 'Post' model and run a simple query, so let's setup a very simple query that is gonna access all the post information in the 'Post' model. now we should pass this information to the template to output them on the page ('index.html' page).
    all_posts = Post.newmanager.all() #به این می‌گن کوئری #using custom manager that by default just retun posts that are 'published' and not 'draft'. ('models.py' line 7 and 22)
    return render(request, 'index.html', {'posts': all_posts}) #در واقع از طریق یک دیکشنری اطلاعات را به تمپلیت‌مان پاس می‌دهیم   #In Django, when you use the 'render()' function, you typically pass a context as a dictionary. it's important to use a dictionary for the context rather than just passing a variable like 'all_posts' directly.
    # So what we've done is By line 6, we collect our data from the database in the 'Post' table and put it into 'all_posts' variable, and then obviously all the data is in this variable and then we're gonna pass it across to the template and referring to it as 'posts'. so now what we need to do is go to our HTML page 'index.html', and now basically we need to render out that information from what's been collected from the database and now it should be able to get access to our posts in our database and display them on our template.
    #what we need to do in our 'index.html' is to make a for loop (so we commented that 'Hello, world!' h1 element and writed our for loop there).
    #now after that we want to tackle the task of making titles of the posts showed on '127.0.0.1:8000/blog/' into links, so they go to the individual page for that particular post.We are going to create a new URL for this purpose, so when someone types in the name of for example the post like '127.0.0.1:8000/blog/slugofthepost/', that should take them to that post. for this purpose we gonna start with writing line 7 in 'urls.py' in 'blog' app.

def post_single(request, post): #this value here 'post' represents that value on 'urls.py' file (that 'post' in '<slug:post>/'). so now what we're going to do now is utilizing this information to make a query to the database. so in SQL terms the query that we're going to make is select all from 'Post' model (table) where slug is equal to whatever is in here ('post'). (but first we import "get_object_or_404" which is going to be utilized if the object doesn't exist the webpage is going to return 404)
    #mypost = get_object_or_404(Post, slug=post, status='published') #this query stores that individual post into variable 'mypost' and then by next line we pass it over to our template 'single.html' #select from the database 'Post', where post equals slug
    #return render(request, 'single.html', {'individualpost': mypost})  #so now we should build this 'single.html' page.
    #حالا که میخواهیم کامنت‌ها را نیز به صفحه سینگل پست‌مان اضافه کنیم و در واقع این ویو را اکستند کنیم دوباره از اول این ویو را می‌نویسیم
    mypost = get_object_or_404(Post, slug=post, status='published')
    previouscomments = mypost.comments.filter(status=True)
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
    return render(request, 'single.html', {'individualpost': mypost, 'user_comment': user_comment, 'previouscomments': previouscomments, 'comment_form': comment_form}) 