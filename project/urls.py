from django.contrib import admin
from django.urls import path, include
from shop.views import *
from rest_framework import routers
from shop.views import CategoryViewset

router=routers.SimpleRouter()
router.register('category',CategoryViewset,basename='category')
router.register('product',ProductViewSet,basename='product')
router.register('article',ArticleViewSet,basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #path('api/category/', CategoryApiView.as_view()),
    #path('api/products/',ProductApiView.as_view()),
    path('api/', include(router.urls)),
]
