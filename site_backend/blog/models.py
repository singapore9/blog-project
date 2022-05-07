from django.db import models


class Article(models.Model):
    cover_image = models.ImageField(upload_to='covers', null=True)
    main_image = models.ImageField(upload_to='main', null=True)
    content = models.TextField()

    def __str__(self):
        return self.content and self.content[:50]
