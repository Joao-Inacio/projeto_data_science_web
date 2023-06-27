# import numpy as np
import json
import re

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

df = pd.read_csv(r'app\static\data\netflix_titles.csv')
data = {}


# Create your views here.
def home(request, page=None):
    counter = 0
    list = []
    rows = len(df.index)

    while (counter < rows):
        list.append("<a href='/detalhes/"+str(counter)+"'>Detalhes</a>")
        counter += 1
    df['links'] = list

    # Paginação
    registers = 10
    if ((page is None) | (page == 1)):
        page_number = 1
        start = 0
        end = registers
    else:
        page_number = int(page)
        start = registers * page_number - registers
        end = start + registers
    paginator = Paginator(df.dropna(), registers)
    data['paginator'] = paginator.get_page(page_number)

    trace = go.Bar(
        x=df.sort_values(by='release_year')['release_year'].unique(),
        y=df.groupby('release_year')['title'].count()
    )
    datas = [trace]
    data['grafico'] = py.plot(datas, output_type='div')

    data['dados'] = df[['title', 'country', 'links']]\
        .dropna()\
        .iloc[start:end]\
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

        data['grafico'] = {
            'x': df2[
                (df2['country'].str.contains(search))
                &
                (df2['title'].str.contains(
                    title, flags=re.IGNORECASE
                    ))].sort_values(
                        by='release_year'
                        )['release_year'].unique().tolist(),
            'y': df2[
                (df2['country'].str.contains(search))
                &
                (df2['title'].str.contains(
                    title, flags=re.IGNORECASE))].groupby(
                        'release_year'
                        )['title'].count().to_list()
        }
        data['dados'] = df2[
            (df2['country'].str.contains(search))
            & (
                df2['title'].str.contains(
                    title, flags=re.IGNORECASE
                )
            )
        ]\
            .to_html(
                render_links=True, escape=False,
                index=False, classes=['table', 'table-striped', 'mt-5'])
        return JsonResponse({'data': data['dados'], 'graph': data['grafico']})
    else:
        return HttpResponseBadRequest('Dados inválidos')


def detalhes(request, pk):
    data['pk'] = pk
    data['dados'] = df.iloc[int(pk)].values
    return render(request, 'detalhes.html', data)
