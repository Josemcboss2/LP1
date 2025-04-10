from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Car

class CarModelTest(TestCase):
    def test_car_creation(self):
        car = Car.objects.create(
            brand="Toyota",
            model="Corolla",
            year=2020,
            price=20000,
            category="sedan",
            condition="new",
            description="A reliable car",
        )
        self.assertEqual(car.brand, "Toyota")
        self.assertEqual(car.model, "Corolla")

class CarViewTest(TestCase):
    def test_car_list_view(self):
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)