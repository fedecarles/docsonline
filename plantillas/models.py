from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from taggit.managers import TaggableManager
import time
import uuid


class UserData(models.Model):
    user = models.ForeignKey(User, editable=False)
    creation_date = models.CharField(max_length=30,
                                     default=time.strftime("%d-%m-%Y"))

    class Meta:
        abstract = True


class plantillaModel(UserData, models.Model):

    summernote = models.TextField(max_length=100000, blank=True, null=True,
                                  default="")

    title = models.CharField(max_length=120, default="")

    doc_id = models.CharField(max_length=120, unique=True,
                              default=str(uuid.uuid4())[:10])

    description = models.TextField(max_length=500, null=True, blank=True)

    public = models.IntegerField(default=1)

    tags = TaggableManager()

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    def is_owner(self, user):
        return self.user == user

    def is_private(self, public):
        return self.public == 1

    def __str__(self):
            return str(self.user)
