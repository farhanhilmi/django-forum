from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
    
class CreateInForum(ModelForm):
    class Meta:
        model = forum
        fields = "__all__"
        exclude = ['profile','num_comment']

    # def __init__(self, *args, **kwargs):
    #     self._profile = kwargs.pop('profile')
    #     super(CreateInForum, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     inst = super(CreateInForum, self).save(commit=False)
    #     inst.profile = self._profile
    #     if commit:
    #         inst.save()
    #         self.save_m2m()

    #     return inst

class updateCommentForm(ModelForm):
    class Meta:
        model = forum
        fields = ['num_comment']
    
class CreateInDiscussion(ModelForm):
    class Meta:
        model= Discussion
        fields = "__all__"
        exclude = ['forum','user','like']

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']
