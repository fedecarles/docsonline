from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from taggit.managers import TaggableManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
import uuid


class userProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    website = models.CharField(max_length=100, blank=True, null=True)
    lugar = models.CharField(max_length=50, blank=True, null=True)
    firma = models.ImageField(upload_to='signatures', default='',
                              blank=True, null=True)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = userProfile.objects.get_or_create(user=instance)


class plantillaModel(models.Model):

    creation_date = models.CharField(max_length=30,
                                     default=time.strftime("%d-%m-%Y"))

    user = models.ForeignKey(User, editable=False, related_name="user")

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



