from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializer import TaskSerializer,UserSerializer
from .models import TaskDb

from rest_framework import permissions,authentication


# Create your views here.
class Usersignup(APIView):

    def post(self,request):
        serializer_instance = UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "message":"User created Sucessfully",
                "details":serializer_instance.data
            })
        return Response(data=serializer_instance.errors)
    
    def get(self,request):
        users = User.objects.all()
        serializer_instance = UserSerializer(users,many=True)
        return Response(data=serializer_instance.data)



class ListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self,request):
        serializer_instance = TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data={
                "message":"Task Created Successfully",
                "details":serializer_instance.data
            })
        return Response(data={
            "message":serializer_instance.errors
        })

    def get(self,request):
        task = TaskDb.objects.filter(user=request.user)
        serializer_instance = TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)

class TaskRetrieveUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def put(self,request,id):
        task = get_object_or_404(TaskDb,id=id)
        seriailzer_instance = TaskSerializer(task,data=request.data)
        if seriailzer_instance.is_valid():
            seriailzer_instance.save()
            return Response(data=seriailzer_instance.data)
        return Response(data=seriailzer_instance.errors)
    
    def get(self,request,id):
            task = get_object_or_404(TaskDb,id=id)
            seriailzer_instance = TaskSerializer(task,data=request.data)
            if seriailzer_instance.is_valid():
                seriailzer_instance.save()
                return Response(data=seriailzer_instance.data)
            return Response(data=seriailzer_instance.errors)

    def delete(self,request,id):
        task = get_object_or_404(TaskDb,id=id)
        task.delete()
        return Response(data={
            "message":"task Deleted Successfully"
        })


