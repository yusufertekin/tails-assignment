from django.test import Client, TestCase
from django.urls import reverse

from tails.utils import load_stores


class StoreTestCase(TestCase):

    def setUp(self):
        load_stores()
        self.client = Client()

    def test_list_of_stores_in_given_radius_of_given_postcode(self):
        """Test that correctly returns stores around from north to south
        in given radius of given postcode.
        """
        expected_data = [
            {
                'name': 'Hove',
                'postcode': 'BN37PN',
                'latitude': '50.837916',
                'longitude': '-0.174360',
            },
            {
                'name': 'Worthing',
                'postcode': 'BN149GB',
                'latitude': '50.834955',
                'longitude': '-0.367010',
            },
            {
                'name': 'Rustington',
                'postcode': 'BN163RT',
                'latitude': '50.817576',
                'longitude': '-0.498092',
            },
        ]
        endpoint_url = reverse('stores:around')
        response = self.client.post(
            f'{endpoint_url}',
            data={
                'postcode': 'BN14 9GB',
                'radius': 15,
            },
        )
        assert expected_data == response.json()
