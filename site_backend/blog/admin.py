from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('content', )
    fields = ('content', )


admin.site.register(Article, ArticleAdmin)
