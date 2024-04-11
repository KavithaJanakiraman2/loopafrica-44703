from django.urls import path
from .views import InitializeTransactionViewSet, SubscriptionViewSet, PaystackCustomerViewSet

urlpatterns = [
    path('initialize-transaction/', InitializeTransactionViewSet.as_view({'post':'create'}), name='initialize_transaction'),
    path('create-subscription/', SubscriptionViewSet.as_view({'post': 'create'}), name='create_subscription'), 
    path('list-subscriptions/', SubscriptionViewSet.as_view({'get': 'list'}), name='list_subscriptions'),
    path('create-customer/', PaystackCustomerViewSet.as_view({'post': 'create'}), name='create_paystack_customer'),  
    path('retrieve-customer/<str:email_or_code>/', PaystackCustomerViewSet.as_view({'get': 'retrieve'}), name='retrieve_paystack_customer'),
    path('update-customer/<str:code>/', PaystackCustomerViewSet.as_view({'put': 'update_customer'}), name='update_paystack_customer'),
]


