from .views import InvoiceViewSet

invoice_list = InvoiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
invoice_detail = InvoiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
