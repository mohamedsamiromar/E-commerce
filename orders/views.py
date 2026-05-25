from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import CartService


class CartDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")


class CartAddView(APIView):
    def post(self, request):
        slug = request.data.get('slug')
        if not slug:
            return Response(
                {"message": "slug is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order, message = CartService.add_item(request.user, slug)
        if not order:
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": message}, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    def post(self, request):
        slug = request.data.get('slug')
        if not slug:
            return Response(
                {"message": "slug is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        _, error = CartService.remove_item(request.user, slug)
        if error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
