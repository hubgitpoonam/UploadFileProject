from django.http import JsonResponse
from django.shortcuts import render
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
        for file in files:
            if file.size > 20 * 1024 * 1024:  # 20MB limit
                return Response({"error": "File too large"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UploadSerializer(data={'file': file})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)
    


    
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
@api_view(['PUT'])
def UpdateFile(request, id=None):
    if request.method == 'PUT':
        try:
            update_file = Upload.objects.get(id=id)
        except Upload.DoesNotExist:
            return JsonResponse({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
        file_serializer = UploadSerializer(update_file, data=request.data, partial=True)
        if file_serializer.is_valid():
            file_serializer.save()
            return JsonResponse({
                "message": "File updated successfully",
                "data": file_serializer.data
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            "message": "Failed to update file",
            "errors": file_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
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