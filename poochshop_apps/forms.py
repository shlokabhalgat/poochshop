from django import forms

from .models import PetFormData

AMOUNT_CHOICES = [
    ('LT100', 'less than 1000'),
    ('BET1000TO3000', '₹1000-₹3000'),
    ('BET3000TO5000', '₹3000-₹5000'),
    ('MT500', 'more than ₹5000')
]

SERVICE_CHOICES = [
    ('pet_grooming', 'Pet Grooming'),
    ('pet_sitting', 'Pet Sitting'), ('vet', 'Vet/At home vet'), ('pet_hostel', 'Pet hostel'),
    ('food_delivery', 'Home-made food delivery'),
    ('pet_taxi', 'Pet Taxi'), ('pet_party', 'Pet Party')
]


class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    breed = forms.CharField(max_length=100)
    amount_spent = forms.ChoiceField(choices=AMOUNT_CHOICES, widget=forms.RadioSelect())
    pincode = forms.CharField(max_length=15)
    services_required = forms.MultipleChoiceField(choices=SERVICE_CHOICES, widget=forms.CheckboxSelectMultiple,
                                                  required=False)

    class Meta:
        model = PetFormData
        fields = ['name', 'age', 'breed', 'amount_spent', 'pincode', 'services_required']
        labels = {'name': 'Enter Pets name', 'age': 'Enter their age'}
        error_messages = {'name': {'required': 'Naam likhna zaroori hai'}}

    def clean_services_required(self):
        return ','.join(self.cleaned_data['services_required'])


class UpdatePetForm(forms.Form):
    u_name = forms.CharField(max_length=100,required=False)
    u_age = forms.IntegerField(required=False)
    u_breed = forms.CharField(max_length=100, required=False)
    u_pincode = forms.CharField(max_length=15, required=False)

    class Meta:
        model = PetFormData
        fields = ['name', 'age', 'breed', 'pincode']