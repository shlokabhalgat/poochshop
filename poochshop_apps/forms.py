from django import forms

from .models import PetFormData

AMOUNT_CHOICES = [
    ('Choose From Below',(
    ('LT100', 'less than 1000'),
    ('BET1000TO3000', '₹1000-₹3000'),
    ('BET3000TO5000', '₹3000-₹5000'),
    ('MT500', 'more than ₹5000'),))
]

SERVICE_CHOICES = [
    ('pet_grooming', 'Pet Grooming'),
    ('pet_sitting', 'Pet Sitting'), ('vet', 'Vet/At home vet'), ('pet_hostel', 'Pet hostel'),
    ('food_delivery', 'Home-made food delivery'),
    ('pet_taxi', 'Pet Taxi'), ('pet_party', 'Pet Party')
]


class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Example- Momo'
        , 'style': 'border : none;','class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Example- 2'
        , 'style': 'border : none;','class': 'form-control'}))
    breed = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Example- Labrador'
        , 'style': 'border : none;','class': 'form-control'}))
    amount_spent = forms.ChoiceField(choices=AMOUNT_CHOICES)
    pincode = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Example- 411037'
        , 'style': 'border : none;','class': 'form-control'}))
    services_required = forms.MultipleChoiceField(choices=SERVICE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
        'style': 'border : none;'}), required=False)

    class Meta:
        model = PetFormData
        fields = ['name', 'age', 'breed', 'amount_spent', 'pincode', 'services_required']
        labels = {'name': 'Enter Pets name', 'age': 'Enter their age','amount_spent': 'Select from below'}
        error_messages = {'name': {'required': 'Naam likhna zaroori hai'}}
        widgets = {
            'amount_spent': forms.Select(attrs={'class': 'bootstrap-select','style': 'width:20px'}),
        }

    def clean_services_required(self):
        return ','.join(self.cleaned_data['services_required'])


class UpdatePetForm(forms.Form):
    u_name = forms.CharField(max_length=100, required=False)
    u_age = forms.IntegerField(required=False)
    u_breed = forms.CharField(max_length=100, required=False)
    u_pincode = forms.CharField(max_length=15, required=False)

    class Meta:
        model = PetFormData
        fields = ['name', 'age', 'breed', 'pincode']
