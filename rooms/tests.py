from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from hotels.models import Hotel

from .models import Room

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


def room_payload(number=101, description="Suite"):
    return {"number": number, "description": description}


class RoomListTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.hotel = make_hotel()
        self.other_hotel = make_hotel(name="Hotel Recife", city="Recife", state="PE")
        self.room = Room.objects.create(number=101, hotel=self.hotel)
        Room.objects.create(number=102, hotel=self.hotel)
        Room.objects.create(number=201, hotel=self.other_hotel)

    def test_list_is_public_and_restricted_to_parent_hotel(self):
        response = self.client.get(f"/api/v1/hotels/{self.hotel.id}/rooms/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        numbers = [room["number"] for room in response.data["results"]]
        self.assertEqual(numbers, [101, 102])
        self.assertNotIn(201, numbers)


class RoomCreateTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = make_user()
        self.hotel = make_hotel()
        self.other_hotel = make_hotel(name="Hotel Recife", city="Recife", state="PE")

    def test_create_requires_authentication(self):
        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/", room_payload(), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_room_in_parent_hotel(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/", room_payload(), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["hotel"], str(self.hotel.id))
        self.assertEqual(Room.objects.get(pk=response.data["id"]).hotel_id, self.hotel.id)


class RoomValidationTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = make_user()
        self.hotel = make_hotel()
        self.client.force_authenticate(self.user)

    def test_rejects_negative_number(self):
        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/",
            room_payload(number=-1),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("number", response.data)

    def test_rejects_zero_number(self):
        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/",
            room_payload(number=0),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("number", response.data)

    def test_rejects_non_integer_number(self):
        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/",
            room_payload(number="abc"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("number", response.data)

    def test_rejects_duplicate_number_in_same_hotel(self):
        Room.objects.create(number=101, hotel=self.hotel)

        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/",
            room_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allows_same_number_in_different_hotels(self):
        other_hotel = make_hotel(name="Hotel Recife", city="Recife", state="PE")
        Room.objects.create(number=101, hotel=other_hotel)

        response = self.client.post(
            f"/api/v1/hotels/{self.hotel.id}/rooms/",
            room_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RoomDestroyTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = make_user()
        self.admin = User.objects.create_superuser(
            name="Admin", email="admin@example.com", password="senha-segura-123"
        )
        self.hotel = make_hotel()
        self.other_hotel = make_hotel(name="Hotel Recife", city="Recife", state="PE")
        self.room = Room.objects.create(number=101, hotel=self.hotel)

    def test_destroy_requires_admin(self):
        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_not_found_outside_parent_hotel(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(f"/api/v1/hotels/{self.other_hotel.id}/rooms/{self.room.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Room.objects.filter(id=self.room.id).exists())

    def test_admin_can_destroy_room(self):
        self.client.force_authenticate(self.admin)

        response = self.client.delete(f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())


class RoomRetrieveUpdateTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = make_user()
        self.hotel = make_hotel()
        self.other_hotel = make_hotel(name="Hotel Recife", city="Recife", state="PE")
        self.room = Room.objects.create(number=101, hotel=self.hotel)

    def test_retrieve_is_public(self):
        response = self.client.get(f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], 101)

    def test_room_not_found_outside_parent_hotel(self):
        response = self.client.get(f"/api/v1/hotels/{self.other_hotel.id}/rooms/{self.room.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_requires_authentication(self):
        response = self.client.patch(
            f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/",
            {"description": "Nova descrição"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_not_found_outside_parent_hotel(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/hotels/{self.other_hotel.id}/rooms/{self.room.id}/",
            {"description": "Nova descrição"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_update_room(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/",
            {"description": "Nova descrição"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.description, "Nova descrição")

    def test_update_rejects_duplicate_number(self):
        self.client.force_authenticate(self.user)
        Room.objects.create(number=102, hotel=self.hotel)

        response = self.client.patch(
            f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/",
            {"number": 102},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("number", response.data)

    def test_update_allows_keeping_own_number(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/hotels/{self.hotel.id}/rooms/{self.room.id}/",
            {"number": 101},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
