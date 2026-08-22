from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Hotel

User = get_user_model()


def make_user(name="João", email="joao@example.com", password="senha-segura-123"):
    return User.objects.create_user(name=name, email=email, password=password)


def make_hotel(name="Hotel Fortaleza", city="Fortaleza", state="CE"):
    return Hotel.objects.create(
        name=name,
        address="Rua das Flores, 100",
        city=city,
        state=state,
        phone="85999999999",
    )


def hotel_payload(name="Hotel Novo", city="Fortaleza", state="CE"):
    return {
        "name": name,
        "address": "Rua das Flores, 100",
        "city": city,
        "state": state,
        "phone": "85999999999",
    }


class PublicAccessTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.hotel = make_hotel()
        make_hotel(name="Hotel Recife", city="Recife", state="PE")

    def test_list_is_public_and_paginated(self):
        response = self.client.get("/api/v1/hotels/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_is_public(self):
        response = self.client.get(f"/api/v1/hotels/{self.hotel.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.hotel.name)


class AuthenticatedWriteTests(APITestCase):
    def setUp(self):
        self.user = make_user()

    def test_create_requires_authentication(self):
        response = self.client.post("/api/v1/hotels/", hotel_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_requires_authentication(self):
        hotel = make_hotel()

        response = self.client.put(
            f"/api/v1/hotels/{hotel.id}/",
            hotel_payload(name="Novo Nome"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_requires_authentication(self):
        hotel = make_hotel()

        response = self.client.patch(
            f"/api/v1/hotels/{hotel.id}/", {"name": "Novo Nome"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_hotel(self):
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/v1/hotels/", hotel_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 1)

    def test_authenticated_user_can_update_hotel(self):
        self.client.force_authenticate(self.user)
        hotel = make_hotel()

        response = self.client.patch(
            f"/api/v1/hotels/{hotel.id}/", {"name": "Novo Nome"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hotel.refresh_from_db()
        self.assertEqual(hotel.name, "Novo Nome")

    def test_authenticated_user_can_put_hotel(self):
        self.client.force_authenticate(self.user)
        hotel = make_hotel()

        response = self.client.put(
            f"/api/v1/hotels/{hotel.id}/",
            hotel_payload(name="Nome do Put"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hotel.refresh_from_db()
        self.assertEqual(hotel.name, "Nome do Put")


class AdminDestroyTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.admin = User.objects.create_superuser(
            name="Admin", email="admin@example.com", password="senha-segura-123"
        )
        self.hotel = make_hotel()

    def test_destroy_requires_admin(self):
        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_destroy_hotel(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Hotel.objects.filter(id=self.hotel.id).exists())


class FilterTests(APITestCase):
    def setUp(self):
        cache.clear()
        make_hotel(name="Hotel A", city="Fortaleza", state="CE")
        make_hotel(name="Hotel B", city="Recife", state="PE")
        make_hotel(name="Hotel C", city="Fortaleza", state="PE")

    def test_filter_by_state(self):
        response = self.client.get("/api/v1/hotels/", {"state": "CE"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Hotel A")

    def test_filter_by_city(self):
        response = self.client.get("/api/v1/hotels/", {"city": "Fortaleza"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_pagination_default_page_size(self):
        for i in range(11):
            make_hotel(name=f"Hotel {i}")

        response = self.client.get("/api/v1/hotels/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])
