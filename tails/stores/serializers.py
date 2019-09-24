from rest_framework.serializers import ModelSerializer

from tails.stores.models import Store


class StoreSerializer(ModelSerializer):

    class Meta:
        model = Store
        fields = ('name', 'postcode', 'latitude', 'longitude')
