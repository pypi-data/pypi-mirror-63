from djangoarticle.models import CategoryModelScheme


def CategoryUniversalContext(request):
    djangoarticle_category = CategoryModelScheme.objects.filter_publish()
    return {"djangoarticle_category": djangoarticle_category}