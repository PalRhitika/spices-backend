from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from .models import Connection
from .serializers import ConnectionSerializer, UserSearchSerializer, ConnectionReadSerializer
from users.models import User
from notifications.tasks import send_connection_notification

class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        print(query)
        users = User.objects.filter(
            Q(full_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(email__icontains=query) |
            Q(contact_number__icontains=query)
        ).exclude(id=request.user.id)
        serializer = UserSearchSerializer(users, many=True)
        return Response(serializer.data)

class SendConnectionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            to_user = User.objects.get(user_id=user_id)
            if Connection.objects.filter(from_user=request.user, to_user=to_user).exists():
                return Response({"detail": "Connection request already sent."}, status=status.HTTP_400_BAD_REQUEST)
            connection = Connection.objects.create(from_user=request.user, to_user=to_user)
            return Response(ConnectionSerializer(connection).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)




class RespondConnectionRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, connection_id):
        try:
            connection = Connection.objects.get(id=connection_id, to_user=request.user)
            action = request.data.get('action').upper()
            if action not in ['ACCEPTED', 'REJECTED']:
                return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
            connection.status = action
            connection.save()
            send_connection_notification.delay(connection.from_user.id, connection.to_user.id, action)
            return Response({"detail": f"Connection {action.lower()}."})
        except Connection.DoesNotExist:
            return Response({"detail": "Connection not found."}, status=status.HTTP_404_NOT_FOUND)


class ConnectionRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = Connection.objects.filter(
            to_user=request.user
        )
        serializer = ConnectionReadSerializer(pending_requests, many=True)
        return Response(serializer.data)

class SentRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sent_requests = Connection.objects.filter(from_user=request.user)
        serializer = ConnectionReadSerializer(sent_requests, many=True)
        return Response(serializer.data)
