from .models import PetFormData, VendorData,MongoPetData

def requestAuthUserData(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }
    return auth0user,userdata


def returnAuthEmailID(request):
    data = returnPetName(request)
    pet_name = data['pet_name']
    all_objs = MongoPetData.objects.all()
    for obj in all_objs:
        if obj.name == pet_name:
            mid = obj.auth_user_email_id
    return mid


def returnPetName(request):
    form_deats = PetFormData.objects.filter(auth_user_email=request.user).values_list('pincode', 'name', 'breed', 'age')
    pet_form_values = form_deats.values()
    value_iterator = iter(pet_form_values)
    first_value = next(value_iterator)
    if PetFormData.objects.filter(auth_user_email=request.user):
        pet_name = first_value.get("name")
        pet_age = first_value.get("age")
        pet_breed = first_value.get("breed")
        pet_pincode = first_value.get("pincode")
    return {'pet_name':pet_name, 'pet_age':pet_age,'pet_breed':pet_breed, 'pet_pincode': pet_pincode}


