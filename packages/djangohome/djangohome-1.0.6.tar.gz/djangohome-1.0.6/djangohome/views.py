from itertools import chain
from django.shortcuts import render
from django.views.generic import ListView
""" Import from External Apps. """
from djangopost.models import ArticleModel
from djangoarticle.models import ArticleModelScheme


# Create your homepage views here.
class HomePageView(ListView):
    template_name = "djangoadmin/djangohome/homepage_view.html"
    model = ArticleModel
    slug_url_kwarg = "tag_slug"
    context_object_name = "article_filter"

    def get_queryset(self):
        return ArticleModel.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_promoted'] = ArticleModelScheme.objects.published()
        post_promo = ArticleModel.objects.promo()
        article_promo = ArticleModelScheme.objects.promo()
        context['promo'] = chain(post_promo, article_promo)
        post_trending = ArticleModel.objects.promo()
        article_trending = ArticleModelScheme.objects.promo()
        context['is_trending'] = chain(post_trending, article_trending)
        return context