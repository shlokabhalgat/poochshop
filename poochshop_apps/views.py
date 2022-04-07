from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from urllib.parse import urlencode
import poochshop_apps.batteries
from .forms import PetForm, UpdatePetForm
from .models import PetFormData, VendorData, MongoPetData
from poochshop_apps import schema
import graphene
from django.contrib.sessions.models import Session
from python_graphql_client import GraphqlClient


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(showformdata)
    else:
        return render(request, 'index.html')


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }
    form_deats = PetFormData.objects.filter(auth_user_email=request.user).values_list('pincode', 'name', 'breed', 'age')
    pet_form_values = form_deats.values()
    value_iterator = iter(pet_form_values)
    first_value = next(value_iterator)
    if PetFormData.objects.filter(auth_user_email=request.user):
        vendor_pincode = first_value.get("pincode")
    print(vendor_pincode)
    print("Auth0user", auth0user)
    print("Request.user", request.user)
    print("USER", user)
    # client = GraphqlClient(endpoint="http://127.0.0.1:8000/graphql/")
    query = """
            query ($pincode: String)
            {
              allVendors (pin:$pincode)
              {
                VendorName,
                Socials,
                WaysOfBooking,
                PhoneNumber,
                Email,
                Address,
                Pincode,
                City,
                Charges,
              }
            }
        """
    endpoint = "http://127.0.0.1:8000/graphql/"
    if PetFormData.objects.filter(auth_user_email=request.user):
        variables = {"pincode": vendor_pincode}
        r = requests.post(endpoint, json={"query": query, "variables": variables})
        if r.status_code == 200:
            q_v_d = json.dumps(r.json(), indent=2)
            query_vendors_dict = json.loads(q_v_d)
            print(type(q_v_d))  # str
            print(type(query_vendors_dict))  # dict
            print(list(query_vendors_dict))  # op- ['data'] lists all keys in dict
            query_vendors_list = query_vendors_dict['data'].get('allVendors')
            print(query_vendors_list)  # returns dict inside dict
            new_dict = {}
            for item in query_vendors_list:
                name = item['VendorName']
                new_dict[name] = item
            print(new_dict)
            # for dictionary in query_vendors_list:
            #     try:
            # v_nm = dictionary['VendorName']
            # print(v_nm)
            # print(v_socials)
            # print(v_booking)
            # print(v_ph)
            # print(v_email)
            # print(v_add)
            # print(v_pin)
            # print(v_city)
            # print(v_charges)
            # except KeyError:
            #     pass
        else:
            raise Exception(f"Query failed to run with a {r.status_code}.")
        # data = client.execute(query=query, variables=variables)
        # print(data)
        # print("req.user", user)  bshloks
        # print(userdata)
        nm = first_value.get("name")
        print(nm)
        breed = first_value.get("breed")
        print(breed)
        age = first_value.get("age")
        print(age)
    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'name': nm,
        'breed': breed,
        'age': age,
        'new_dict': new_dict
    }
                  )


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)


@login_required
def showformdata(request):
    # session_key = request.session.session_key
    # session = Session.objects.get(session_key=session_key)
    # session_data = session.get_decoded()
    # user = User.objects.get(id=uid)
    form = PetForm(request.POST)
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }
    if PetFormData.objects.filter(auth_user_email=request.user).exists():
        # print(session_data)
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            if form.is_valid():
                if request.user.is_authenticated:
                    user = request.user
                nm = form.cleaned_data['name']
                age = form.cleaned_data['age']
                breed = form.cleaned_data['breed']
                am_sp = form.cleaned_data['amount_spent']
                pin = form.cleaned_data['pincode']
                ser_req = form.cleaned_data['services_required']
                model_pet_data = PetFormData(name=nm, age=age, breed=breed, amount_spent=am_sp, pincode=pin,
                                             services_required=ser_req, auth_user_email=user)
                model_pet_data.save()
                print(user)
                return redirect('/dashboard')
        else:
            form = PetForm()
        return render(request, 'petform.html',
                      {'form': form, 'auth0User': auth0user, 'userdata': json.dumps(userdata, indent=4),
                       })


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

@login_required
def updateprofile(request):
    form = UpdatePetForm(request.POST)
    mid = returnAuthEmailID(request)
    data = returnPetName(request)
    if request.method == 'POST':
        if form.is_valid():
            if request.user.is_authenticated:
                if not form.cleaned_data['u_name']:
                    nm = data['pet_name']
                else:
                    nm = request.POST.get('u_name')
                if not form.cleaned_data['u_age']:
                    age = data['pet_age']
                else:
                    age = request.POST.get('u_age')
                if not form.cleaned_data['u_breed']:
                    breed = data['pet_breed']
                else:
                    breed = request.POST.get('u_breed')
                if not form.cleaned_data['u_pincode']:
                    pincode = data['pet_pincode']
                else:
                    pincode = request.POST.get('u_pincode')
                print("Name from form", nm)
                # print("auth_user_email_id from Mongodb",mid)
                # print(name)
                print(age)
                print(breed)
                print(pincode)
                print(mid)
                # client = GraphqlClient(endpoint="http://127.0.0.1:8000/graphql/")
                # data = client.execute(query=query, variables=variables)
                # print(data)
                endpoint = "http://127.0.0.1:8000/graphql/"
                variables = {"mid": mid, "name": nm, "age": age, "breed": breed, "pincode": pincode}
                query = """
                         mutation($mid: Int!, $name: String, $age: Int, $breed: String, $pincode: String){
                             updateProfile(mid:$mid,name:$name,age:$age,breed:$breed,pincode:$pincode){
                                petform{
                                    name
                                    age
                                    breed
                                    Id
                                    authUserEmailId
                                }
                            }
                        }
                         """
                r = requests.post(endpoint, json={"query": query, "variables": variables})
                if r.status_code == 200:
                    res = json.dumps(r.json(), indent=2)
                    print(res)
                else:
                    raise Exception(f"Query failed to run with a {r.status_code}.")

    else:
        form = UpdatePetForm()

    return render(request, 'updateprofile.html', {'form': form})
