from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from poochshop_apps.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('petform/', views.showformdata),
    path(
        "graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="graphql"
    ),
    path('updateprofile/', views.updateprofile),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
