from django import forms #by this we brought in 'forms' module from Django framework.
from .models import Comment #by this we can grap the data from 'Comment' table.
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.fields['parent'].widget = forms.HiddenInput() #Hidden Input: By setting 'self.fields['parent'].widget = forms.HiddenInput()', you ensure that the field will not be displayed on the page at all, rather than just being visually hidden.
        self.fields['parent'].widget.attrs.update({'class':'d-none'}) #این دی‌نان هم یک کلاس بوت استرپ هست که المان رو از ویو حذف می‌کنه و در صفحه سایت دیگه نشونش نمی‌ده  #    یا این یا خط بالایی. برای نمایش ندادن فیلد پرنت در هنگام کامنت گذاری
        self.fields['parent'].label = ''  
        self.fields['parent'].required = False
    parent = TreeNodeChoiceField(queryset=Comment.objects.all()) #'parent' was foreignkey in our 'Comment' model in 'models.py'
    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')           #These fields gonna be generated into inputs in our form.
        widgets = {                                      #we don't have direct access to the form, because remember the form is being generated automatically so there's no way of me other than injecting som code into the form, of me actually formatting that form in a Bootstrap way. so we use this widget option to add some styling to our form.
            "name": forms.TextInput(attrs={"class" : "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        } #by this "widgets" we're just going to inject the class into the input forms from the form that Django builds. now we can go ahead and start developing our view.   (views.py رفتیم توی فایل)