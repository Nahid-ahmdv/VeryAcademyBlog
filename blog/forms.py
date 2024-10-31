from django import forms #by this we brought in 'forms' module from Django framework.
from .models import Comment,Category #by this we can grap the data from 'Comment' table.
from mptt.forms import TreeNodeChoiceField  #we use 'MPTT' to create a multi-layered comments feature.


class NewCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.fields['parent'].widget = forms.HiddenInput() #Hidden Input: By setting 'self.fields['parent'].widget = forms.HiddenInput()', you ensure that the field will not be displayed on the page at all, rather than just being visually hidden.
        self.fields['parent'].widget.attrs.update({'class':'d-none'}) #این دی‌نان هم یک کلاس بوت استرپ هست که المان رو از ویو حذف می‌کنه و در صفحه سایت دیگه نشونش نمی‌ده  #    یا این یا خط بالایی. برای نمایش ندادن فیلد پرنت در هنگام کامنت گذاری
        self.fields['parent'].label = ''  
        self.fields['parent'].required = False
    parent = TreeNodeChoiceField(queryset=Comment.objects.all()) #'parent' was foreignkey in our 'Comment' model in 'models.py'
    class Meta:
        model = Comment #I created a form by utilizing the 'Comment' database.
        fields = ('name', 'parent', 'email', 'content')           #These fields gonna be generated into inputs in our form. Django turned those fields into input fields that we can utilize on the template.
        widgets = {                                      #we don't have direct access to the form, because remember the form is being generated automatically so there's no way of me other than injecting som code into the form, of me actually formatting that form in a Bootstrap way. so we use this widget option to add some styling to our form.
            "name": forms.TextInput(attrs={"class" : "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        } #by this "widgets" we're just going to inject the class into the input forms from the form that Django builds. now we can go ahead and start developing our view.   (views.py رفتیم توی فایل)

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)   
    
# ارث‌بری می‌کنیمforms.Form ارث‌بری کنیم و در کلاس متا هم اسم آن مدلی که قرار است فرم را براساسش بسازیم، می‌نویسیم. در مقابل اما اگر فرم‌مان مستقل است از forms.ModelForm اگه فرمی که می‌خواهیم بسازیم وابسته به مدل خاصی باشد، باید از 
#'forms.ModelForm': Directly tied to a specific model. You specify which model to use in the Meta class, and it automatically generates fields based on that model.
#'forms.Form': Does not have any direct association with a model. You define all fields manually, and it can be used for various purposes (e.g., search forms, login forms).
#let's go ahead and create a new form for our search.
class PostSearchForm(forms.Form):
    h = forms.CharField()  #we're not gonna build a form, we're gonna utilize Django and tell Django what type of form we want and we do that by basically set  up this variable 'q' (query).Basically we're gonna say from 'forms' we just want to build a character field input. we just told Django that we want to make a new form and we want one input and that's just gonna be a character field. (ساختیم post_search و ویوای به نام views.py رفتیم توی فایل)
    cgry = forms.ModelChoiceField(queryset=Category.objects.exclude(name='default').order_by('name'))#next up we want to add the drop-down facility so not only do we want the user to be able to search for a word, we want to be able to let them select a category we want to search within. 'ModelChoiceField' is gonna create a drop-down choice field.
    #l want to query my 'Category' model and select all the information order it by name and l want to use all the category names as the drop-down items. 
    #for example you wanted to make your own choices, set up the choices here (FRUIT_CHOICES) you can create a label and a widget and use the 'choices'
            # FRUIT_CHOICES = [
            #     ('orange', 'Oranges'),
            #     ('cantaloupe', 'Cantaloupes'),
            #     ('mango', 'Mangoes'),
            #     ('honeydew', 'Honeydews'),
            # ]
            # d = forms.CharField(label='what is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))
    # 127.0.0.1:8000/search/ این خط بالا را که نوشتیم الان در بلاگمان اگه به آدرس
    #مراجعه کنیم، یک دراپ داون می‌بینیم وقتی خب اطلاعات را فعلا نمی‌توان از این دراپ داون کپچر کرد
    #قدم بعدی فراهم کردن مقدماتی برای کپچر کردن اطلاعات از این دراپ داون است
    #The option field created so obviously what I want to do now is capture that information and utilize it in a query. let's go back to the views and in 'post_search' l want to make a new variable for that so l want to capture that and save it in there."cgry=''".
    def __init__(self, *args, **kwargs): #we're gonna return some arguments back
        super().__init__(*args, **kwargs)
        self.fields['cgry'].required = False #we're gonna select the field 'h' and put it as unrequired
        #کار نمیکند سه خط بالا چون در ویومان چنین کوئری‌ای داریم
        #results = Post.objects.filter(category=cgry).filter(title__contains = h)
         #یعنی در ویومان گفتیم که ما پست‌های مربوط به یک کتگوری خاص را می‌خواهیم و وقتی کتگوری را مشخص نکنیم میره دنبال پست‌هایی می‌گرده که جزو هیچ کتگوری‌ای نیستن و خب ما همچین پست‌هایی اصلا نداریم
         #When we don't select anything in categories this is returning nothing so what this is querying is looking for all the posts where the category equals nothing.
         #Q objects allow us to perform complex lookups in our queries.
        # self.fields['cgry'].label = ''
        self.fields['cgry'].label = 'Category'
        self.fields['h'].label = 'Search For'
        self.fields['h'].widget.attrs.update(
            {'class': 'form-control menudd'})
        self.fields['h'].widget.attrs.update(
            {'data-toggle': 'dropdown'})