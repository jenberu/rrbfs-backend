
from django.urls import path
from .views import (RegisterView, CurrentUserView, 
                    UserLoginView,GetUsersAPIView,
                    DepartmentListAPIView
                    , ChangePasswordView,
                    TotalUsersView)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', GetUsersAPIView.as_view(), name='get-users'),
    path('departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
        path("total-users/", TotalUsersView.as_view(), name="total-users"),




]
