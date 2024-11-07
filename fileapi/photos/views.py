# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
import uuid
from.models import ImageInfo
from.serializers import ImageInfoSerializer


class ImageInfoView(APIView):
    def post(self, request):
        # забираем информацию с фронта
        image = request.FILES['image']
        # img = Image.open(image)
        project_id = request.headers.get('project_id')
        profile_id = request.headers.get('profile_id')
        account_id = request.headers.get('account_id')
        if not all([project_id, profile_id, account_id]):
            return Response({'error': 'Не все необходимые заголовки присутствуют'}, status=400)
        info = {
            'name': image.name,
            'size': image.size,
            'type': image.content_type,
            'file_id': str(uuid.uuid4()),
            'project_id': project_id,
            'profile_id': profile_id,
            'account_id': account_id
        }

        # Сохраняем изображение на сервере
        default_storage.save(image.name, ContentFile(image.read()))

        # Загружаем информацию о изображении в модель данных
        image_info = ImageInfo.objects.create(
            file_id=info['file_id'],
            project_id=info['project_id'],
            profile_id=info['profile_id'],
            account_id=info['account_id'],
            data={
                'name': info['name'],
                'size': info['size'],
                'type': info['type'],
                'path': None,
                'url': None
            }
        )

        # Возвращаем JSON-ответ с информацией о изображении
        serializer = ImageInfoSerializer(image_info)
        return Response(serializer.data)

    def get(self, request):
        image_id = request.GET.get('image_id')
        if not image_id:
            return Response({'error': 'Не указан идентификатор изображения'}, status=400)

        try:
            image_info = ImageInfo.objects.get(file_id=image_id)
        except ImageInfo.DoesNotExist:
            return Response({'error': 'Изображение не найдено'}, status=404)

        serializer = ImageInfoSerializer(image_info)
        return Response(serializer.data)