"""Coupon management Views"""

from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import ListCreateAPIView, ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Coupon
from .serializers import CouponSerializer, UserSerializer, LoginSerializer, User


# Create your views here.

class RegisterView(CreateAPIView):
    """Registers a new user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(GenericAPIView):
    """Logs in a user and returns a JWT token."""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)

            return Response({'token': str(refresh.access_token)})
        
        return Response({'status': 401, 'error': 'Invalid Credentials'})
    

class CouponCreateView(ListCreateAPIView):
    """Allows admin users to create and list coupons."""

    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponSearchView(ListAPIView):
    """Allows authenticated users to search for coupons by company name."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    serializer_class = CouponSerializer

    def get_queryset(self):

        company_name = self.request.query_params.get('company_name', None)
        if company_name:
            # Filter coupons based on company name
            return Coupon.objects.filter(company_name__icontains=company_name)
        
        return Coupon.objects.none()
    
class CouponAvailView(GenericAPIView):
    """Checks and updates coupon availability (authenticated users)."""

    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):

        coupon_id = request.data.get('coupon_id')
        try:
            coupon = Coupon.objects.get(id=coupon_id)

            # Decrement availability if coupon is available
            if coupon.availability > 0:
                coupon.availability -= 1
                coupon.save()

                return Response(CouponSerializer(coupon).data)
            else:

                return Response({"status": 400, 'error': 'Coupon is no longer available'})
        except Coupon.DoesNotExist:

            return Response({'status': 404,'error': 'Coupon not found'})

    


