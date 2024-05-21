from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import CRMTrucks, PostalCodeInfo
from .serializers import CRMTrucksSerializer, CRMPostalCodeInfoSerializer


class CRMTrucksViewSet(viewsets.ModelViewSet):
    queryset = CRMTrucks.objects.all()
    serializer_class = CRMTrucksSerializer

    # Метод для получения списка объектов (GET)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Метод для получения конкретного объекта (GET)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Метод для создания нового объекта (POST)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Метод для обновления объекта (PUT)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # Метод для частичного обновления объекта (PATCH)
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # Метод для удаления объекта (DELETE)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CRMPostalCodeInfoViewSet(viewsets.ModelViewSet):
    queryset = PostalCodeInfo.objects.all()
    serializer_class = CRMPostalCodeInfoSerializer
