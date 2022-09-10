from rest_framework.pagination import PageNumberPagination

class PackagePagination(PageNumberPagination):
    page_size = 3
    last_page_strings= 'end'
