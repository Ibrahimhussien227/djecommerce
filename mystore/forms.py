from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Comment, Item

PAYMENT_CHOICES = (
    ('V', 'Visa'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St', 'class': 'form-control'
    }))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite', 'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    # so you can choose just one in a time = RadioSelect
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'discount_price', 'category', 'label', 'label_text', 'description', 'image']


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'discount_price', 'category', 'label', 'label_text', 'slug', 'description', 'image']
