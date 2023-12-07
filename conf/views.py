from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def get_or_None(model,**kwargs):
    try:
        my_object = model.objects.get(**kwargs)
    except model.DoesNotExist:
        my_object = None
    return my_object

class AuthModelViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]

    @property
    def data(self):
        request=self.request
        data={}
        if type(request.data)==dict:
            data=dict(request.data)
        else:
            data={key: None if value == 'null' else value for key, value in request.data.items()}
        data['user']=self.get_user().id
        return data

    def get_user(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
      
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
