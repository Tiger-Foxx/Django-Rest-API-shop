from django.contrib import admin
from django.urls import path, include
from shop.views import *
from rest_framework import routers
from shop.views import CategoryViewset
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView


router=routers.SimpleRouter()
router.register('category',CategoryViewset,basename='category')
router.register('product',ProductViewSet,basename='product')
router.register('article',ArticleViewSet,basename='article')
router.register('admin/article',AdminArticleViewSet,basename='admin-article')
router.register('admin/category',AdminCategoryViewset,basename='admin-category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #path('api/category/', CategoryApiView.as_view()),
    #path('api/products/',ProductApiView.as_view()),
    path('api/', include(router.urls)),
    #ceci sont respectivement les vues qui permettent de fournir un jeton jwt et de rafraischir son jeton jwt , a noter que pour obtenir le jeton il faut envoyer dans le body de la requete un username et password
    # et pour le rafraischir il faut aller vers la route de refresh et fournir le token de refresh
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
