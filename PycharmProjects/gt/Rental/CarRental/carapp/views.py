from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializer import UserSerializer,CarSerializer

from .models import CarDb
from rest_framework import authentication, permissions

from .models import CarDb, RentalDb
from .serializer import UserSerializer, CarSerializer, RentalSerializer
from rest_framework import authentication, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError

# Create your views here.

class UserSignUp(APIView):
    def post(self,request):
        serializer_instance = UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"User Registered Successfully",
                "data":serializer_instance.data
            })
        return Response(serializer_instance.errors)

    def get(self,request):
        users = User.objects.all()
        serializer_instance = UserSerializer(users,many=True)
        return Response(serializer_instance.data)


class CarManagement(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        serializer_instance = CarSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"Car Added Successfully",
                             "details":serializer_instance.data})
        return Response(serializer_instance.errors)

    def get(self,request):
        cars = CarDb.objects.all()
        serializer_instance = CarSerializer(cars,many=True)
        return Response(serializer_instance.data)

    def put(self,request,id):
        car = get_object_or_404(CarDb,id=id)
        if car.created_by != request.user:
            serializer_instance = CarSerializer(car,data=request.data)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data=serializer_instance.data)
            return Response(data=serializer_instance.errors)

    def delete(self,request,id):

        car = get_object_or_404(CarDb,id=id)
        car.delete()
        return Response(data={"message":"Car Deleted Successfully..."})


class RentalManagement(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rentals = RentalDb.objects.filter(customer=request.user)
        serializer_instance = RentalSerializer(rentals, many=True)
        return Response(serializer_instance.data)

    def post(self, request):
        serializer_instance = RentalSerializer(data=request.data)

        if serializer_instance.is_valid():
            car = serializer_instance.validated_data['car']
            start_date = serializer_instance.validated_data['start_date']
            end_date = serializer_instance.validated_data['end_date']

            if start_date > end_date:
                return Response({"message": "Invalid rental dates"})

            if not car.is_avilable:
                return Response({"message": "Car is not available"})

            if RentalDb.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exists():
                return Response({"message": "Car is already booked"})

            days = (end_date - start_date).days + 1
            total_amount = days * car.rent_per_day

            serializer_instance.save(
                customer=request.user,
                total_amount=total_amount
            )

            return Response({
                "message": "Rental Booked Successfully",
                "details": serializer_instance.data
            })

        return Response(serializer_instance.errors)

    def put(self, request, id):
        rental = get_object_or_404(RentalDb, id=id)

        if rental.customer != request.user:
            raise PermissionDenied("Access Denied")

        serializer_instance = RentalSerializer(
            rental,
            data=request.data
        )

        if serializer_instance.is_valid():
            car = serializer_instance.validated_data['car']
            start_date = serializer_instance.validated_data['start_date']
            end_date = serializer_instance.validated_data['end_date']

            if start_date > end_date:
                return Response({"message": "Invalid rental dates"})

            if not car.is_avilable:
                return Response({"message": "Car is not available"})

            if RentalDb.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exclude(id=id).exists():
                return Response({"message": "Car is already booked"})

            days = (end_date - start_date).days + 1
            total_amount = days * car.rent_per_day

            serializer_instance.save(
                customer=request.user,
                total_amount=total_amount
            )

            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)

    def delete(self, request, id):
        rental = get_object_or_404(RentalDb, id=id)

        if rental.customer != request.user:
            raise PermissionDenied("Access Denied")

        rental.delete()

        return Response(
            {"message": "Rental Deleted Successfully"}
            
        )
