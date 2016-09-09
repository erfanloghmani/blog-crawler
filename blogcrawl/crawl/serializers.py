from .models import Blog, Link
from rest_framework import serializers
from rest_framework.reverse import reverse

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    src = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='blog-detail'
    )
    dest = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='blog-detail'
    )
    class Meta:
        model = Link
        fields = ('url', 'src', 'dest', )

class SrcHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'blog-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.dest.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


class DestHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'blog-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.src.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    src_len = serializers.ReadOnlyField(source='out_degree_count')
    dest_len = serializers.ReadOnlyField(source='in_degree_count')

    class Meta:
        model = Blog
        fields = ('url', 'name', 'src_len', 'dest_len', 'coeffition', 'reaching_count')
