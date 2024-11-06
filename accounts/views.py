from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login #به محض اینکه یوزرمان که رجیستر کرده روی لینکی که به ایمیلش ارسال شده کلیک می‌کند، لاگ‌این می‌شود یعنی اکانتش اکتیو می‌شود برای همین این را ایمپورت کردیم
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm
from .tokens import account_activation_token  # the class in this file is gonna create our token

# Create your views here.
@login_required  #this is gonna protect this page (profile page) so that only logged in users can access this view (or template) or this section of our application
def profile(request):
    return render(request,
                  'accounts/profile.html', #we're just returning the template for this view
                  {'section': 'profile'}) #This is a context dictionary that is passed to the template. In this case, it includes a key 'section' with the value 'profile', which can be used in the template for rendering or logic purposes.
#برای لاگ‌این ویو ننوشتیم و از لاگ‌این ساخته شده در خود جنگو استفاده کردیم

@login_required #you're gonna need to be logged in to use this view so again we protect it by via this decorator.
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)#if we receive a 'POST' request from this 'edit', we're gonna collect the user information and then check to see if it's valid. If it is valid then we're gonna try and save it. else, we just gonna show the form.
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form})



#we’re gonna send our url to this view (accounts_register) so every time someone visits this url we’re gonna check to make sure if they have registered, if they have, then we’re gonna be sending a request method for “POST”; if they haven’t registered or sent a POST request then we ‘re just gonna show them the RegistrationForm.
def accounts_register(request): #It takes an HTTP request object as an argument. This view function will handle the registration logic for new users.
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST) #This line creates an instance of 'RegistrationForm', passing in the data from the request (request.POST). The 'RegistrationForm' should be a Django form class that handles user input for registration, including fields like username, email, and password.#capturing the 'RegistrationForm' information inside of the variable called 'registerForm'. so we get grab all the information from there and put it into this variable.
        if registerForm.is_valid(): #This checks if the submitted form data is valid according to the rules defined in the 'RegistrationForm'. If the form is valid, it proceeds to save the user; otherwise, it will render the form with error messages.
            user = registerForm.save(commit=False) #This saves a new user instance but does not commit it to the database yet ('commit=False'). This allows you to modify certain fields (like setting 'is_active') before saving it permanently.
            '''Setting User Attributes'''
            user.email = registerForm.cleaned_data['email'] #you explicitly set the user's email attribute using cleaned data from the form. The cleaned_data dictionary contains validated data from the form fields.
            user.set_password(registerForm.cleaned_data['password'])#This method hashes the password provided by the user before saving it. It ensures that plain-text passwords are not stored in the database, enhancing security.
            user.is_active = False #by default, when someone registers we're not activting them, which means that they can't log in just yet. we're gonna send them an email, they're gonna click on that email and then once they have linked back to us via that email, 
                                   #we're then gonna create another method which is going to activate that functionality (منظورش فعال شدن تیک گزینه اکتیوت هست. وارد ادمین اریا شد و وارد گزینه یوزرز و وارد اسم ادمین شد اون پایین سه تا گزینه هست که بای دیفالت تیکشون زده شده و اون گزینه اول که اکتیوت هست رو داره می‌گه برای یوزرهامون دیفالتش رو فالس می‌ذاریم که یعنی این گزینه تیک نخورده باشه تا زمانی کهیوزر از راه اون لینکی که براش ایمیل کردیم وارد سایتمون بشه)
            '''
            This sets the 'is_active' attribute of the user to False. 
            By doing this, you are preventing the user from logging in until they activate their account via an email link (which is common in many registration flows).
            '''
            user.save() #Finally, this line commits the user instance to the database, creating a new record for this user.
            current_site = get_current_site(request)
            subject = 'Activate your Account' #This sets the subject line for the activation email. It informs the user that they need to activate their account.
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # we need to set out and create a unique id that identifies that particular user. Because what we want to do is obviously capture when someone clicks on that link that sends them back to our site to activate them we want to know what their user id is or what user they are so we're gonna send out in this code here and the user primary key so when they click on that link we're gonna be able to identify what user is actually trying to activate.
                #آماده سازی می‌کنیم account_activation_email.html در url با خط بالا در واقع داریم یوزر دات پرایمرکی یا همون آیدی یوزر را برای استفاده شدن در
                'token': account_activation_token.make_token(user),  #این متد برای ما یک توکن یونیک جدید می‌سازد که برای هر یوزر یونیک است و به کمک آن می‌توان تشخیص داد که یوزر ما رجیستر کرده است یا نه
            })
            '''
            Purpose: This line generates the content of the activation email by rendering a template called 'account_activation_email.html'. The 'render_to_string' function takes two arguments:
            1)The path to the template file.
            2)A context dictionary containing data to be passed into the template.
            In this case, the context includes:
            user: The newly registered user instance.
            domain: The domain of the current site (to create a link for activation).
            uid: A URL-safe base64 encoded version of the user's primary key (ID), which will be used in the activation link.
            token: A unique token generated for this user using a custom token generator (account_activation_token). This token is used to verify that the user requesting activation is legitimate.
            '''
            user.email_user(subject=subject, message=message)
            '''
            Purpose: This method sends an email to the user. The 'email_user' method is a built-in method on Django's 'User' model that simplifies sending emails. It takes two arguments:
                    subject: The subject line of the email.
                    message: The body of the email (which contains a link for account activation). 
            '''
            return HttpResponse('registered succesfully and activation email sent')
        '''
        After sending the activation email, this line returns an HTTP response indicating that registration was successful and that an activation email has been sent to the user's email address. 
        This response will be displayed in the browser.
        '''
    else: #If the request method is not POST, the function will render a blank registration form.
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})

def activate(request, uidb64, token): #این توکن و یوآیدی همون‌هایی هست که در فایل یوآرالز در لینک یوآرال وجود دارد و الان داریم پاسشون می‌دهیم به ویو
    try:
        uid = force_text(urlsafe_base64_decode(uidb64)) #try and capture the uid, decode that.
        user = User.objects.get(pk=uid) #try and capture the user id, so we know what account to activate.
        #حالا بعد از اینکه یوآیدی و یوزرآیدی را گرفتیم سراغ مرحله بعدی می‌رویم
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): #چک می‌کنیم ببینیم آیا یوزر وجود دارد یا خیر
        user = None #This will happen if we receive an error from the data that's being linked from (User model), so if the data is incorrect in the email from the url link then this is gonna return an error.
    #if everything is successful:
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login') # and if you are logged in remember we have got a piece of JavaScript which will take you to the profile page.
    else:
        return render(request, 'registration/activation_invalid.html')
    
@login_required
def delete_user(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False #we're gonna disable the account not delete it and then save the information.
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')