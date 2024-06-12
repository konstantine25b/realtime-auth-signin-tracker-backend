from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True)))),
    path('api/token/', obtain_auth_token),
]