
from rest_framework.response import Response
from .serializers import TaskSerializer
from ...models import Task 
# or instead of ...models you can point models.py like this: todo.models
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated
from accounts.models import Profile

# class-based views for api
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        # define the queryset wanted
        profile = Profile.objects.get(user=self.request.user.id)
        queryset = Task.objects.filter(user=profile.id)
        return queryset
"""   
class TaskList(ListCreateAPIView):
    # list of tasks and create a new one
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        # define the queryset wanted
        profile = Profile.objects.get(user=self.request.user.id)
        queryset = Task.objects.filter(user=profile.id)
        return queryset
class TaskDetail(RetrieveUpdateDestroyAPIView):
    # show a single task and edit or delete it
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_queryset(self):
        # define the queryset wanted
        profile = Profile.objects.get(user=self.request.user.id)
        queryset = Task.objects.filter(user=profile.id)
        return queryset
"""

    
"""
# list of tasks and create a new one
class TaskList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    
    def get(self, request, *args, **kwargs):
        # retrieve a list of tasks
        profile = Profile.objects.get(user=self.request.user.id)
        tasks = Task.objects.filter(user=profile.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        # creating a new task with the given data

        # automatically detect user
        profile = Profile.objects.get(user=self.request.user.id)
        request.data['user'] = profile.id

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
"""        


"""
# show a single task and edit or delete it
class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, id):
        # retrieve the task data
        profile = Profile.objects.get(user=request.user.id)
        task = get_object_or_404(Task, pk=id , user=profile.id)
        serializer = self.serializer_class(task)
        return Response(serializer.data)
    
    def put(self, request, id):
        # edit the task data
        profile = Profile.objects.get(user=request.user.id)
        task = get_object_or_404(Task, pk=id , user=profile.id)
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        # delete the task object
        profile = Profile.objects.get(user=request.user.id)
        task = get_object_or_404(Task, pk=id , user=profile.id)
        task.delete()
        return Response({'detail':'item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
""" 


#  Example for Function-Based View
"""
from rest_framework.decorators import api_view ,permission_classes

 # list of tasks and create a new one
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def taskList(request):
    profile = Profile.objects.get(user=request.user.id)
    if request.method == 'GET':
        tasks = Task.objects.filter(user=profile.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# show a single task and edit or delete it
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def taskDetail(request,id):
    # check if the task is for a specific user or not
    profile = Profile.objects.get(user=request.user.id)
    task = get_object_or_404(Task, pk=id , user=profile.id)
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        task.delete()
        return Response({'detail':'item deleted successfully'}, status=status.HTTP_204_NO_CONTENT) 
"""
