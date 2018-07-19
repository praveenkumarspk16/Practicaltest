from django.shortcuts import render, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.models import Rest_framework
from rest_framework.serializers import RestSerializer
from rest_framework.views import APIView


class RestApi(APIView):

    def get(self, request):
        account = Rest_framework.objects.all()
        serializer = RestSerializer(account, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestApiDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return Rest_framework.objects.get(pk=pk)
        except Rest_framework.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print(request.method)
        account = self.get_object(pk)
        account = RestSerializer(account)
        return Response(account.data)

    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = RestSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = Rest_framework.objects.get(pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
