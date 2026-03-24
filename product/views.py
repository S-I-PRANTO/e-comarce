from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product,Categroy,Review,ProductImages
from django.db.models import Count
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from product.filters import ProductFilter
from product.pagination import paginationpage
from product.permission import IsAdminOrReadOnly,ReviewAuthorReadonly
class ProductList(ModelViewSet):
    """
    API endpoint for managing products in the E-commerce store

    - Allow authenticatd admin to create,update and delete product
    - Allow users to browse and filter product 
    - Support searching by name, description, and category
    - Support ordering by price and updated_at

    """

    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_class=ProductFilter
    search_fields=['name','description','category__name']
    pagination_class=paginationpage
    permission_classes=[IsAdminOrReadOnly]
    

    def list(self, request, *args, **kwargs):
        """ Retrive all the Products"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """ Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        product=self.get_object()
        if product.stoke > 10:
            self.perform_destroy(product)
            return Response(status=status.HTTP_204_NO_CONTENT)

class ProductImagesViewset(ModelViewSet):
    serializer_class=ProductImageSerializer

    def get_queryset(self):
        return ProductImages.objects.filter(product_id=self.kwargs.get('product_pk'))
       
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))



class CategoryList(ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    queryset=Categroy.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer




class ReviewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[ReviewAuthorReadonly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    def get_serializer_context(self):
        return {'product_id':self.kwargs.get('product_pk')}

    







# @api_view(['GET','POST'])
# def product_view(request):
#     if request.method =='GET':
#         product=Product.objects.select_related('categroy').all()
#         serializer=ProductSerializer(
#             product,many=True
#         )
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
    

# @api_view(['GET','PUT','DELETE'])
# def specificProduct(request,pk):
#     if request.method == 'GET':
#         product=get_object_or_404(Product,pk=pk)
#         seralizer=ProductSerializer(product)
#         return Response(seralizer.data)
    
#     if request.method == 'PUT':
#         product=get_object_or_404(Product,pk=pk)
#         seralizer=ProductSerializer(product,data=request.data)
#         seralizer.is_valid(raise_exception=True)
#         seralizer.save()
#         return Response(seralizer.data)
    
#     if request.method == 'DELETE':
#         product=get_object_or_404(Product,pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view()
# def category_view(request):
#     category=Categroy.objects.annotate(product_count=Count('products')).all()
#     serializer=CategorySerializer(
#         category,many=True
#     )
#     return Response(serializer.data)

# def specificCategory(request,pk):
#     category=get_object_or_404(Categroy,pk=pk)
#     serializer=CategorySerializer(category)
#     return Response(serializer.data)


