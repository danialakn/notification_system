from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, RegisterView, AllUserIdsView,UserTokenValidateView,ListUsersView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='custom_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/internal/all-user-ids/', AllUserIdsView.as_view(), name='all_user_ids'),
    path('api/internal/list-user-ids/', ListUsersView.as_view(), name='list_user_ids'),
    path('api/internal/token/validate/', UserTokenValidateView.as_view(), name='internal-token-validate'),

]