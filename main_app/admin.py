from django.contrib import admin
from .models import Cat, Feeding, Toy

# Register your models here.

admin.site.register(Cat)  # Allows admins to manage cats
admin.site.register(Feeding)
admin.site.register(Toy)