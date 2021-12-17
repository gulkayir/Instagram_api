import os
import uuid

from django.conf import settings
from django.db import models

def story_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('stories/', filename)


class Story(models.Model):

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_story",
                               on_delete=models.CASCADE, )

    posted_on = models.DateTimeField(auto_now_add=True)

    story_image = models.ImageField(upload_to=story_file_path,
                                    default='story.png')

    views = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="story_viewers",
                                   blank=True,
                                   symmetrical=False)

    tagged = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="story_tagged",
                                    blank=True,
                                    symmetrical=False)

    def number_of_views(self):
        if self.views.count():
            return self.views.count()
        else:
            return 0

    def number_of_tags(self):
        if self.tagged.count():
            return self.tagged.count()
        else:
            return 0

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.author}\'s story'