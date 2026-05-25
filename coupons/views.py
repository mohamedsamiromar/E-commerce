from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from coupons.services import CouponService


class ApplyCouponView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {"message": "Coupon code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order, error = CouponService.apply_coupon(request.user, code)
        if error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Coupon applied successfully"}, status=status.HTTP_200_OK)
