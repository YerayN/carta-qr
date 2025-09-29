from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HelloSerializer


class HelloView(APIView):
    def get(self, request):
        data = {"message": "Hola desde la API!"}
        serializer = HelloSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
