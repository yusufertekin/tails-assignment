from decimal import Decimal

from django.db.models import Q

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from tails.stores.models import Store
from tails.stores.serializers import StoreSerializer
from tails.utils import check_if_in_radius, get_lat_and_lon_of_given_postcode


@api_view(['GET'])
def stores(request):
    """Return list of stores ordered by postcode and name.

    Example Response:
        [{
            'name': 'St_Albans',
            'postcode': 'AL12RJ',
            'latitude': '51.741753',
            'longitude': '-0.341337',   
        }]
    """
    search = request.GET.get('search')
    paginator = LimitOffsetPagination()
    queryset = Store.objects.all()
    if search:
        queryset = queryset.filter(
            Q(name__contains=search) or
            Q(postcode__contains=search)
        )

    queryset = queryset.order_by('postcode', 'name')
    if request.GET.get('limit'):
        page = paginator.paginate_queryset(queryset)
        if page is not None:
            serializer = StoreSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

    serializer = StoreSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def stores_in_given_radius_of_given_postcode(request):
    """Return list of stores in given radius (km) of given postcode in the UK ordered
    from north to south.
    """

    radius = request.POST.get('radius')
    if radius:
        radius = Decimal(radius)
    else:
        return Response('Radius is required', status=status.HTTP_404_NOT_FOUND)

    postcode = request.POST.get('postcode')
    if postcode:
        postcode = postcode.replace(' ', '')
    else:
        return Response('Postcode is required', status=status.HTTP_404_NOT_FOUND)

    stores_in_given_radius = []
    source_latitude, source_longitude = get_lat_and_lon_of_given_postcode(postcode)

    for store in Store.objects.order_by('-latitude'):
        if store.latitude and store.longitude:
            if check_if_in_radius(store, source_latitude, source_longitude, radius):
                stores_in_given_radius.append(store)

    serializer = StoreSerializer(stores_in_given_radius, many=True)
    return Response(serializer.data)
