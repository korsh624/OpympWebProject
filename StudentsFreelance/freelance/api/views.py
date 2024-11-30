from rest_framework.views import APIView, Response
from rest_framework import status

from .serializers import CommentSerializer, OrderSerializer


class AddCommentsView(APIView):

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)


class AddOrderView(APIView):

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'OK'}, status=status.HTTP_201_CREATED)