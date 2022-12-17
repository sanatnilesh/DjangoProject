from django import forms
from django.contrib.auth.forms import UserCreationForm

from myaoo.models import Order, Client, Product, User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']

    client = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Client.objects.all(), to_field_name="username",
                                    label='Client name')
    product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('id'), to_field_name="name")
    num_units = forms.IntegerField(label='Quantity')


class InterestForm(forms.Form):
    INT_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=INT_CHOICES)
    quantity = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
