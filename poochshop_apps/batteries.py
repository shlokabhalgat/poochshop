from .models import PetFormData, VendorData


def my_function(*form_details, request):
    dict = form_details.values()
    value_iterator = iter(dict)
    first_value = next(value_iterator)
    if PetFormData.objects.filter(auth_user_email=request.user):
        nm = first_value.get("name")
        print(nm)
        breed = first_value.get("breed")
        print(breed)
        age = first_value.get("age")
        print(age)