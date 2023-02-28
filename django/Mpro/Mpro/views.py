from django.shortcuts import render
from . import visual

def index(request):
    return render(request, "index.html")

def sub(request):
    return render(request, "index.html")

def main_A(request):
    return render(request, "main_A.html")

def main_B(request):
    return render(request, "main_A.html")

def main_C(request):
    return render(request, "main_A.html")

def index(request):
    contexts = dict()
    contexts['location_foot_traffic'] = visual.location_foot_traffic()
    contexts['location_region_traffic'] = visual.location_region_traffic()
    contexts['location_work_traffic'] = visual.location_work_traffic()
    contexts['location_store_density'] = visual.location_store_density()
    contexts['seoul_restaurant'] = visual.seoul_restaurant()

    return render(request, 'index.html', contexts)

def main_A(request):
    contexts = dict()
    contexts['economic_real'] = visual.economic_real()
    contexts['economic_nomial'] = visual.economic_nomial()
    contexts['business_loan_interest'] = visual.business_loan_interest()
    contexts['consumer_price_index'] = visual.consumer_price_index()
    
    return render(request, 'main_A.html', contexts)

def main_B(request):
    contexts = dict()
    contexts['location_foot_traffic'] = visual.location_foot_traffic()
    contexts['location_region_traffic'] = visual.location_region_traffic()
    contexts['location_work_traffic'] = visual.location_work_traffic()
    contexts['location_store_density'] = visual.location_store_density()
    contexts['seoul_restaurant'] = visual.seoul_restaurant()
    
    return render(request, 'main_B.html', contexts)

def main_C(request):
    contexts = dict()
    contexts['location_foot_traffic'] = visual.location_foot_traffic()
    contexts['location_region_traffic'] = visual.location_region_traffic()
    contexts['location_work_traffic'] = visual.location_work_traffic()
    contexts['location_store_density'] = visual.location_store_density()
    contexts['seoul_restaurant'] = visual.seoul_restaurant()
    
    return render(request, 'main_C.html', contexts)