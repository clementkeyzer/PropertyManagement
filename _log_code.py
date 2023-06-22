from management.utils import convert_string


def convert_charge_frequency(value):
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
	elif value == 'andere':
	# IndexSeries  Andere 
	    return 0
	elif value == 'andet':
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
	elif value == 'nee':
	# IsCompany   Nee 
	    return 0
	elif value == 'nein':
	# IsCompany   Nein 
	    return 0
	elif value == 'njet':
	# IsCompany   Njet 
	    return 0
	elif value == 'no':
	# IsCompany   No 
	    return 0
	elif value == 'da':
	# IsCompany   Da 
	    return 1
	elif value == 'ja':
	# IsCompany   Ja 
	    return 1
	elif value == 'qui':
	# IsCompany   Qui 
	    return 1
	elif value == 'yes':
	# IsCompany   Yes 
	    return 1
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
	elif value == 'nee':
	# Vacant  Nee 
	    return 0
	elif value == 'nein':
	# Vacant  Nein 
	    return 0
	elif value == 'njet':
	# Vacant  Njet 
	    return 0
	elif value == 'no':
	# Vacant  No 
	    return 0
	elif value == 'da':
	# Vacant  Da 
	    return 1
	elif value == 'ja':
	# Vacant  Ja 
	    return 1
	elif value == 'qui':
	# Vacant  Qui 
	    return 1
	elif value == 'yes':
	# Vacant  Yes 
	    return 1
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