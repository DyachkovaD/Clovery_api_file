from django.db import models
import uuid


class ImageInfo(models.Model):
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.UUIDField()
    profile_id = models.UUIDField()
    account_id = models.UUIDField()
    data = models.JSONField()

    def __str__(self):
        return str(self.file_id)