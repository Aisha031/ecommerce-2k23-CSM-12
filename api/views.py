from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Validation for negative stock rejection
        stock = request.data.get('stock_quantity')
        if stock is not None and int(stock) < 0:
            return Response({"detail": "Stock cannot be negative"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        self.perform_update(serializer)
        return Response(serializer.data)