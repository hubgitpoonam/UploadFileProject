from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Upload 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from  uploader.serializer import UploadSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    
    def post(self, request, *args, **kwargs):
        
        user = request.user  
        print(user,"user")
        files = request.FILES.getlist('file')
        total_size = sum(file.size for file in files)
        limit_mb = 20

        if total_size > limit_mb * 1024 * 1024:
            return Response({"error": f"Total file size exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)
        
        for file in files:
            if file.size > limit_mb * 1024 * 1024:  # 20MB limit
                return Response({"error": f"File {file.name} exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UploadSerializer(data={'file': file,'user': user.id})
            if serializer.is_valid():
                serializer.save(user=user)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
          

        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)
    

    def put(self, request, id, *args, **kwargs):
        try:
            update_file = Upload.objects.get(id=id,user=request.user)
        except Upload.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user  
        print(user,"user")
        # Calculate total size of files being updated
        files = request.FILES.getlist('file')
        total_size = sum(file.size for file in files) if files else 0
        
        limit_mb = 20

        if total_size > limit_mb * 1024 * 1024:
            return Response({"error": f"Total file size exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)

        # Update each file individually
        for file in files:
            if file.size > limit_mb * 1024 * 1024:  # 20MB limit
                return Response({"error": f"File {file.name} exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)

            file_serializer = UploadSerializer(update_file, data={'file': file})
            if file_serializer.is_valid():
                file_serializer.save(user=user)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "File(s) updated successfully",
            "data": file_serializer.data
        }, status=status.HTTP_200_OK)
    
    def get(self, request, id=None, *args, **kwargs):
        user = request.user
        if id:
            try:
                file = Upload.objects.get(id=id, user=user, is_deleted=False)
                file_serializer = UploadSerializer(file)
                return Response(file_serializer.data, status=status.HTTP_200_OK)
            except Upload.DoesNotExist:
                return Response({"message": "uploaded file not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            all_files = Upload.objects.filter(user=user, is_deleted=False)
            all_files_serializer = UploadSerializer(all_files, many=True)
            return Response(all_files_serializer.data, status=status.HTTP_200_OK)

    def list(request,id=None):
        if request.method == "GET":
            user = request.user
            
            try:
                all_files = Upload.objects.filter(user=user)
                
                allFiles_serializer = UploadSerializer(all_files, many=True)
                return JsonResponse(allFiles_serializer.data, safe=False)
            except Upload.DoesNotExist:
                return JsonResponse({"message": "uploaded file not found"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  

    def delete(self, request, id=None, *args, **kwargs):
        user = request.user
        if id:
            try:
                file = Upload.objects.get(id=id, user=user, is_deleted=False)
                file.is_deleted = True  #soft delete
                file.save()
                return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Upload.DoesNotExist:
                return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
