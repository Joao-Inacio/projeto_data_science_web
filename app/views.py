# import numpy as np
import pandas as pd
from django.shortcuts import render


# Create your views here.
def home(request):
    df = pd.read_csv(r'app\static\data\netflix_titles.csv')
    data = {}

    df['country'] = df['country'].apply(
        lambda x: 'Brasil' if x == 'Brazil' else x
        )

    data['dados'] = df.to_html(
        index=False,
        classes=['table', 'table-striped', 'mt-5']
        )
    return render(request, 'index.html', data)
