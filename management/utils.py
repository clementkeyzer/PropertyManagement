import codecs
import csv
import json
import operator
import re
from datetime import datetime
from functools import reduce
from io import TextIOWrapper

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse
from openpyxl import load_workbook

from management.models import Contract, ManagementRule, Management
from structures.models import DataStructureRequiredField


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def excel_to_dict_list(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active

    data = []
    #  create custom header for check
    headers = []
    header_dictionary = []
    for cell in ws[1]:
        # if there is a cell then it append it to the header  and  the header dictionary
        headers.append(convert_string(cell.value))
        header_dictionary.append({convert_string(cell.value): cell.value})

    for row in ws.iter_rows(min_row=2):  # Assuming the data starts from the third row
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

    return data, header_dictionary


def csv_to_dict_list(csv_file):
    data = []

    reader = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
    raw_headers = next(reader)  # Read the first row as headers
    headers = [convert_string(header) for header in raw_headers]  # Clean the headers using convert_string function
    #  create custom header for check
    header_dictionary = []
    for item in raw_headers:
        if item:
            header_dictionary.append({convert_string(item): item})
    for row in reader:
        row_data = {}
        for header, value in zip(headers, row):
            row_data[header] = value
        data.append(row_data)

    return data, header_dictionary


def convert_file_to_dictionary(file):
    if str(file).endswith(".csv"):
        data, header_dictionary = csv_to_dict_list(file)
    elif str(file).endswith(".xlsx") or str(file).endswith(".xls"):
        data, header_dictionary = excel_to_dict_list(file)
    else:
        raise ValueError("Unsupported file format")

    return data, header_dictionary


def convert_date_format(input_string):
    try:
        # Assuming the input string is in the "YYYY/MM/DD" format
        if isinstance(input_string, datetime):
            return input_string
        # Check if the input string is already in the desired format
        if re.match(r"\d{4}-\d{2}-\d{2}", input_string):
            return input_string

        date_object = datetime.strptime(input_string, "%Y/%m/%d")
        return date_object.strftime("%Y-%m-%d")
    except:
        return None


def convert_string_to_int(value):
    """the check if the value is a string or int and returns the it of the value or none"""
    try:
        # try converting the value to int
        value = str(value).replace(",", "")
        value = float(value)
        return value
    except:
        return None


def is_integer_value(value):
    """
    this is used to check if an integer is a string
    :param value:
    :return:
    """
    try:
        value = int(value)
    except:
        value = value

    if type(value) == int:
        return True
    else:
        return False


def convert_charge_frequency(value):
    """
    this is used to convert charge frequency to custom values in integers from string
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'andenfrekvens':
        # ChargeFrequency  Anden frekvens
        return 0
    elif value == 'anderefrequentie':
        # ChargeFrequency  Andere frequentie
        return 0
    elif value == 'anderefrequenz':
        # ChargeFrequency  Andere Frequenz
        return 0
    elif value == 'autrefrquence':
        # ChargeFrequency  Autre fr�quence
        return 0
    elif value == 'otherfrequency':
        # ChargeFrequency  Other Frequency
        return 0
    elif value == 'gebruikelijkekwartalen':
        # ChargeFrequency  Gebruikelijke kwartalen
        return 10
    elif value == 'quartiershabituels':
        # ChargeFrequency  Quartiers habituels
        return 10
    elif value == 'sdvanligekvarter':
        # ChargeFrequency  S�dvanlige Kvarter
        return 10
    elif value == 'blichequartiere':
        # ChargeFrequency  �bliche Quartiere
        return 10
    elif value == 'usualquarters':
        # ChargeFrequency  Usual Quarters
        return 10
    elif value == 'modernquarters':
        # ChargeFrequency  Modern Quarters
        return 20
    elif value == 'modernekvarter':
        # ChargeFrequency  Moderne Kvarter
        return 20
    elif value == 'moderneviertel':
        # ChargeFrequency  Moderne Viertel
        return 20
    elif value == 'modernewijken':
        # ChargeFrequency  Moderne wijken
        return 20
    elif value == 'quartiersmodernes':
        # ChargeFrequency  Quartiers modernes
        return 20
    elif value == 'altschottisch':
        # ChargeFrequency  Altschottisch
        return 30
    elif value == 'gammelskotsk':
        # ChargeFrequency  Gammel skotsk
        return 30
    elif value == 'oldscottish':
        # ChargeFrequency  Old Scottish
        return 30
    elif value == 'oudschots':
        # ChargeFrequency  Oud Schots
        return 30
    elif value == 'vieuxcossais':
        # ChargeFrequency  Vieux �cossais
        return 30
    elif value == 'cossaismoderne':
        # ChargeFrequency  �cossais moderne
        return 40
    elif value == 'modernscottish':
        # ChargeFrequency  Modern Scottish
        return 40
    elif value == 'moderneschots':
        # ChargeFrequency  Moderne Schots
        return 40
    elif value == 'moderneskotsk':
        # ChargeFrequency  Moderne skotsk
        return 40
    elif value == 'modernesschottisch':
        # ChargeFrequency  Modernes Schottisch
        return 40
    elif value == 'anderekwartalen':
        # ChargeFrequency  Andere kwartalen
        return 50
    elif value == 'andereviertel':
        # ChargeFrequency  Andere Viertel
        return 50
    elif value == 'andrekvarter':
        # ChargeFrequency  Andre Kvarter
        return 50
    elif value == 'autresquartiers':
        # ChargeFrequency  Autres quartiers
        return 50
    elif value == 'otherquarters':
        # ChargeFrequency  Other Quarters
        return 50
    elif value == 'maandelijks':
        # ChargeFrequency  Maandelijks
        return 60
    elif value == 'mnedlige':
        # ChargeFrequency  M�nedlige
        return 60
    elif value == 'mensuel':
        # ChargeFrequency  Mensuel
        return 60
    elif value == 'monatlich':
        # ChargeFrequency  Monatlich
        return 60
    elif value == 'monthly':
        # ChargeFrequency  Monthly
        return 60
    elif value == 'hebdomadaire':
        # ChargeFrequency  Hebdomadaire
        return 70
    elif value == 'ugentlig':
        # ChargeFrequency  Ugentlig
        return 70
    elif value == 'weekly':
        # ChargeFrequency  Weekly
        return 70
    elif value == 'wekelijks':
        # ChargeFrequency  Wekelijks
        return 70
    elif value == 'wchentlich':
        # ChargeFrequency  W�chentlich
        return 70
    elif value == 'annual':
        # ChargeFrequency  Annual
        return 80
    elif value == 'annuel':
        # ChargeFrequency  Annuel
        return 80
    elif value == 'rligt':
        # ChargeFrequency  �rligt
        return 80
    elif value == 'jaarlijks':
        # ChargeFrequency  Jaarlijks
        return 80
    elif value == 'jhrlich':
        # ChargeFrequency  J�hrlich
        return 80
    elif value == 'halbjhrlich':
        # ChargeFrequency  Halbj�hrlich
        return 90
    elif value == 'halfyearly':
        # ChargeFrequency  Half Yearly
        return 90
    elif value == 'halfjaarlijks':
        # ChargeFrequency  Halfjaarlijks
        return 90
    elif value == 'halvrligt':
        # ChargeFrequency  Halv�rligt
        return 90
    elif value == 'semestriel':
        # ChargeFrequency  Semestriel
        return 90
    elif value == 'dagelijks':
        # ChargeFrequency  Dagelijks
        return 100
    elif value == 'daglige':
        # ChargeFrequency  Daglige
        return 100
    elif value == 'daily':
        # ChargeFrequency  Daily
        return 100
    elif value == 'quotidien':
        # ChargeFrequency  Quotidien
        return 100
    elif value == 'tglich':
        # ChargeFrequency  T�glich
        return 100
    elif value == 'allezweiwochen':
        # ChargeFrequency  Alle zwei Wochen
        return 110
    elif value == 'bihebdomadaire':
        # ChargeFrequency  Bihebdomadaire
        return 110
    elif value == 'fortnightly':
        # ChargeFrequency  Fortnightly
        return 110
    elif value == 'hverfjortendedag':
        # ChargeFrequency  Hver fjortende dag
        return 110
    elif value == 'tweewekelijks':
        # ChargeFrequency  Tweewekelijks
        return 110
    elif value == 'fireugentlige':
        # ChargeFrequency  Fire Ugentlige
        return 120
    elif value == 'fourweekly':
        # ChargeFrequency  Four Weekly
        return 120
    elif value == 'quatresemaines':
        # ChargeFrequency  Quatre semaines
        return 120
    elif value == 'vierwekelijks':
        # ChargeFrequency  Vier wekelijks
        return 120
    elif value == 'vierwchentlich':
        # ChargeFrequency  Vierw�chentlich
        return 120
    elif value == 'bimensuel':
        # ChargeFrequency  Bimensuel
        return 130
    elif value == 'bimonthly':
        # ChargeFrequency  Bi-monthly
        return 130
    elif value == 'tomnedligt':
        # ChargeFrequency  To-m�nedligt
        return 130
    elif value == 'tweemaandelijks':
        # ChargeFrequency  Tweemaandelijks
        return 130
    elif value == 'zweimonatlich':
        # ChargeFrequency  Zweimonatlich
        return 130


def convert_index_series(value):
    """
    this is used to convert the index series to int
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'andet':
        # IndexSeries  Andet
        return 0
    elif value == 'autre':
        # IndexSeries  Autre
        return 0
    elif value == 'other':
        # IndexSeries  Other
        return 0
    elif value == 'consumentenprijsindex':
        # IndexSeries  Consumentenprijsindex
        return 10
    elif value == 'consumerpriceindex':
        # IndexSeries  Consumer Price Index
        return 10
    elif value == 'cpi':
        # IndexSeries  CPI
        return 10
    elif value == 'forbrugerprisindekset':
        # IndexSeries  Forbrugerprisindekset
        return 10
    elif value == 'ipc':
        # IndexSeries  IPC
        return 10
    elif value == 'verbraucherpreisindex':
        # IndexSeries  Verbraucherpreisindex
        return 10
    elif value == 'vpi':
        # IndexSeries  VPI
        return 10
    elif value == 'tendance':
        # IndexSeries  Tendance
        return 20
    elif value == 'tendens':
        # IndexSeries  Tendens
        return 20
    elif value == 'trend':
        # IndexSeries  Trend
        return 20
    elif value == 'points':
        # IndexSeries  Points
        return 30
    elif value == 'punkte':
        # IndexSeries  Punkte
        return 30
    elif value == 'punten':
        # IndexSeries  Punten
        return 30
    elif value == 'accordcontractuel':
        # IndexSeries  Accord contractuel
        return 90
    elif value == 'contractagreement':
        # IndexSeries  Contract agreement
        return 90
    elif value == 'contractafspraak':
        # IndexSeries  Contractafspraak
        return 90
    elif value == 'kontraktaftale':
        # IndexSeries  Kontraktaftale
        return 90
    elif value == 'vertragsvereinbarung':
        # IndexSeries  Vertragsvereinbarung
        return 90
    elif value == 'abweichend':
        # IndexSeries  Abweichend
        return 99
    elif value == 'afwijkend':
        # IndexSeries  Afwijkend
        return 99
    elif value == 'divergent':
        # IndexSeries  Divergent
        return 99
    elif value == 'divergerende':
        # IndexSeries  Divergerende
        return 99
    return None


def convert_index_type(value):
    """
    this is used to convert the index type value
    :param value:
    :return:
    """
    old_value = value
    value = convert_string(value)
    if value == 'chronologique':
        # IndexType  Chronologique
        return 'Chronological'
    elif value == 'chronologisch':
        # IndexType  Chronologisch
        return 'Chronological'
    elif value == 'festerrhythmus':
        # IndexType  Fester Rhythmus
        return 'Chronological'
    elif value == 'kronologisk':
        # IndexType  Kronologisk
        return 'Chronological'
    elif value == 'geografisch':
        # IndexType  Geografisch
        return 'Geographically'
    elif value == 'geografisk':
        # IndexType  Geografisk
        return 'Geographically'
    elif value == 'gographiquement':
        # IndexType  G�ographiquement
        return 'Geographically'
    elif value == 'geographisch':
        # IndexType  Geographisch
        return 'Geographically'
    elif value == 'percentage':
        # IndexType  Percentage
        return 'Percentage'
    elif value == 'pourcentage':
        # IndexType  pourcentage
        return 'Percentage'
    elif value == 'procent':
        # IndexType  procent
        return 'Percentage'
    elif value == 'prozent':
        # IndexType  Prozent
        return 'Percentage'
    elif value == 'prozentsatz':
        # IndexType  Prozentsatz
        return 'Percentage'
    elif value == 'taksonomisk':
        # IndexType  Taksonomisk
        return 'Taxonomic'
    elif value == 'taxonomique':
        # IndexType  Taxonomique
        return 'Taxonomic'
    elif value == 'taxonomisch':
        # IndexType  Taxonomisch
        return 'Taxonomic'
    elif value == 'locationtape':
        # IndexType  Location �tape
        return 'Step rent'
    elif value == 'chiffredaffairesloyer':
        # IndexType  Chiffre d'affaires loyer
        return 'Turnover rent'
    elif value == 'trinleje':
        # IndexType  Trinleje
        return 'Step rent'
    elif value == 'omstningsleje':
        # IndexType  Oms�tningsleje
        return 'Turnover rent'
    elif value == 'stufenmiete':
        # IndexType  Stufenmiete
        return 'Step rent'
    elif value == 'umsatzmiete':
        # IndexType  Umsatzmiete
        return 'Turnover rent'
    elif value == 'stapsgewijzehuur':
        # IndexType  Stapsgewijze huur
        return 'Step rent'
    elif value == 'omzethuur':
        # IndexType  Omzethuur
        return 'Turnover rent'
    return old_value


def convert_option_by_code(value):
    """
    this is used to convert the option by code value
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'landheer':
        # OptionByCode   Landheer
        return 10
    elif value == 'landlord':
        # OptionByCode   Landlord
        return 10
    elif value == 'udlejer':
        # OptionByCode   Udlejer
        return 10
    elif value == 'vermieter':
        # OptionByCode   Vermieter
        return 10
    elif value == 'huurder':
        # OptionByCode   Huurder
        return 20
    elif value == 'lejer':
        # OptionByCode   Lejer
        return 20
    elif value == 'mieter':
        # OptionByCode   Mieter
        return 20
    elif value == 'tenant':
        # OptionByCode   Tenant
        return 20
    elif value == 'either':
        # OptionByCode   Either
        return 30
    elif value == 'elke':
        # OptionByCode   Elke
        return 30
    elif value == 'enten':
        # OptionByCode   Enten
        return 30
    elif value == 'entweder':
        # OptionByCode   Entweder
        return 30
    elif value == 'begge':
        # OptionByCode   Begge
        return 40
    elif value == 'beide':
        # OptionByCode   Beide
        return 40
    elif value == 'both':
        # OptionByCode   Both
        return 40
    return None


def convert_type_code(value):
    """
    this is used to convert the option type code
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'break':
        # TypeCode   Break
        return 10
    elif value == 'brechen':
        # TypeCode   Brechen
        return 10
    elif value == 'pause':
        # TypeCode   Pause
        return 10
    elif value == 'pauze':
        # TypeCode   Pauze
        return 10
    elif value == 'aankoop':
        # TypeCode   Aankoop
        return 20
    elif value == 'kaufen':
        # TypeCode   Kaufen
        return 20
    elif value == 'kb':
        # TypeCode   K�b
        return 20
    elif value == 'purchase':
        # TypeCode   Purchase
        return 20
    elif value == 'erneuern':
        # TypeCode   Erneuern
        return 30
    elif value == 'forny':
        # TypeCode   Forny
        return 30
    elif value == 'renew':
        # TypeCode   Renew
        return 30
    elif value == 'vernieuwen':
        # TypeCode   Vernieuwen
        return 30
    return None


def convert_unit_type(value):
    """
    this is used to convert the unit type
    :param value:
    :return:
    """
    old_value = value
    value = convert_string(value)
    if value == 'almindeligtomrde':
        # UnitType  Almindeligt omr�de
        return 'Common Area'
    elif value == 'espacecommun':
        # UnitType  Espace commun
        return 'Common Area'
    elif value == 'gemeenschappelijkeruimte':
        # UnitType  Gemeenschappelijke ruimte
        return 'Common Area'
    elif value == 'gemeinschaftsraum':
        # UnitType  Gemeinschaftsraum
        return 'Common Area'
    elif value == 'couloirs':
        # UnitType  Couloirs
        return 'Corridors'
    elif value == 'gangen':
        # UnitType  Gangen
        return 'Corridors'
    elif value == 'korridore':
        # UnitType  Korridore
        return 'Corridors'
    elif value == 'korridorer':
        # UnitType  Korridorer
        return 'Corridors'
    elif value == 'faade':
        # UnitType  Fa�ade
        return 'Fasade'
    elif value == 'fasade':
        # UnitType  Fasade
        return 'Fasade'
    elif value == 'fassade':
        # UnitType  Fassade
        return 'Fasade'
    elif value == 'gevel':
        # UnitType  gevel
        return 'Fasade'
    elif value == 'benzinestation':
        # UnitType  Benzinestation
        return 'Gas Station'
    elif value == 'stationessence':
        # UnitType  Station-essence
        return 'Gas Station'
    elif value == 'tankstation':
        # UnitType  Tankstation
        return 'Gas Station'
    elif value == 'tankstelle':
        # UnitType  Tankstelle
        return 'Gas Station'
    elif value == 'bonstockage':
        # UnitType  Bon stockage
        return 'Good stora'
    elif value == 'godopbevaring':
        # UnitType  God opbevaring
        return 'Good stora'
    elif value == 'goedeopslag':
        # UnitType  Goede opslag
        return 'Good stora'
    elif value == 'guterspeicher':
        # UnitType  Guter Speicher
        return 'Good stora'
    elif value == 'bureau':
        # UnitType  Bureau
        return 'Office'
    elif value == 'bro':
        # UnitType  B�ro
        return 'Office'
    elif value == 'kantoor':
        # UnitType  Kantoor
        return 'Office'
    elif value == 'kontor':
        # UnitType  Kontor
        return 'Office'
    elif value == 'ander':
        # UnitType  Ander
        return 'Other'
    elif value == 'andere':
        # UnitType  Andere
        return 'Other'
    elif value == 'andet':
        # UnitType  Andet
        return 'Other'
    elif value == 'autre':
        # UnitType  Autre
        return 'Other'
    elif value == 'auen':
        # UnitType  Au�en
        return 'Outside'
    elif value == 'buiten':
        # UnitType  Buiten
        return 'Outside'
    elif value == 'dehors':
        # UnitType  Dehors
        return 'Outside'
    elif value == 'udenfor':
        # UnitType  Uden for
        return 'Outside'
    elif value == 'parken':
        # UnitType  Parken
        return 'Parking'
    elif value == 'parkeren':
        # UnitType  Parkeren
        return 'Parking'
    elif value == 'parkering':
        # UnitType  Parkering
        return 'Parking'
    elif value == 'parking':
        # UnitType  Parking
        return 'Parking'
    elif value == 'dtail':
        # UnitType  D�tail
        return 'Retail'
    elif value == 'detailhandel':
        # UnitType  Detailhandel
        return 'Retail'
    elif value == 'einzelhandel':
        # UnitType  Einzelhandel
        return 'Retail'
    elif value == 'dach':
        # UnitType  Dach
        return 'Roof'
    elif value == 'dak':
        # UnitType  Dak
        return 'Roof'
    elif value == 'tag':
        # UnitType  Tag
        return 'Roof'
    elif value == 'toit':
        # UnitType  Toit
        return 'Roof'
    elif value == 'sociaal':
        # UnitType  Sociaal
        return 'Social'
    elif value == 'social':
        # UnitType  Social
        return 'Social'
    elif value == 'sozial':
        # UnitType  Sozial
        return 'Social'
    elif value == 'lagerung':
        # UnitType  Lagerung
        return 'Storage'
    elif value == 'opbevaring':
        # UnitType  Opbevaring
        return 'Storage'
    elif value == 'opslag':
        # UnitType  Opslag
        return 'Storage'
    elif value == 'stockage':
        # UnitType  Stockage
        return 'Storage'
    elif value == 'technique':
        # UnitType  Technique
        return 'Technical'
    elif value == 'teknisk':
        # UnitType  Teknisk
        return 'Technical'
    elif value == 'technisch':
        # UnitType  Technisch
        return 'Technical '
    elif value == 'toiletten':
        # UnitType  Toiletten
        return 'Toilets'
    elif value == 'toiletter':
        # UnitType  Toiletter
        return 'Toilets'
    elif value == 'toilettes':
        # UnitType  Toilettes
        return 'Toilets'
    elif value == 'couloirsverticaux':
        # UnitType  Couloirs verticaux
        return 'Vertical Corridors'
    elif value == 'lodrettekorridorer':
        # UnitType  Lodrette korridorer
        return 'Vertical Corridors'
    elif value == 'verticalegangen':
        # UnitType  Verticale gangen
        return 'Vertical Corridors'
    elif value == 'vertikalekorridore':
        # UnitType  Vertikale Korridore
        return 'Vertical Corridors'
    elif value == 'woonhuis':
        # UnitType  Woonhuis
        return 'Residential'
    elif value == 'wohnen':
        # UnitType  Wohnen
        return 'Residential'
    elif value == 'bolig':
        # UnitType  Bolig
        return 'Residential'
    elif value == 'rsidentiel':
        # UnitType  R�sidentiel
        return 'Residential'
    elif value == 'appartement':
        # UnitType  Appartement
        return 'Residential'
    elif value == 'eengezinswoning':
        # UnitType  Eengezinswoning
        return 'Residential'
    elif value == 'egw':
        # UnitType  EGW
        return 'Residential'
    elif value == 'mgw':
        # UnitType  MGW
        return 'Residential'
    elif value == 'appartement':
        # UnitType  Appartement
        return 'Residential'
    elif value == 'maisonunifamiliale':
        # UnitType  Maison unifamiliale
        return 'Residential'
    elif value == 'lejlighed':
        # UnitType  Lejlighed
        return 'Residential'
    elif value == 'enfamiliehus':
        # UnitType  Enfamiliehus
        return 'Residential'
    elif value == 'wohnung':
        # UnitType  Wohnung
        return 'Residential'
    elif value == 'einfamilienhaus':
        # UnitType  Einfamilienhaus
        return 'Residential'
    elif value == 'apartment':
        # UnitType  Apartment
        return 'Residential'
    elif value == 'singlefamilyhouse':
        # UnitType  Single-family house
        return 'Residential'
    elif value == 'studio':
        # UnitType  Studio
        return 'Residential'
    elif value == 'bungalow':
        # UnitType  Bungalow
        return 'Residential'
    elif value == 'maisonnette':
        # UnitType  Maisonnette
        return 'Residential'
    return old_value


def convert_vat_code(value):
    """
    this is used to convert vat code
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'nee':
        # VATCode  Nee
        return 0
    elif value == 'nein':
        # VATCode  Nein
        return 0
    elif value == 'njet':
        # VATCode  Njet
        return 0
    elif value == 'no':
        # VATCode  No
        return 0
    elif value == 'da':
        # VATCode  Da
        return 1
    elif value == 'ja':
        # VATCode  Ja
        return 1
    elif value == 'qui':
        # VATCode  Qui
        return 1
    elif value == 'yes':
        # VATCode  Yes
        return 1
    return None


def convert_security_type_code(value):
    """
    this is used to convert security type code
    :param value:
    :return:
    """
    value = convert_string(value)
    if value == 'bankguarantee':
        # SecurityTypeCode  Bank Guarantee
        return 10
    elif value == 'companyguarantee':
        # SecurityTypeCode  Company Guarantee
        return 20
    elif value == 'deposit':
        # SecurityTypeCode  Deposit
        return 30
    elif value == 'none':
        # SecurityTypeCode  None
        return 40
    elif value == 'bankgarantie':
        # SecurityTypeCode  Bankgarantie
        return 10
    elif value == 'bedrijfsgarantie':
        # SecurityTypeCode  Bedrijfsgarantie
        return 20
    elif value == 'borg':
        # SecurityTypeCode  Borg
        return 30
    elif value == 'geen':
        # SecurityTypeCode  Geen
        return 40
    elif value == 'bankgarantie':
        # SecurityTypeCode  Bankgarantie
        return 10
    elif value == 'firmengarantie':
        # SecurityTypeCode  Firmengarantie
        return 20
    elif value == 'kaution':
        # SecurityTypeCode  Kaution
        return 30
    elif value == 'keiner':
        # SecurityTypeCode  Keiner
        return 40
    elif value == 'garantiebancaire':
        # SecurityTypeCode  Garantie bancaire
        return 10
    elif value == 'garantieentreprise':
        # SecurityTypeCode  Garantie Entreprise
        return 20
    elif value == 'dpt':
        # SecurityTypeCode  D�p�t
        return 30
    elif value == 'aucun':
        # SecurityTypeCode  Aucun
        return 40
    elif value == 'bankgaranti':
        # SecurityTypeCode  Bank garanti
        return 10
    elif value == 'virksomhedsgaranti':
        # SecurityTypeCode  Virksomhedsgaranti
        return 20
    elif value == 'depositum':
        # SecurityTypeCode  Depositum
        return 30
    elif value == 'ingen':
        # SecurityTypeCode  Ingen
        return 40
    return None


def convert_string_int_to_bool(value):
    """the check if the value is a string or int and returns the bool of it"""
    try:
        # try converting the value to int
        if type(value) == bool:
            return value
        elif value == 0:
            return False
        elif value == 1:
            return True
        elif value.lower == "da":
            return True
        elif value.lower == "ja":
            return True
        elif value.lower == "nee":
            return False
        elif value.lower == "nein":
            return False
        elif value.lower == "njet":
            return False
        elif value.lower == "no":
            return False
        elif value.lower == "qui":
            return True
        elif value.lower == "yes":
            return True

        elif value.lower() == "false":
            return False
        elif value.lower() == "true":
            return True
        else:
            return False
    except:
        return False


def convert_string(input_string):
    # Convert capital letters to lowercase
    if not input_string or input_string == "":
        return None
    lowercase_string = input_string.lower()

    # Remove non-alphabetic characters
    cleaned_string = re.sub('[^a-z0-9]', '', lowercase_string)

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
        (Q(user__email__icontains=x) |
         Q(status__icontains=x) |
         Q(name__icontains=x) |
         Q(name=[x]) for x in query_list)
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
    errors = []
    counter = 0
    for management in managements:
        counter += 1
        try:
            for field in required_fields._meta.fields:
                if field.name == 'id' or field.name == "timestamp" or field.name == "user" or field.name == "contract":
                    continue
                if getattr(required_fields, field.name):
                    if getattr(management, field.name) is None or getattr(management, field.name) == "":
                        errors.append(
                            f"row {counter}: {field.name} is a required field. Please update below, then save and validate")
        except:
            pass
    return errors


def check_header_in_structure(headers, structure):
    # Assuming you have a Django instance called 'instance' of some model
    fields = [field.name for field in structure._meta.get_fields()]
    data_dict = model_to_dict(structure, fields=fields)
    new_dict = {convert_string(key): value for key, value in data_dict.items()}

    error_list = []
    try:
        for header in headers:
            for key, value in header.items():
                # Perform operations with key and value
                if key and key != "":
                    found_key = None
                    for dict_key, dict_value in new_dict.items():
                        if convert_string(dict_value) == convert_string(value):
                            found_key = dict_key
                            break
                    if not found_key:
                        error_list.append(
                            f"Invalid Header: '{value}'. Please change the mapping or provide a valid header"
                            f" In your upload file. The current upload is cancelled."
                        )
    except:
        pass
    return error_list


def check_validation_on_management(contract: Contract):
    """
    this is used to validate the management model with the default value that is supposed to be there
    :param contract:
    :return:
    """

    rule = ManagementRule.objects.filter(user=contract.user).first()
    if not rule:
        rule = ManagementRule.objects.create(user=contract.user)
    managements = contract.management_set.all()
    # loop through the management and check for the required stuff in each row
    counter = 0
    errors = []

    for management in managements:
        counter += 1
        # check is vacant on rule
        if rule.is_vacant_then_vacancy_reason:
            if management.vacant:
                if not management.vacancy_note:
                    errors.append(
                        f"row {counter}: Vacancy Reason is required if unit is vacant. Please update below, then save and validate. ")
        #  check for gross area and net area
        if rule.gross_area_then_net_area:
            if not management.gross_area and not management.net_area:
                errors.append(
                    f"row {counter}: either Net or Gross area is required. Please update below, then save and validate.")
            if management.gross_area:
                if management.gross_area < 1 and not management.net_area:
                    errors.append(
                        f"Gross Area cannot be less than zero if Net Area is not provided in row {counter}.")
            if management.net_area:
                if management.net_area < 1 and not management.gross_area:
                    errors.append(
                        f"Net Area cannot be less than zero if Gross Area is not provided in row {counter}.")
        # check for Option
        if rule.option_then_date_provided:
            # option_type_landlord_tenant_mutual and option_type_break_purchase_renew  is provided then there must be
            # date
            if management.option_by_code or management.type_code:
                if not management.to_date or not management.from_date:
                    errors.append(
                        f"row {counter}: either the Option From Date or The Option To Date is required. Please update below, then save and validate.")
        # check for index
        if rule.index_then_date:
            if management.index_type or management.value:
                if not management.index_date:
                    errors.append(f"row {counter}: Index date needs to be provided if a value exists.")
    return errors


def export_management_csv(contract):
    """
    this returns the full info of all the product in csv format
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{contract.name}.csv"'
    # Specify the encoding as utf-8
    response.write('\ufeff'.encode('utf-8'))  # Add the BOM (Byte Order Mark) for UTF-8 encoding

    writer = csv.writer(response)

    # Get a list of all fields of the model
    fields = [f.name for f in Management._meta.fields if f.name not in ['id', 'user', 'contract', 'timestamp']]

    # Write the header row
    writer.writerow(fields)

    # Write the data rows
    for obj in Management.objects.filter(contract=contract):
        row = [getattr(obj, f) for f in fields]
        writer.writerow(row)
    return response


def convert_management_value_with_field_name(field_name, management_value):
    """this is used to convert the field name with the management value"""
    if field_name == "charge_frequency":
        # converting the value to an integer if written in words
        if not is_integer_value(management_value):
            management_value = convert_charge_frequency(value=management_value)

    elif field_name == "index_series":
        if not is_integer_value(management_value):
            management_value = convert_index_series(management_value)
    elif field_name == "index_type":
        management_value = convert_index_type(management_value)
    elif field_name == "option_by_code":
        if not is_integer_value(management_value):
            management_value = convert_option_by_code(management_value)
    elif field_name == "option_by_code":
        if not is_integer_value(management_value):
            management_value = convert_option_by_code(management_value)
    elif field_name == "type_code":
        if not is_integer_value(management_value):
            management_value = convert_type_code(management_value)
    elif field_name == "unit_type":
        # the field is a string, so it does not need converting
        management_value = convert_unit_type(management_value)
    elif field_name == "vat_code":
        if not is_integer_value(management_value):
            management_value = convert_vat_code(management_value)
    elif field_name == "security_type_code":
        if not is_integer_value(management_value):
            management_value = convert_security_type_code(management_value)
    return management_value
