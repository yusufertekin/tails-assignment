from django.urls import path

from tails.stores.views import stores, stores_in_given_radius_of_given_postcode


urlpatterns = [
    path('', stores, name='list'),
    path('around/', stores_in_given_radius_of_given_postcode, name='around'),
]
