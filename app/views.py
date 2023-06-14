# import numpy as np
import json
import re

import pandas as pd
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

df = pd.read_csv(r'app\static\data\netflix_titles.csv')
data = {}


# Create your views here.
def home(request):
    counter = 0
    list = []
    rows = len(df.index)

    while (counter < rows):
        list.append("<a href='/detalhes/"+str(counter)+"'>Detalhes</a>")
        counter += 1
    df['links'] = list

    data['dados'] = df[['title', 'country', 'links']]\
        .dropna()\
        .head(20)\
        .to_html(
            render_links=True, escape=False,
            classes=[
                'table', 'table-striped',
                'table-hover', 'mt-5'
            ]
        )
    data['countryFilter'] = df['country'].sort_values().unique()
    return render(request, 'index.html', data)


# Requisição para filtro de país
def countryFilter(request):
    if request.body:
        field = json.loads(request.body.decode('utf-8'))
        search = field['country']
        title = field['title']
        df2 = df.dropna()
        data['dados'] = df2[
            (df2['country'].str.contains(search))
            & (
                df2['title'].str.contains(
                    title, flags=re.IGNORECASE
                )
            )
        ]\
            .to_html(index=False, classes=['table', 'table-striped', 'mt-5'])
        return JsonResponse({'data': data['dados']})
    else:
        return HttpResponseBadRequest('Dados inválidos')


def detalhes(request, pk):
    data['pk'] = pk
    data['dados'] = df.iloc[int(pk)].values
    return render(request, 'detalhes.html', data)

