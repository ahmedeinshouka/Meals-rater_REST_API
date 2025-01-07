from . import models
from rest_framework import serializers



class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meal
        fields = ( 'id','name', 'description', 'image', 'date')
        filterset_fields = ('name', 'date')
        read_only_fields = ('id',)
        
class RatingSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)  # Read-only for responses
    meal_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Meal.objects.all(), source='meal', write_only=True
         )
    user=serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    class Meta:
        model = models.Rating
        fields = ('id','meal', 'user','meal_id','stars', 'description')
        filterset_fields = ('meal', 'user')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'password')
        filterset_fields = ('username',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super().update(instance, validated_data)                 
  
  
  