from rest_framework.serializers import ModelSerializer, CharField

from .models import Article


class ReadOnlyArticleSerializer(ModelSerializer):
    content = CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Article


class WriteOnlyArticleSerializer(ModelSerializer):
    content = CharField()

    class Meta:
        fields = '__all__'
        model = Article

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        article = super().create(validated_data)
        return article

    def update(self, instance, validated_data):
        article = super().update(instance, validated_data)
        return article
