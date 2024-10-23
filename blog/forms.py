from django import forms #by this we brought in 'forms' module from Django framework.
from .models import Comment #by this we can grap the data from 'Comment' table.

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')           #These fields gonna be generated into inputs in our form.
        widgets = {                                      #we don't have direct access to the form, because remember the form is being generated automatically so there's no way of me other than injecting som code into the form, of me actually formatting that form in a Bootstrap way. so we use this widget option to add some styling to our form.
            "name": forms.TextInput(attrs={"class" : "col-sm-12"}),
            "email": forms.EmailInput(attrs={"class": "col-sm-12"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        } #by this "widgets" we're just going to inject the class into the input forms from the form that Django builds. now we can go ahead and start developing our view.   (views.py رفتیم توی فایل)