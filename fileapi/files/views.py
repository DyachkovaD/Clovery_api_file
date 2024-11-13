from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileSerializer


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FileView(APIView):
    pagination_class = ResultsSetPagination

    def post(self, request):

        if not request.data:
            return Response({'error': 'Запрос не может быть пустым'}, status=400)

        serializer = FileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            file = serializer.validated_data['file']
            file_path = 'media/{}'.format(file.name)
            with open(file_path, 'wb') as f:
                f.write(file.read())

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
