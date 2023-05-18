import json
import operator
import re
from datetime import datetime
from functools import reduce

from django.db.models import Q
from openpyxl import load_workbook

from management.models import Contract
from structures.models import DataStructureRequiredField


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def excel_to_dict_list(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active

    headers = [convert_string(cell.value) for cell in ws[2]]  # Assuming the headers are in the second row
    data = []
    for row in ws.iter_rows(min_row=3):  # Assuming the data starts from the third row
        row_data = {}
        all_none = True
        for header, cell in zip(headers, row):
            # loop through the headers and the row accordingly
            row_data[header] = cell.value
            if cell.value is not None:
                all_none = False
        if all_none:
            break
        data.append(row_data)

    return data


def convert_string_int_to_bool(value):
    """the check if the value is a string or int and returns the bool of it"""
    try:
        # try converting the value to int
        value = int(value)
        if value == 0:
            return False
        elif value == 1:
            return True
    except:
        return False


def convert_string(input_string):
    # Convert capital letters to lowercase
    if not input_string or input_string == "":
        return None
    lowercase_string = input_string.lower()

    # Remove non-alphabetic characters
    cleaned_string = re.sub('[^a-z]', '', lowercase_string)

    return cleaned_string


def query_items(query, item):
    """
    this query list is used to filter item more of like a custom query the return the query set
    :param query:
    :param item:
    :return:
    """
    query_list = []
    query_list += query.split()
    query_list = sorted(query_list, key=lambda x: x[-1])
    query = reduce(
        operator.or_,
        (Q(rent_security=x) |
         Q(rent_security_type=x) |
         Q(option_type_break_purchase_renew=x) |
         Q(option_type_break_purchase_renew=[x]) for x in query_list)
    )
    object_list = item.filter(query).distinct()
    return object_list


def check_required_field_to_management(contract: Contract):
    """
    This checks all the fields in our required field if it is currently in the contract management
    """
    managements = contract.management_set.all()
    required_fields = DataStructureRequiredField.objects.first()
    if not required_fields:
        required_fields = DataStructureRequiredField.objects.create()

    for management in managements:
        for field in required_fields._meta.fields:
            if field.name == 'id' or field.name == "timestamp":
                continue
            if getattr(required_fields, field.name):
                if getattr(management, field.name) is None or getattr(management, field.name) == "":
                    return False, field.name
    return True, None
