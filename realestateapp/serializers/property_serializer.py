# serializers.py
from rest_framework import serializers
from realestateapp.models import Property, PropertyType, SubPropertyType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['name']


class SubPropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPropertyType
        fields = ['name', 'property_type']

class PropertySerializer(serializers.ModelSerializer):
    property_type_detail = PropertyTypeSerializer(source='property_type', read_only=True)
    sub_property_type_detail = SubPropertyTypeSerializer(source='sub_property_type', read_only=True)
    developer_detail = UserBasicSerializer(source='developer', read_only=True)
    class Meta:
        model = Property
        fields = [
            'id','title', 'description', 'city', 'location',
            'price', 'beds', 'baths', 'area', 'area_unit',
            'category', 'status', 'brochure', 'floor_plan',
            'created_at', 'developer', 'property_type', 'sub_property_type',
            'property_type_detail', 'sub_property_type_detail', 'developer_detail'
        ]
        read_only_fields = ['id','developer', 'status', 'created_at']
