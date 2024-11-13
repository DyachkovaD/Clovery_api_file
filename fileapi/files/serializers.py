from rest_framework import serializers
import uuid


class FileSerializer(serializers.Serializer):
    project_id = serializers.CharField(max_length=36)
    profile_id = serializers.CharField(max_length=36)
    account_id = serializers.CharField(max_length=36)

    file = serializers.FileField()
    type = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    size = serializers.IntegerField(read_only=True)


    def validate_file(self, file):

        # Если пытаются сделать post-запрос без файла
        if not file:
            raise serializers.ValidationError('Вы не передали файл')

        # Проверяем тип файла (тут типы для примера, список можно пополнять)
        if file.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
            raise serializers.ValidationError('Неподдерживаемый тип файла')
        return file

    def create(self, validated_data):
        file = validated_data['file']
        type_ = file.content_type
        name = file.name
        size = file.size

        project_id = self.context['request'].headers.get('project_id')
        profile_id = self.context['request'].headers.get('profile_id')
        account_id = self.context['request'].headers.get('account_id')

        # Сохраняем информацию о файле в реестре (FileInfo - потенциальное название реестра)
        file_instance = FileInfo.objects.create(
            file_id=str(uuid.uuid4()),
            project_id=project_id,
            profile_id=profile_id,
            account_id=account_id,
            item=profile_id,
            file_type=type_,
            meta='ACTIVE',
            data={
                'name': name,
                'size': size,
                'path': None,
                'url': None
            }
        )

        return file_instance
