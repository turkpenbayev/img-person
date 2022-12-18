from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.routers import reverse

from images.models import Person
from images.serializers import ListPersonNameSerializer


class PersonNamesAPIViewTestCase(APITestCase):
    def setUp(self):
        self.persons = []

        for i in range(3):
            p = Person.objects.create(
                name=f'name {i+1}'
            )
            self.persons.append(p)

        self.client_user = User.objects.create_user(username='john',
                                                    email='jlennon@beatles.com',
                                                    password='glass onion')
        self.person_url = reverse("person-names")
        self.token = Token.objects.create(user=self.client_user)

    def test_person_names_not_auth(self):
        """
        Test to person names m=not auth user
        """
        response = self.client.get(self.person_url)
        self.assertEqual(401, response.status_code)

    def test_person_names_auth_user(self):
        """
        Test to person names
        """
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get(self.person_url, {'name': 'name'}, **header)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()['names'], ['name 1', 'name 2', 'name 3'])
