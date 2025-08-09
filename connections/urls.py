from django.urls import path
from .views import UserSearchView, SendConnectionRequestView, RespondConnectionRequestView, ConnectionRequestsView, SentRequestsView
urlpatterns = [
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('send/<uuid:user_id>/', SendConnectionRequestView.as_view(), name='send-request'),
    path('respond/<int:connection_id>/', RespondConnectionRequestView.as_view(), name='respond-request'),
    path('requests/', ConnectionRequestsView.as_view(), name='connection-requests'),
    path('sent/', SentRequestsView.as_view(), name='sent-requests')
]
