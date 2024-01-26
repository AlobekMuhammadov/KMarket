from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf import settings

urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', IndexView.as_view(), name="main"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('aloqa/', ContactView.as_view(), name="aloqa"),
    path('sotib-olish/', CheckoutView.as_view(), name="sotib-olish"),
    path('savat/', CartView.as_view(), name="savat"),
    path('mahsulot/<int:pk>/', DetailView.as_view()),
    path('yoqganlar/', LikesListView.as_view(), name="likeslist"),
    path('like/<int:pk>/', LikeView.as_view()),
    path('item_plus/<int:pk>/', ItemPlusView.as_view()),
    path('item_minus/<int:pk>/', ItemMinusView.as_view()),
    path('bolim/<int:pk>/', BolimView.as_view()),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
