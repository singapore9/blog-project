from django.db import models


class Article(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content and self.content[:50]
