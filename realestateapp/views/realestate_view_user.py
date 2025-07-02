from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from realestateapp.serializers.realestate_user_serializer import SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from realestateapp.serializers.realestate_user_serializer import CustomTokenObtainPairSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data.get('role')
            try:
                if role == 'Investor' or role == 'investor':
                    serializer.save(is_approved=True)
                    message = "User registered successfully. You can now log in."
                else:  # Developer or Realtor
                    serializer.save()  # is_approved=False by default
                    message = "User registered successfully. Please wait for admin approval. You will receive an email once approved."

                return Response({"message": message}, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Optional: log the exception for debugging (e.g. logger.error(str(e)))
                return Response(
                    {"error": "Something went wrong while creating the user."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


