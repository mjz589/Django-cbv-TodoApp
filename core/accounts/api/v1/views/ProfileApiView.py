from rest_framework import generics
from django.shortcuts import get_object_or_404


from ....models import Profile
from ..serializers import ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# profile
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
