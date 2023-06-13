# import numpy as np
import json
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

df = pd.read_csv(r'app\static\data\netflix_titles.csv')
data = {}


# Create your views here.
def home(request):
    data['dados'] = df\
        .drop(['show_id', 'date_added'], axis=1)\
        .dropna()\
        .head(20)\
        .to_html(index=False, classes=['table', 'table-striped', 'mt-5'])
    data['countryFilter'] = df['country'].sort_values().unique()
    return render(request, 'index.html', data)


# Requisição para filtro de país
from django.http import JsonResponse, HttpResponseBadRequest


def countryFilter(request):
    if request.body:
        field = json.loads(request.body.decode('utf-8'))
        search = field['country']
        df2 = df.dropna()
        data['dados'] = df2[df2['country'].str.contains(search)]\
            .to_html(index=False, classes=['table', 'table-striped', 'mt-5'])
        return JsonResponse({'data': data['dados']})
    else:
        return HttpResponseBadRequest('Dados inválidos')
