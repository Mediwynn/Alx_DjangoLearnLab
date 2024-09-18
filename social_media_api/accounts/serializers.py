from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()  # Password will not be write-only

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Create a user and hash their password
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Hash the password
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )

        # Create a token for the newly created user
        Token.objects.create(user=user)
        
        return user
