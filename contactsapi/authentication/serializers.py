from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def save(self):
            user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
            )
            password = self.validated_data['password']
            print(password)
            user.set_password(password, algorithm="HS256")
            user.save()
            return user

        def validate(self, attrs):
            email = attrs.get('email', '')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'email': 'Email is already in use'})
            return super().validate(attrs)

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']
