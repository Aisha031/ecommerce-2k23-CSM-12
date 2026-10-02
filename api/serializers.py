from rest_framework import serializers
# Explicit import se path ka masla hamesha ke liye khatam
from api.models import Product, WellnessTag

class WellnessTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessTag
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    wellness_tags = WellnessTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=WellnessTag.objects.all(), write_only=True, source='wellness_tags'
    )

    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'ingredients', 'price', 'stock_quantity', 'wellness_tags', 'tag_ids']
        read_only_fields = ['seller']