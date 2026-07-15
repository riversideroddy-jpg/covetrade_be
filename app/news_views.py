from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import News

PAGE_SIZE = 12


@api_view(["GET"])
@permission_classes([AllowAny])
def list_news(request):
    category = request.GET.get('category', '').strip()
    search_query = request.GET.get('search', '').strip()
    page = max(1, int(request.GET.get('page', 1) or 1))

    news_query = News.objects.order_by('-is_featured', '-published_at')

    if category:
        news_query = news_query.filter(category=category)

    if search_query:
        news_query = news_query.filter(
            title__icontains=search_query
        ) | news_query.filter(
            summary__icontains=search_query
        ) | news_query.filter(
            content__icontains=search_query
        )

    paginator = Paginator(news_query, PAGE_SIZE)
    total = paginator.count
    total_pages = paginator.num_pages
    page = min(page, total_pages) if total_pages else 1
    page_obj = paginator.get_page(page)

    news_list = []
    for article in page_obj:
        image_url = article.image_url or None
        if not image_url and article.image:
            image_url = article.image.url

        news_list.append({
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category": article.category,
            "source": article.source,
            "author": article.author,
            "published_at": article.published_at.isoformat(),
            "image_url": image_url,
            "tags": article.tags,
            "is_featured": article.is_featured,
            "created_at": article.created_at.isoformat(),
            "updated_at": article.updated_at.isoformat(),
        })

    return Response({
        "results": news_list,
        "total": total,
        "page": page,
        "pages": total_pages,
        "page_size": PAGE_SIZE,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def news_detail(request, news_id):
    """
    Get detailed information about a specific news article
    """
    try:
        article = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response({
            "success": False,
            "error": "News article not found"
        }, status=404)

    # Prefer plain image_url (set by FMP sync), fall back to Cloudinary upload
    image_url = article.image_url or None
    if not image_url and article.image:
        image_url = article.image.url

    return Response({
        "success": True,
        "article": {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category": article.category,
            "source": article.source,
            "author": article.author,
            "published_at": article.published_at.isoformat(),
            "image_url": image_url,
            "tags": article.tags,
            "is_featured": article.is_featured,
            "created_at": article.created_at.isoformat(),
            "updated_at": article.updated_at.isoformat(),
        }
    })
