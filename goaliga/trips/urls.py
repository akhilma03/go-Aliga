from . import views
from .views import ViewPackages


from django.urls import path
urlpatterns = [
 path('packages/',views.ViewPackages.as_view(),name='packages'),
  path('trips/<slug:category_slug>/',views.trips,name='packages'),
  path('trips/<slug:category_slug>/<slug:package_slug>/',views.tripdetails,name='packages'),
  path('category/',views.viewCat,name='category'),
    path('addpack/',views.addPackage,name='addpackage'),

]