from django.test import TestCase

# Create your tests here.

from django.contrib.auth import authenticate
user = authenticate(username="Felimo", password="Feylicks@123")
print(user)  # Should return a user object or None
