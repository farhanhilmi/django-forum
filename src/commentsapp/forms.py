from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
    
class CreateInForum(ModelForm):
    class Meta:
        model= forum
        fields = "__all__"
    
class CreateInDiscussion(ModelForm):
    class Meta:
        model= Discussion
        fields = "__all__"

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']