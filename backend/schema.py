import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from users.models import CustomUser
from django.db.models import Sum
from graphql_jwt.shortcuts import get_token
from django.http import HttpResponse

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    global_sign_in_count = graphene.Int()

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_global_sign_in_count(self, info):
        return CustomUser.objects.aggregate(global_count=Sum('sign_in_count'))['global_count']

class Register(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = CustomUser.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        # Increment sign-in count
        user.sign_in_count += 1
        user.save()

        token = get_token(user)
        return Register(user=user, token=token)

class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = CustomUser.objects.get(username=username)
        if not user.check_password(password):
            raise Exception('Invalid credentials')
        
        # Increment sign-in count
        user.sign_in_count += 1
        user.save()

        token = get_token(user)
        return Login(user=user, token=token)

class SignOut(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        response = HttpResponse()
        response.delete_cookie('JWT')
        return SignOut(success=True)

class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    sign_out = SignOut.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
