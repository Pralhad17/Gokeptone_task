from rest_framework import generics, status, viewsets, filters
from .serializers import RegisterSerializer, TaskSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
import django_filters
from django.db import models 
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth import get_user_model
from django_filters import rest_framework as django_filters




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow task owners or admins to edit or view tasks.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can view or edit any task
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Normal users can only view/edit their own tasks
        return obj.user == request.user
    
class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.CharFilter(field_name='priority', lookup_expr='icontains')
    due_date = django_filters.DateFilter(field_name='due_date')
    search = django_filters.CharFilter(method='filter_by_search')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date']

    def filter_by_search(self, queryset, name, value):
        # Search tasks by title or description
        return queryset.filter(models.Q(title__icontains=value) | models.Q(description__icontains=value))


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        """Restrict tasks so that normal users can only see their own tasks."""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        """Assign the task to the currently authenticated user for normal users."""
        if self.request.user.is_staff or self.request.user.is_superuser:
            user = get_user_model().objects.get(id=self.request.data['user_id'])
            task = serializer.save(user=user)
        else:
            task = serializer.save(user=self.request.user)

        # Return a custom response message
        return Response({
            'message': 'Task created successfully.',
            'task': TaskSerializer(task).data
        }, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """Ensure that only admins can change the task's user assignment."""
        if self.request.user.is_staff or self.request.user.is_superuser:
            task = serializer.save()
        else:
            if serializer.instance.user != self.request.user:
                raise PermissionDenied("You cannot edit another user's task.")
            task = serializer.save()

        # Return a custom response message
        return Response({
            'message': 'Task updated successfully.',
            'task': TaskSerializer(task).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Only allow admins or the task owner to delete a task."""
        task = self.get_object()
        if task.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You cannot delete another user's task.")
        
        # Delete the task and return a message
        task.delete()
        return Response({
            'message': 'Task deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)



# Custom serializer (optional if you want to customize the token response)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token here (e.g., user role)
        token['username'] = user.username
        # Add other custom claims if necessary

        return token

# Custom login view
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({
                'access': response.data['access'],
                'refresh': response.data['refresh'],
                'user': {
                    'username': request.user.username,
                    # Add any other user info here if needed
                }
            })
        return response


