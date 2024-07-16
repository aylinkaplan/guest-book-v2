from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Entry
from .serializers import EntrySerializer, UserSerializer
from django.db.models import Subquery, OuterRef, Count, Value, CharField
from rest_framework import status
from django.db.models.functions import Concat


class EntryPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'entries': data,
        })


class EntryListView(ListAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = EntryPagination


class CreateEntryView(CreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


class UserListView(APIView):
    def get(self, request):

        last_entry_subquery = (
            Entry.objects.filter(user=OuterRef('id'))
            .values('subject', 'message')
            .annotate(last_entry=Concat('subject', Value(' | '), 'message', output_field=CharField()))
            .order_by('-created_date')
        )
        users = User.objects.annotate(
            total_messages=Count('entries'),
            last_entry=Subquery(last_entry_subquery.values('last_entry')[:1])
        )
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
