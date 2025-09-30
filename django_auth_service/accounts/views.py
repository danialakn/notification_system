from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import os

from .serializers import UserRegisterSerializer,LoginSerializer,UserIdSerializer, TokenIntrospectionSerializer
from .models import User
#..........................................................................................................
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return Response(data={f'user {user.username} created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#.........................................................................................................
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.is_active:
                return Response(data={'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#.................................................................................................
# A simple permission to check for a shared secret key in the headers

class IsInternalService(BasePermission):
    def has_permission(self, request, view):
        # Read the secret key from environment variables
        internal_service_key = os.getenv("INTERNAL_SERVICE_KEY")

        # Check if the header from the incoming request matches our key
        provided_key = request.headers.get('X-Internal-Service-Key')

        return provided_key is not None and provided_key == internal_service_key

#...................................................................................................
@method_decorator(csrf_exempt, name="dispatch")
class AllUserIdsView(ListAPIView):
    """
    An internal endpoint to get a list of all active user IDs.
    Accessible only by other microservices.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserIdSerializer
    permission_classes = [IsInternalService]
#...................................................................................................
@method_decorator(csrf_exempt, name="dispatch")
class ListUsersView(APIView):
    permission_classes = [IsInternalService]
    def get(self, request):
        ids_str = request.query_params.get('ids', None)
        if not ids_str:
            return Response({"error": "Please provide user IDs in the 'ids' query parameter."},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            user_ids = [int(id_str) for id_str in ids_str.split(',')]
        except ValueError:
            return Response(
                {"error": "Invalid ID format. IDs must be comma-separated integers."},
                status=status.HTTP_400_BAD_REQUEST)

        queryset = User.objects.filter(is_active=True, id__in=user_ids)
        serializer = UserIdSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#...................................................................................................
@method_decorator(csrf_exempt, name="dispatch")
class UserTokenValidateView(APIView):

    permission_classes = [IsInternalService]  # فقط سرویس‌های داخلی اجازه دسترسی دارند

    def post(self, request):
        print("====== INSIDE THE VALIDATE VIEW POST METHOD! ======")
        serializer = TokenIntrospectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_str = serializer.validated_data['token']

        try:
            token = AccessToken(token_str)

            return Response(token.payload, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError) as e:
            return Response({"detail": "Token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)


