from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            'category',
            'label',
            'label_text',
            'slug',
            'description',
            'image'
        )

