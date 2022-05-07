from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('content', )
    fields = ('content', 'cover_image', 'main_image', )


admin.site.register(Article, ArticleAdmin)
