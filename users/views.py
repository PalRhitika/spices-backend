from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserResgistrationSeriallizer


class UserRegistrationView(APIView):
  def post(self,request,*args,**kwargs):
    try:
      serializer=UserResgistrationSeriallizer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response({'msg':"User registered Successfully"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

