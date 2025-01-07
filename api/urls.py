from django.urls import path, include
from api.views import MealList, MealDetail, RatingList, RatingDetail, MealDispatchAPIView

# Define the URL patterns for the API
urlpatterns = [
  # URL pattern for listing all meals
  path('meals/', MealList.as_view(), name='meal-list'),
  
  # URL pattern for retrieving a specific meal by UUID
  path('meals/<uuid:pk>/', MealDetail.as_view(), name='meal-detail'),
  
  # URL pattern for listing all ratings
  path('ratings/', RatingList.as_view(), name='rating-list'),
  
  # URL pattern for retrieving a specific rating by UUID
  path('ratings/<uuid:pk>/', RatingDetail.as_view(), name='rating-detail'),
  
  # URL pattern for dispatching meals
  path('meals/dispatch/', MealDispatchAPIView.as_view(), name='meal-dispatch'),
  
  # URL pattern for dispatching a specific meal by UUID
  path('meals/dispatch/<uuid:meal_id>/', MealDispatchAPIView.as_view(), name='meal-dispatch-detail'),
]