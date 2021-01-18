from django.db.models import F, Sum, Count, Case, When, Value
from django.db import transaction
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Deal, Customer
from .serializers import CustInfoSerializer, DealCreateSerializer

import itertools
from collections import namedtuple

# Create your views here.


class CustomerInfoView(APIView):

    def get(self, request):
        cust_ids = Customer.objects.annotate(
                        deals_sum=Sum(F('deals__total') * F('deals__quantity'))
                        ).order_by('-deals_sum')[:5].values('name')

        item_ids = Deal.objects.values('item__name').filter(
                        customer__name__in=cust_ids
                        ).annotate(
                        cnt=Count('customer__name', distinct=True)
                        ).filter(cnt__gte=2).values('item__name')

        target = Deal.objects.values('customer__name').annotate(
                        deals_sum=Sum(F('total') * F('quantity'))
                        ).annotate(
                        gems=ArrayAgg(
                            Case(
                              When(item__name__in=item_ids, then='item__name'),
                              default=Value('')), distinct=True)
                        ).order_by('-deals_sum')[:5]
        ser = CustInfoSerializer(target, many=True)
        return Response({"response": ser.data})


class FileUploadView(APIView):

    def post(self, request):
        file_obj = request.FILES.get('deals', None)
        if file_obj:
            errors = []
            Deal = namedtuple('Deal', file_obj.readline().decode())
            
            for ind, line in enumerate(itertools.islice(file_obj, 1, None)):
                data = Deal._make(line.strip().decode().split(','))._asdict()
                deal = DealCreateSerializer(data=data)
                if deal.is_valid():
                    deal.save()
                else:
                    tmp = deal.errors
                    tmp.update((('rownum', ind+2),))
                    errors.append(tmp)

            if errors:
                return Response(errors,
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            content = {'Error': "CSV file wasn't sent."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
