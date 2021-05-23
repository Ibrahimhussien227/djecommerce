from rest_framework import generics
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_condition import And, Or
from .models import *
from .serializers import ItemSerializer


class IsPostMethod(BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() == 'POST'


class IsSafeMethod(BasePermission):
    def has_permission(self, request, view):
        return request.method.upper() in ('OPTIONS', 'HEAD', 'GET')


class ListItem(generics.ListCreateAPIView):
    permission_classes = [
        Or(
            And(IsPostMethod, IsAdminUser),
            And(IsSafeMethod, IsAdminUser),
        )
    ]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class DetailItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
