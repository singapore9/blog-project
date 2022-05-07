from rest_framework.serializers import ModelSerializer, CharField, ImageField

from .models import Article


class ReadOnlyArticleSerializer(ModelSerializer):
    content = CharField(read_only=True)
    cover_image = ImageField(read_only=True)
    main_image = ImageField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Article


class WriteOnlyArticleSerializer(ModelSerializer):
    content = CharField(required=False)
    cover_image = ImageField(required=False)
    main_image = ImageField(required=False)

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
