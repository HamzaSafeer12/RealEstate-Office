from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

# ----------- Property Type Models -----------

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubPropertyType(models.Model):
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='subtypes')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.property_type.name} - {self.name}"


# ----------- Property Main Model -----------

class Property(models.Model):
    CATEGORY_CHOICES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('lease', 'Lease'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('leased', 'Leased'),
    ]

    BEDS_CHOICES = [(i, str(i)) for i in range(1, 11)]
    BATHS_CHOICES = [(i, str(i)) for i in range(1, 11)]

    AREA_UNIT_CHOICES = [
        ('marla', 'Marla'),
        ('kanal', 'Kanal'),
        ('sqft', 'Square Feet'),
    ]

    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='developer_properties')
    realtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='realtor_properties', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    sub_property_type = models.ForeignKey(SubPropertyType, on_delete=models.SET_NULL, null=True)

    beds = models.IntegerField(choices=BEDS_CHOICES, null=True, blank=True)
    baths = models.IntegerField(choices=BATHS_CHOICES, null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    area_unit = models.CharField(max_length=10, choices=AREA_UNIT_CHOICES, null=True, blank=True)

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    brochure = models.FileField(
        upload_to='brochures/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    floor_plan = models.FileField(
        upload_to='floor_plans/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
