from rest_framework import serializers
from realestateapp.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','username','email', 'password', 'role', 'company_name', 'professional_credentials', 'is_approved']

    def create(self, validated_data):
        is_approved = validated_data.pop('is_approved', False)
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],
            company_name=validated_data.get('company_name'),  # validated_data.get use kr rhy na mly data to error throw nai kry ga
            professional_credentials=validated_data.get('professional_credentials'),
            is_approved=is_approved,
        )
        return user

# realestateapp/authentication/serializers.py

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_approved:
            raise serializers.ValidationError("Your account is not approved yet.")

        data = super().validate(attrs)
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'role': user.role,
        }
        return data

