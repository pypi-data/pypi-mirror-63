from rest_framework.serializers import ModelSerializer
""" Import from Local App. """
from taggit.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
