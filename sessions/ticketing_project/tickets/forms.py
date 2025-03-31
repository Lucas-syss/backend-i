from django import forms
from tickets.models import User

class AgentCreationForm(forms.ModelForm):
    """Form to create a new agent."""

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'agent'
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  
        user.save()
        return user
    
class CustomerSignUpForm(forms.ModelForm):
    """Form to allow customers to sign up."""

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user.save()
        return user