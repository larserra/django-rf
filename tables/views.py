from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Reset, User
from .serializers import UserSerializer
from django.core.mail import send_mail
import random, string


# =============================EDIT TOKEN
# # ========================JWT POST View 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['refresh'] =str(refresh)
        data['access'] = str(refresh.access_token)

        return data
# =====================JWT.IO view
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ==============================REGISTER_VIEW
class Register_view(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password not Match')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
       
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ====================================LOGIN_VIEW
class Login_view(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid Credentials')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid Credentials')

        refresh = RefreshToken.for_user(user.id)
        user['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        serializer = UserSerializer(user)

        return Response(serializer.data)
      
        # ==================comment
# =========================================USERLIST
class UserList_view(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = request.user
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfile_View(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class Logout_view(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {'message': 'success'}
        return response


class Forgot_view(APIView):
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(
            string.ascii_lowercase + string.digits)for _ in range(20))
        Reset.objects.create(email=email, token=token)
        url = 'http://localhost:3000/reset/' + token

        send_mail(subject='Reset your passowrd!',
                  message='Click <a href="%s">here</a> to reset your password!' % url,
                  from_email='do_not@reply.com',
                  recipient_list=[email])
        return Response({'message': 'success'})


class Reset_view(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        reset_password = Reset.objects.filter(token=data['token']).first()

        if not reset_password:
            raise exceptions.APIException('Invalid link!')
        
        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('User not found!')
        
        user.set_password(data['password'])
        user.save()

        return Response({'message':'success'})