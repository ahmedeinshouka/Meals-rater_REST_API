from django.contrib import admin
from api.models import Meal, Rating
# Register your models here.


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name', 'date')
    list_filter = ('date', 'name')
    ordering = ('-date',)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('meal', 'user', 'stars')
    search_fields = ('meal', 'user')
    list_filter = ('meal', 'user')
    ordering = ('-meal',)
    
admin.site.register(Meal, MealAdmin)
admin.site.register(Rating, RatingAdmin)
    
    
    
    