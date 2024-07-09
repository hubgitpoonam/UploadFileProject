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

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        total_size = sum(file.size for file in files)
        limit_mb = 20

        if total_size > limit_mb * 1024 * 1024:
            return Response({"error": f"Total file size exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)
        
        for file in files:
            if file.size > limit_mb * 1024 * 1024:  # 20MB limit
                return Response({"error": f"File {file.name} exceeds {limit_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UploadSerializer(data={'file': file})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)
    

    def put(self, request, id, *args, **kwargs):
        try:
            update_file = Upload.objects.get(id=id)
        except Upload.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
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
                file_serializer.save()
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "File(s) updated successfully",
            "data": file_serializer.data
        }, status=status.HTTP_200_OK)

    
def getFile(request,id=None):
    if request.method == "GET":
        if id is not None:
            try:
                file = Upload.objects.get(id=id)
                file_serializer = UploadSerializer(file)
                return JsonResponse(file_serializer.data, safe=False)
            except Upload.DoesNotExist:
                return JsonResponse({"message": "uploaded file not found"}, status=status.HTTP_404_NOT_FOUND)
            
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def getAllFile(request):
    if request.method == "GET":
        try:
            all_files = Upload.objects.all()
            allFiles_serializer = UploadSerializer(all_files, many=True)
            return JsonResponse(allFiles_serializer.data, safe=False)
        except Upload.DoesNotExist:
            return JsonResponse({"message": "uploaded file not found"}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@csrf_exempt
@api_view(['DELETE'])
def deleteFile(request, id=None):
    if request.method == 'DELETE':
        try:
            file = Upload.objects.get(id=id)
            file.delete()
            return JsonResponse({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Upload.DoesNotExist:
            return JsonResponse({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse({"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)