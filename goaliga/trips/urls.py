from . import views
from .views import *


from django.urls import path
urlpatterns = [
 path('packages/',ViewPackages.as_view(),name='packages'),
  # path('packages/',views.ViewPackages.as_view(),name='packages'),
  path('trips/<slug:category_slug>/',views.trips,name='packages'),
  path('trips/<slug:category_slug>/<slug:package_slug>/',views.tripdetails,name='packages'),
  path('category/',views.viewCat,name='category'),
  path('bookslot',views.Bookuser,name='slotbook'),
  path('addvariation/',views.addVariation,name='addvariation'),
  path('packse/',SearchPackages.as_view(),name='packages'),
  path('packor/',OrderPackages.as_view(),name='packages'),
  path('packfilter/',FilterPackages.as_view(),name='packages'),
    
]