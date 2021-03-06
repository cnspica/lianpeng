import os
from hashlib import md5

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.db.models import F
from django.dispatch import receiver
from django.conf import settings

from bookmark.models import Bookmark

def snapshot_upload_to(instance, filename):
    bookmark = instance.bookmark
    user_dir = md5(bookmark.user.username + settings.SNAPSHOT_SALT).hexdigest()
    return os.path.join('snapshots', user_dir, filename)


class Snapshot(models.Model):
    bookmark = models.OneToOneField(Bookmark)
    html_file = models.FileField(upload_to=snapshot_upload_to)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        return "/" + self.html_file.name

@receiver(post_save, sender=Bookmark)
def create_snapshot(sender, instance, created, **kwargs):
    try:
        instance.snapshot
    except Snapshot.DoesNotExist:
        no_snapshot = True
    else:
        no_snapshot = False
    if created or no_snapshot:
        from snapshot.tasks import create_snapshot_task
        from market.models import UserApp
        user = instance.user
        is_active = UserApp.objects.is_active(user, 'snapshot')
        if is_active:
            create_snapshot_task.delay(instance)

@receiver(post_delete, sender=Snapshot)
def delete_snapshot_file(sender, instance, **kwargs):
    instance.html_file.delete(save=False)
