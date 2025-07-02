from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework import status
from realestateapp.models import UserConnection
from realestateapp.serializers.realestate_user_serializer import SignupSerializer
from realestateapp.serializers.realtor_developer_serializer import RealtorDeveloperConnectionSerializer

User = get_user_model()

class AvailableDevelopersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Sirf approved realtor hi access kare
        if user.role != 'realtor' or not user.is_approved:
            return Response({"detail": "Access denied. Only approved realtors can view developers."}, status=status.HTTP_403_FORBIDDEN)

        developers = User.objects.filter(role='developer', is_approved=True)
        data = [
            {
                "id": dev.id,
                "username": dev.username,  # ya first_name, full_name depending on your model
                "email": dev.email,
                "company_name": dev.company_name

            }
            for dev in developers
        ]
        return Response(data, status=status.HTTP_200_OK)

class SendRequestToDeveloperView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, receiver_id):
        realtor = request.user

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'Developer not found.'}, status=404)

        if UserConnection.objects.filter(realtor=realtor, receiver=receiver).exists():
            return Response({'error': 'Request already sent.'}, status=400)
        
        print("realtor id is..........", realtor.id)

        data = request.data.copy()

        serializer = RealtorDeveloperConnectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(realtor=realtor, receiver=receiver)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class DeveloperRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        receiver = request.user
        requests = UserConnection.objects.filter(receiver=receiver, status='pending')
        serializer = RealtorDeveloperConnectionSerializer(requests, many=True)
        return Response(serializer.data)
    
    def patch(self, request, request_id):
        receiver = request.user
        try:
            try:
                request_obj = UserConnection.objects.get(id=request_id, receiver=receiver)
            except UserConnection.DoesNotExist:
                return Response({'error': 'Request not found.'}, status=404)
            new_statues = request.data.get('status')
            if new_statues not in ['accepted', 'rejected']:
                return Response({'error': 'Invalid status.'}, status=400)
            request_obj.status = new_statues
            request_obj.save()
            serializer = RealtorDeveloperConnectionSerializer(request_obj)
            return Response(serializer.data)
        except UserConnection.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=404)

class AcceptedDevelopersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        realtor = request.user
        accepted_connections = UserConnection.objects.filter(
            realtor=realtor,
            status='accepted'
        )
        receivers = [conn.receiver for conn in accepted_connections]

        # Use a serializer to return developer info (you can customize this)
        serializer = SignupSerializer(receivers, many=True)
        return Response(serializer.data)
