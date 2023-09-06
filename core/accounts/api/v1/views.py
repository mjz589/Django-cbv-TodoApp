from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
                RegistrationSerializer,
                CustomAuthTokenSerializer,
                CustomTokenObtainPairSerializer,
                ChangePasswordApiSerializer,
                ProfileSerializer,)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# jwt
from rest_framework_simplejwt.views import TokenObtainPairView
# change password
from django.contrib.auth import get_user_model
# profile
from ...models import Profile
from django.shortcuts import get_object_or_404
# email
# from django.core.mail import send_mail
# from mail_templated import send_mail
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError

User = get_user_model()



class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data ={
                'detail' : 'We sent an email to you for verification. Please check your email and click the link to verify your account.',
                'email': email,
                
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token }, 'admin@admin.com', to=[email] )
            EmailThread(email_obj).start()
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    

# custom Auth Token
class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# discard token
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    

# custom TokenObtainPairView
class CostumTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# change password view
class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordApiSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old Password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user wiil get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'details':'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# profile
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
        
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    

# email
class EmailTestSend(generics.GenericAPIView):
    def get(self, *args, **kwargs):
        self.email = 'mjz589.2018@gmail.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token }, 'admin@admin.com', to=[self.email] )
        EmailThread(email_obj).start()
        return Response('email sent')
    
    # get access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# verify user by jwt token after sending email
class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        # if token has been expired
        except ExpiredSignatureError:
            return Response({'detail': 'Your token has been expired.'}, status=status.HTTP_400_BAD_REQUEST)
        # if token is invalid
        except InvalidSignatureError:
            return Response({'detail': 'Your token is not valid.'}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk = user_id)
        # if user is already verified
        if user_obj.is_verified:
            return Response({'detail': 'Your account has alreadey been verified.'}, status=status.HTTP_400_BAD_REQUEST)
        user_obj.is_verified = True
        user_obj.is_active = True
        user_obj.save()
        return Response({'detail': 'Your account has been verified and activated successfully.'}, status=status.HTTP_200_OK)
