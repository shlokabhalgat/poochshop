import graphene
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from graphene_django import DjangoObjectType
from .models import VendorData, MongoPetData


class Vendor(MongoengineObjectType):  # VendorType- Type declaration for GraphQL
    class Meta:
        model = VendorData


class PetFormType(MongoengineObjectType):
    class Meta:
        model = MongoPetData


class Query(graphene.ObjectType):
    all_vendors = graphene.List(Vendor, pin=graphene.String())
    all_pets = graphene.List(PetFormType)

    def resolve_all_vendors(self, info, pin):
        print(info)
        print(pin)
        return VendorData.objects.filter(Pincode=pin)

    def resolve_all_pets(self, info):
        return MongoPetData.objects.all()


class ProfileMutation(graphene.Mutation):
    petform = graphene.Field(PetFormType)  # Connection between model and the field we want to update through GraqhQL

    class Arguments:
        mid = graphene.Int()
        name = graphene.String(required=False)
        age = graphene.Int(required=False)
        breed = graphene.String(required=False)
        pincode = graphene.String(required=False)

    @classmethod
    def mutate(cls, root, info, mid, **kwargs):
        petform = MongoPetData.objects.get(auth_user_email_id=mid)
        petform.name = kwargs.get('name', petform.name)
        petform.age = kwargs.get('age', petform.age)
        petform.pincode = kwargs.get('pincode', petform.pincode)
        petform.breed = kwargs.get('breed', petform.breed)
        petform.save()
        print(info)
        return ProfileMutation(petform=petform)


class Mutation(graphene.ObjectType):
    updateProfile = ProfileMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
