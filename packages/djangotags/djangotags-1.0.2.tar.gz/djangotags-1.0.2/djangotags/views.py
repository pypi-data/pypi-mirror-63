from itertools import chain
from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView
""" Import from External Apps. """
from taggit.models import Tag
from djangopost.models import ArticleModel
from djangoarticle.models import ArticleModelScheme


# Create your homepage views here.
class TaggitTagDetailView(DetailView):
    template_name = "djangoadmin/djangotags/taggit_tag_detail_view.html"
    model = Tag
    slug_url_kwarg = "tag_slug"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lookup_instance = self.kwargs['tag_slug']
        context['article_filter'] = ArticleModel.objects.published().filter(tags__slug=lookup_instance)
        context['is_promoted'] = ArticleModelScheme.objects.published().filter(tags__slug=lookup_instance)
        post_promo = ArticleModel.objects.promo()
        article_promo = ArticleModelScheme.objects.promo()
        context['promo'] = chain(post_promo, article_promo)
        post_trending = ArticleModel.objects.promo()
        article_trending = ArticleModelScheme.objects.promo()
        context['is_trending'] = chain(post_trending, article_trending)
        return context
