from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from user.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from user.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, ChangePasswordSerializer
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] ={
            'uid': self.kwargs['uid'],
            'token': self.kwargs['token']
        }

        return serializer_class(*args, **kwargs)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User with this email does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        id = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uidb64': id, 'token': token})
        )

        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_url}',
            'from@example.com',
            [email]
        )

        return Response(status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_str(urlsafe_base64_decode(uidb64))
        new_password = serializer.validated_data['new_password']

        try:
            user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)