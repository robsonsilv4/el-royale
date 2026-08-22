from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def make_user(name="João", email="joao@example.com", password="senha-segura-123"):
    return User.objects.create_user(name=name, email=email, password=password)


class UserCreationTests(APITestCase):
    def test_create_user_persists_with_hashed_password(self):
        payload = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "password": "senha-segura-123",
        }

        response = self.client.post("/api/v1/users/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="maria@example.com")
        self.assertTrue(user.check_password("senha-segura-123"))
        self.assertNotEqual(user.password, "senha-segura-123")
        self.assertNotIn("password", response.data)

    def test_create_user_requires_email(self):
        response = self.client.post(
            "/api/v1/users/",
            {"name": "João", "password": "senha-segura-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_requires_password(self):
        response = self.client.post(
            "/api/v1/users/",
            {"name": "João", "email": "joao@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_requires_password_min_length(self):
        response = self.client.post(
            "/api/v1/users/",
            {"name": "João", "email": "joao@example.com", "password": "123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = make_user()

    def test_login_returns_tokens(self):
        response = self.client.post(
            "/api/v1/login/",
            {"email": "joao@example.com", "password": "senha-segura-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_rejects_wrong_password(self):
        response = self.client.post(
            "/api/v1/login/",
            {"email": "joao@example.com", "password": "senha-errada"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_returns_new_access_token(self):
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            "/api/v1/login/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_rejects_invalid_token(self):
        response = self.client.post(
            "/api/v1/login/refresh/",
            {"refresh": "token-invalido"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateOwnProfileTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.other_user = make_user(name="Maria", email="maria@example.com")

    def test_update_requires_authentication(self):
        response = self.client.patch(
            f"/api/v1/users/{self.user.id}/", {"name": "Novo Nome"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_update_own_profile_with_patch(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/users/{self.user.id}/", {"name": "Novo Nome"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Novo Nome")

    def test_user_can_update_own_profile_with_put(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(
            f"/api/v1/users/{self.user.id}/",
            {"name": "Novo Nome", "email": "joao@example.com", "password": "nova-senha-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Novo Nome")
        self.assertTrue(self.user.check_password("nova-senha-123"))
        self.assertNotEqual(self.user.password, "nova-senha-123")

    def test_update_hashes_password(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/users/{self.user.id}/", {"password": "nova-senha-123"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("nova-senha-123"))
        self.assertNotEqual(self.user.password, "nova-senha-123")

    def test_user_cannot_update_another_profile(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            f"/api/v1/users/{self.other_user.id}/", {"name": "Nome Hackeado"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminOnlyTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.other_user = make_user(name="Maria", email="maria@example.com")
        self.admin = User.objects.create_superuser(
            name="Admin", email="admin@example.com", password="senha-segura-123"
        )

    def test_list_requires_admin(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_requires_admin(self):
        response = self.client.get(f"/api/v1/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_requires_admin(self):
        response = self.client.delete(f"/api/v1/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/v1/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        response = self.client.delete(f"/api/v1/users/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
