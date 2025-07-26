from rest_framework import viewsets, filters
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.core.cache import cache
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock', 'created_at']

    def list(self, request, *args, **kwargs):
        cached_data = cache.get('product_list')
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        cache.set('product_list', serializer.data, timeout=3600)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        cache.delete('product_list')
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        cache.delete('product_list')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        cache.delete('product_list')
        return super().perform_destroy(instance)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
