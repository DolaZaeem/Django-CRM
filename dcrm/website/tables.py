from django_tables2 import Table, Column
from .models import Record

class YourModelTable(Table):
    class Meta:
        model = Record
        fields = ('id', 'first_name', 'last_name')