from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
import datetime

class TaskView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            if request.headers.get('Accept') == 'application/json':
                tasks = Task.objects.all()
                serializer = TaskSerializer(tasks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return render(request, 'task.html')
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['creator'] = request.user.pk
        request.data['status'] = 'Assigned'
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if request.data['status'] == 'Closed' and not (task.creator == request.user or task.assigned_to == request.user or request.user.is_superuser):
            return Response({'error': 'You do not have permission to edit this task'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['last_updated_by'] = request.user
            serializer.validated_data['updated_at'] = datetime.datetime.now()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        if task.creator != request.user and not request.user.is_superuser:
            return Response({'error': 'You do not have permission to delete this task'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
