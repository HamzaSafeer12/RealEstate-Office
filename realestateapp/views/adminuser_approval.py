from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from realestateapp.models import CustomUser
from django.core.mail import send_mail
from realestateapp.task import send_approval_email_task
from realestateapp.serializers.realestate_user_serializer import SignupSerializer


# def send_approval_email(user_email):
#     subject = "Approval Notification"
#     message = "Congratulations! Your account has been approved by admin. You can now log in and use the platform."
#     from_email = 'yourgmail@gmail.com'
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)

class AdminUserApprovalView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            print("user id is",user_id)
            user = CustomUser.objects.get(id=user_id)
            data = {
                "id": user.id,
                "email": user.email,
                "name": user.username,
                "role": user.role,
                "is_approved": user.is_approved
            }
            return Response(data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_approved = True
            user.save()
            # send_approval_email(user.email)
            send_approval_email_task.delay(user.email)  # <-- yahan .delay() use karna
            return Response({"message": "User approved and email sent successfully."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found or already approved."}, status=status.HTTP_404_NOT_FOUND)

