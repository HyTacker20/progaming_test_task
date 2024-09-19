from django.core.cache import cache
from rest_framework.response import Response


class CacheResponseMixin:
    cache_timeout = 60 * 60  # duration in seconds

    def get_cache_prefix(self):
        return self.__class__.__name__

    def get_cache_key(self, request):
        cache_prefix = self.get_cache_prefix()
        query_params = request.GET.copy()

        # normalize query parameters
        if 'page' not in query_params:
            query_params['page'] = '1'

        query_string = query_params.urlencode()
        return f"{cache_prefix}:{request.path}?{query_string}"

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(request)
        print(f"Caching response with key: {cache_key}")

        response_data = cache.get(cache_key)
        if response_data:
            return Response(response_data)

        response = super().list(request, *args, **kwargs)

        cache.set(cache_key, response.data, self.cache_timeout)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # clear cache from last page
        self.invalidate_last_page_cache(request)

        return response

    def invalidate_last_page_cache(self, request):
        # get total items after creation
        total_items = self.get_queryset().count()

        # get page size
        page_size = self.paginator.page_size if self.paginator else None

        if page_size:
            # calculate last page number
            last_page = (total_items + page_size - 1) // page_size
            query_params = request.GET.copy()
            query_params['page'] = str(last_page)
        else:
            query_params = request.GET.copy()

        query_string = query_params.urlencode()
        last_page_full_path = f"{request.path}?{query_string}"

        cache_key = f"{self.get_cache_prefix()}:{last_page_full_path}"
        print(f"Invalidating cache with key: {cache_key}")

        cache.delete(cache_key)

    def get_page_size(self, request):
        if hasattr(self, 'paginator') and self.paginator is not None:
            return self.paginator.get_page_size(request)
        return None
