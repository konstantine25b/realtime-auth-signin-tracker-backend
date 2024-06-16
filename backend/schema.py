import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token, create_refresh_token
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.db.models import Sum
from django.http import HttpResponse
from graphql_jwt import ObtainJSONWebToken, Refresh
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.consumers import notify_global_sign_in_count
from users.consumers import notify_winner


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    global_sign_in_count = graphene.Int()
    winner = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_global_sign_in_count(self, info):
        return CustomUser.objects.aggregate(global_count=Sum('sign_in_count'))['global_count']
    
    def resolve_winner(self, info):
        winner = CustomUser.objects.filter(winner=True).first()
        return winner

class Register(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
   
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        if len(password) < 8:
            raise Exception('Password must be at least 8 characters long')

        user = CustomUser.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        # Increment sign-in count
        user.sign_in_count += 1
        user.save()
        
        global_count = CustomUser.objects.aggregate(global_count=Sum('sign_in_count'))['global_count']
        if global_count == 5:
            user.winner = True
            user.save()
            notify_winner()  # Notify winner

        notify_global_sign_in_count(global_count)  # Notify global sign-in count

        # Obtain JWT token and refresh token for the newly registered user
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        
        return Register(user=user, token=token, refresh_token=refresh_token)

class Login(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = CustomUser.objects.get(username=username)
        if not user.check_password(password):
            raise Exception('Invalid credentials')
        
        user.sign_in_count += 1
        user.save()
        
        global_count = CustomUser.objects.aggregate(global_count=Sum('sign_in_count'))['global_count']
        if global_count == 5:
            user.winner = True
            user.save()
            notify_winner()
            

        notify_global_sign_in_count(global_count)  # Notify global sign-in count


        token = get_token(user)
        refresh_token = create_refresh_token(user)
        
        return Login(user=user, token=token, refresh_token=refresh_token)

class ChangePassword(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        new_password = graphene.String(required=True)  
        
    def mutate(self, info, username, password, new_password):
        if len(new_password) < 8:
            raise Exception('Password must be at least 8 characters long')

        user = CustomUser.objects.get(username=username)
        if not user.check_password(password):
            raise Exception('Invalid credentials')

        user.set_password(new_password)
        user.save()
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return ChangePassword(user=user, success=True,token=token, refresh_token=refresh_token)
class SignOut(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        response = HttpResponse()
        response.delete_cookie('JWT')
        # Optionally, you can also delete the refresh token here if needed
        return SignOut(success=True)

class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    sign_out = SignOut.Field()
    change_password = ChangePassword.Field()
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
