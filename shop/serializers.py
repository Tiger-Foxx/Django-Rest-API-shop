from rest_framework.serializers import ModelSerializer,SerializerMethodField

from shop.models import Article, Category, Product

from rest_framework import serializers





        
        
class ProductSerializer(ModelSerializer):
    articles=SerializerMethodField()
    class Meta:
        model = Product
        fields=['id', 'name','category_id','date_created','date_updated','articles']
    
    def get_articles(self,instance):
        queryset=instance.articles.filter(active=True)
        serializer=ArticleSerializer(queryset,many=True)
        return serializer.data
        
        

class ArticleSerializer(ModelSerializer):
    class Meta:
        model=Article
        fields=['id','date_created','price','product_id','date_updated','name']
        
    def validate(self, data):
        price=data['price']
        active= Product.objects.get(id=data['product_id']).active
        if not active :
            raise serializers.ValidationError('Ce produit est désactivé') 
        if price<1:
            raise serializers.ValidationError('Le prix doit être supérieur à 1$')
        return data
        
class CategoryDetailSerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']
    # methode pour definir une validation sur le champ du nom
    def validate_name(self,value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Cette catégorie existe déjà')
        return value

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data
    

class CategorySerializer(ModelSerializer):

    # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'

    class Meta:
        model = Category
        fields = ['id', 'name']
    
    def validate_name(self,value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Cette catégorie existe déjà')
        return value

 