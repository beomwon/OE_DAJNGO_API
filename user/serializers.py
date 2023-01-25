from rest_framework import serializers
from .models import User, MustFood, Preference

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class MustFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MustFood
        fields = "__all__"

class PreferenceSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Preference
        fields = "__all__"

        