from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response
from accounts.serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegistrationSerializer(user).data,
            "message": "User registered successfully."
        })
