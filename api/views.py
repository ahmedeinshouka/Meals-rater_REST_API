from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import mixins, generics, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from api.models import Meal, Rating
from api.serializers import MealSerializer, RatingSerializer
from rest_framework import filters

# Create your views here.

# View for listing and creating meals
class MealList(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Meal.objects.all()
  serializer_class = MealSerializer
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['name', 'description']
  ordering_fields = ['date']

# View for retrieving, updating, and deleting a specific meal
class MealDetail(generics.RetrieveUpdateDestroyAPIView):
  authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Meal.objects.all()
  serializer_class = MealSerializer

# View for listing and creating ratings
class RatingList(generics.ListCreateAPIView):
  authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Rating.objects.all()
  serializer_class = RatingSerializer
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['meal__name', 'user__username']
  ordering_fields = ['stars']

  # Override perform_create to associate the rating with the current user
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

# View for retrieving, updating, and deleting a specific rating
class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
  authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  queryset = Rating.objects.all()
  serializer_class = RatingSerializer

# Dispatch-based API view for handling Meal objects
class MealDispatchAPIView(APIView):
  """
  Dispatch-based API view for handling Meal objects.
  """
  authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  search_fields = ['name', 'description']
  ordering_fields = ['date']

  # Custom dispatch method to handle request type and additional logic
  def dispatch(self, request, *args, **kwargs):
    print(f"Request Method: {request.method}")  # Debugging
    return super().dispatch(request, *args, **kwargs)

  # Handle GET requests to retrieve meals or a single meal by ID
  def get(self, request, *args, **kwargs):
    meal_id = kwargs.get('meal_id')
    if (meal_id):
      try:
        meal = Meal.objects.get(id=meal_id)
        serializer = MealSerializer(meal)
        return Response(serializer.data, status=status.HTTP_200_OK)
      except Meal.DoesNotExist:
        return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
      meals = Meal.objects.all()
      serializer = MealSerializer(meals, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

  # Handle POST requests to create a new meal
  def post(self, request, *args, **kwargs):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # Handle PUT requests to update an existing meal
  def put(self, request, *args, **kwargs):
    meal_id = kwargs.get('meal_id')
    try:
      meal = Meal.objects.get(id=meal_id)
      serializer = MealSerializer(meal, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Meal.DoesNotExist:
      return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)

  # Handle DELETE requests to delete a meal by ID
  def delete(self, request, *args, **kwargs):
    meal_id = kwargs.get('meal_id')
    try:
      meal = Meal.objects.get(id=meal_id)
      meal.delete()
      return Response({"message": "Meal deleted successfully."}, status=status.HTTP_200_OK)
    except Meal.DoesNotExist:
      return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)
