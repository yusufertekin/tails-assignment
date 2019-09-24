import json
from math import asin, cos, radians, sin, sqrt

from django.conf import settings

import requests

from tails.stores.models import Store


def load_stores():
    """Read store names and postcodes from stores.json file, make a request to postcode.io to
    get latitude and longitude information of all stores in the given file.

    Notes:
        This assumes stores.json is not too large to be kept in
        dictionary (postcode: store_instance). On a really large stores.json, we might need to
        read from database after creation. It's faster to update latitude and longitude after
        receiving bulk postcode information than making a request to postcodes.io for each store.
        However, because this is I/O bound operation for further improvement we could
        make a request to postcode.io for each postcode and take advantage of
        paralelism using python threads.
    """
    with open('stores.json', 'r') as f:
        stores = json.load(f)

    store_map = {}
    for store_info in stores:
        postcode = store_info['postcode'].replace(' ', '')
        name = store_info['name']
        store_map[postcode], _ = Store.objects.get_or_create(name=name, postcode=postcode)

    for postcode_info in get_bulk_postcode_info(list(store_map.keys())):
        info = postcode_info['result']
        if info:
            store = store_map[info['postcode'].replace(' ', '')]
            store.latitude = info['latitude']
            store.longitude = info['longitude']
            store.save()


def check_if_in_radius(store, source_latitude, source_longitude, radius):
    """
    Returns True if store is in the given radius of given source latitude and longitude,
    and returns False if it's not. Used the solution mentioned here;
    https://stackoverflow.com/a/42687012. Alternative using geopy, the reason is not used here
    is not to introduce dependency for a single function that won't need any change.
    """

    def haversine(lon1, lat1, lon2, lat2):
        """Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    distance = haversine(source_longitude, source_latitude, store.longitude, store.latitude)
    if distance <= radius:
        return True
    else:
        return False


def get_bulk_postcode_info(postcodes):
    """Returns latitude and langitude of given list of postcodes.

    i.e.
    >> response = requests.post(
        'https://api.postcodes.io/postcodes?filter=postcode,latitude,longitude',
        json={'postcodes': ['BN37PN', 'BN90AG']
       })
    >> response.json()
        {
            'status': 200,
            'result': [
                {
                    'query': 'BN37PN',
                    'result': {
                        'postcode': 'BN3 7PN',
                        'latitude': 50.837916,
                        'longitude': -0.17436}
                    },
                {
                    'query': 'BN90AG',
                    'result': {
                        'postcode': 'BN9 0AG',
                        'latitude': 50.798205,
                        'longitude': 0.059491
                    }
                }
            ]
        }
    """
    response = requests.post(
        f'{settings.POSTCODES_IO_BASE_URL}/postcodes?filter=postcode,latitude,longitude',
        json={'postcodes': postcodes},
    )
    if not response.status_code == 200:
        raise Exception('Request failed')

    return response.json()['result']


def get_lat_and_lon_of_given_postcode(postcode):
    """Returns latitude and longitude information of given postcode."""
    response = requests.get(
        f'{settings.POSTCODES_IO_BASE_URL}/postcodes/{postcode}?filter=latitude,longitude',
    )
    if not response.status_code == 200:
        raise Exception('Request failed')

    response_json = response.json()['result']
    return (response_json['latitude'], response_json['longitude'])
