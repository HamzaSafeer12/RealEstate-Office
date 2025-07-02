# realestateapp/urls.py
from django.urls import path
from django.conf.urls.static import static
from realestate import settings
from realestateapp.views.realestate_view_user import SignupView , CustomLoginView # ya signup function agar function-based use kar raha
from realestateapp.views.adminuser_approval import AdminUserApprovalView
from realestateapp.views.property_view import PropertyCreateAPIView, PropertyListing, PropertyTypeCreateAPIView, SubPropertyTypeCreateAPIView
from realestateapp.views.realtor_view import AvailableDevelopersAPIView, SendRequestToDeveloperView, DeveloperRequestsView,AcceptedDevelopersView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'), 
    path('login/', CustomLoginView.as_view(), name='custom_login'), # for APIView
    path('admin/user/<int:user_id>/', AdminUserApprovalView.as_view(), name='user-approval'),
    path('developer/properties/create/', PropertyCreateAPIView.as_view(), name='developer-property-create'),
    path('properties/', PropertyListing.as_view(), name='property-listing'),
    path('property-types/add/', PropertyTypeCreateAPIView.as_view(), name='add-property-type'),
    path('sub-property-types/add/', SubPropertyTypeCreateAPIView.as_view(), name='add-sub-property-type'),
    path('realtors/available-developers/', AvailableDevelopersAPIView.as_view(), name='available-developers'),
    path('realtor/send-request/<int:receiver_id>/', SendRequestToDeveloperView.as_view(), name='send-request'),
    path('developer/view-requests/', DeveloperRequestsView.as_view(), name='developer-view-requests'),
    path('developer/approve-request/<int:request_id>/', DeveloperRequestsView.as_view(), name='developer-approve-request'),
    path('realtor/accepted-developers/', AcceptedDevelopersView.as_view(), name='realtor-accepted-developers'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)