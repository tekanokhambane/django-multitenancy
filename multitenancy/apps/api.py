from multitenancy.apps.views import TenantViewSet, api_root
from rest_framework import renderers

tenant_list = TenantViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tenant_detail = TenantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
