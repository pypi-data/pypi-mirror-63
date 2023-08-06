from django.conf.urls import re_path, include
""" Import from Local App. """
from djangotags.rest_api import viewsets


urlpatterns = [
    re_path(r'^list/$', viewsets.TagListViewSet.as_view(), name="tag_list_viewset"),
    re_path(r'^detail/(?P<tag_slug>[\w-]+)/$', viewsets.TagRetrieveViewSet.as_view(), name="tag_retrieve_viewset"),
    re_path(r'^update/(?P<tag_slug>[\w-]+)/$', viewsets.TagUpdateViewSet.as_view(), name="tag_update_viewset"),
    re_path(r'^delete/(?P<tag_slug>[\w-]+)/$', viewsets.TagDestroyViewSet.as_view(), name="tag_destroy_viewset")
]