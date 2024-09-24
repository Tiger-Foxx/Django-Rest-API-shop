from rest_framework.views import APIView 
from rest_framework.viewsets import ModelViewSet ,ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Article, Category, Product
from shop.serializers import ArticleSerializer, CategoryDetailSerializer, CategorySerializer, ProductSerializer


class CategoryApiView(APIView):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

class ProductApiView(APIView):
    def get(self, *args, **kwargs):
        produits = Product.objects.all()
        serializer = ProductSerializer(produits, many=True)
        return Response(serializer.data)
    

class MultipleSerializerMixin:
    detail_serializer_class = None
    
    def get_serializer_class(self):
        print('get serialiser class')
        # On vérifie si l'action est une vue de détail ou toute autre action définie comme `detail=True`
        if getattr(self, 'action', None) in ['retrieve', 'disable'] and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class CategoryViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):
 
    serializer_class = CategorySerializer
    detail_serializer_class=CategoryDetailSerializer
    
    #je definie une action de type detail avec une methode post
    @action(methods=['post'],detail=True)
    def disable(self,request,pk):
        self.get_object().disable()
        return Response({'message':'La catégorie a été désactivée'})
    def get_queryset(self):
        return Category.objects.all()
    
class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class=ProductSerializer
    
    
    def get_queryset(self):
        produits=Product.objects.all()
        category_id=self.request.GET.get('category_id')
        if category_id is not None:
            produits=Product.objects.filter(category_id=category_id)
        return produits
    
class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class=ArticleSerializer
    def get_queryset(self):
        articles=Article.objects.filter(active=True)
        product_id=self.request.GET.get('product_id')
        category_id=self.request.GET.get('category_id')
        if product_id is not None:
            articles=Article.objects.filter(product_id=product_id,active=True)
        elif category_id is not None :
            articles=Article.objects.filter(product__category_id=category_id,active=True)
            
        return articles
    

