from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from realestateapp.serializers.property_serializer import PropertySerializer, PropertyTypeSerializer, SubPropertyTypeSerializer
from realestateapp.models import Property, PropertyType, SubPropertyType, UserConnection
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()
class PropertyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # --- If user is Developer ---
        if user.role == 'developer':
            if not user.is_approved:
                return Response({'error': 'You are not an approved developer.'}, status=400)
            
            serializer = PropertySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(developer=user)  # realtor = None
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        # --- If user is Realtor ---
        elif user.role == 'realtor':
            developer_id = request.data.get('developer')
            print("developer id is----------------------------------------------------", developer_id)
            if not developer_id:
                return Response({'error': 'Developer ID is required.'}, status=400)

            try:
                developer = User.objects.get(id=developer_id, role='developer', is_approved=True)
            except User.DoesNotExist:
                return Response({'error': 'Developer not found or not approved.'}, status=404)

            # Check connection
            if not UserConnection.objects.filter(
                realtor=user, receiver=developer, status='accepted'
            ).exists():
                return Response({'error': 'You are not connected with this developer.'}, status=403)

            serializer = PropertySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(developer=developer, realtor=user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        else:
            return Response({'error': 'Unauthorized role.'}, status=403)


class PropertyTypeCreateAPIView(generics.CreateAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class SubPropertyTypeCreateAPIView(generics.CreateAPIView):
    queryset = SubPropertyType.objects.all()
    serializer_class = SubPropertyTypeSerializer

class PropertyListing(APIView):
    def post(self, request):
        # Get all properties initially
        properties = Property.objects.all()      
        # Get filter parameters from request body
        filters = request.data
        
        # Create filter query
        if filters:
            filter_query = Q()
            
            # Handle city filter
            if 'city' in filters and filters['city']:
                filter_query &= Q(city__icontains=filters['city'])
            
            # Handle location filter
            if 'location' in filters and filters['location']:
                filter_query &= Q(location__icontains=filters['location'])
            
            # Handle price range filter
            if 'price_min' in filters and filters['price_min']:
                filter_query &= Q(price__gte=filters['price_min'])
            if 'price_max' in filters and filters['price_max']:
                filter_query &= Q(price__lte=filters['price_max'])
            
            # Handle property_type filter
            if 'property_type' in filters and filters['property_type']:
                filter_query &= Q(property_type=filters['property_type'])
            
            # Handle sub_property_type filter
            if 'sub_property_type' in filters and filters['sub_property_type']:
                filter_query &= Q(sub_property_type=filters['sub_property_type'])
            
            # Handle beds filter
            if 'beds' in filters and filters['beds']:
                filter_query &= Q(beds=filters['beds'])
            
            # Handle baths filter
            if 'baths' in filters and filters['baths']:
                filter_query &= Q(baths=filters['baths'])
            
            # Handle area range filter
            if 'area_min' in filters and filters['area_min']:
                filter_query &= Q(area__gte=filters['area_min'])
            if 'area_max' in filters and filters['area_max']:
                filter_query &= Q(area__lte=filters['area_max'])
            
            # Handle area_unit filter
            if 'area_unit' in filters and filters['area_unit']:
                filter_query &= Q(area_unit=filters['area_unit'])
            
            # Handle category filter
            if 'category' in filters and filters['category']:
                filter_query &= Q(category=filters['category'])
            
            # Handle developer filter
            if 'developer' in filters and filters['developer']:
                filter_query &= Q(developer=filters['developer'])
            
            # Apply all filters to queryset
            properties = properties.filter(filter_query)
        
        # Paginate results if needed
        page_size = int(request.query_params.get('page_size', 4))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        # Count total properties that match the filters
        total_count = properties.count()
        
        # Apply pagination
        properties = properties[start:end]
        
        # Serialize the data
        serializer = PropertySerializer(properties, many=True)
        
        # Return response with pagination info
        return Response({
            'count': total_count,
            'current_page': page,
            'page_size': page_size,
            'results': serializer.data
        })