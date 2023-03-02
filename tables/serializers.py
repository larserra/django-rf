from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Reset, Product

# ===============================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password', 'is_admin']
        extra_kwargs = {'password':{'write_only' : True}}
  
# --------------------------------------VALIDATION PASSWORD NORMAL USER
    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError({'password': serializer_errors['non_field_errors']})
        return data
# ------------------------------------- CREATE USER REGISTER       
    def create(self, validated_data):  
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        
            
    def get_isAdmin(self, obj):
        return obj.is_staff

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
# ======================================================
# class UserSerializerWithToken(ModelSerializer):
#     token = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = User
#         fields = ['id','first_name','last_name', 'is_admin','email', 'token',]
        
#     def get_token(self, obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)


class ResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reset
        fields = ('email',)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'