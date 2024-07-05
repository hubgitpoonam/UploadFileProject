from django.shortcuts import render

# Create your views here.
# uploader/views.py
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
