from django.contrib import admin
from .models import Category,Itinerary,Packages,DateBooking,Variations
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('category_name',)}
  list_display = ('category_name', 'slug')

class PackageAdmin(admin.ModelAdmin):
     prepopulated_fields = {'slug':('package_name',)}
     list_display = ('package_name', 'slug','stock',)

class VariationModel(admin.ModelAdmin):     
  list_display=('package','variation_category','variation_value')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Itinerary)
admin.site.register(Packages,PackageAdmin)
admin.site.register(DateBooking)
admin.site.register(Variations,VariationModel)