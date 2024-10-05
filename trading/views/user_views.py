from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling all CRUD operations for the User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Custom create logic (e.g., set password hashing, additional validation)
        serializer.save()

    def update(self, request, *args, **kwargs):
        # Custom update logic (you can override this if needed)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Hash password if password is in the data
        if 'password' in request.data:
            instance.set_password(request.data['password'])
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Handles partial updates (PATCH)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Custom delete logic (if you want to handle soft delete or any other logic)
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
