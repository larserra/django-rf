from django.urls import path
from .views import ( 
    Register_view, 
    Login_view,
    UserProfile_View, 
    Logout_view,
    Forgot_view, 
    Reset_view,
    # Products_view,
    # ProductDetail_view,
    MyTokenObtainPairView
    ) 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', Register_view.as_view()),
    path('login/', Login_view.as_view()),
    path('logout', Logout_view.as_view()),

    path('forgot/', Forgot_view.as_view()),
    path('reset', Reset_view.as_view()),

    path('user/', UserProfile_View.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name=''),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('products/', Products_view.as_view()),
    # path('products/<str:pk>/', ProductDetail_view.as_view()),
]