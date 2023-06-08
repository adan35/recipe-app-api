"""
Views from the user API
"""
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user system"""
    serializer_class = UserSerializer
