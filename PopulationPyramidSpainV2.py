# -*- coding: utf-8 -*-
'''
@author: Juan José Carrasco Fernández
'''

import plotly.express as px
from dash import Dash, dcc, html
import pandas as pd
pd.options.mode.copy_on_write = True

# load data
df = pd.read_json('Poblacion.json')

# df.head()
# df.columns
# df.info()

# Extract data and convert into dataframe.
dataframes = []

for _, row in df.iterrows():
    data = pd.DataFrame.from_records(row['Data'],
                                     exclude=['T3_TipoDato', 'T3_Periodo', 'Anyo'])

    data['Age_text'] = row['MetaData'][1]['Nombre']  # years old
    data['Gender'] = row['MetaData'][2]['Nombre']  # gender
    dataframes.append(data)

df2 = pd.concat(dataframes, ignore_index=True)

df2['Fecha'] = pd.to_datetime(df2['Fecha'], utc=True)
df2 = df2[df2['Fecha'].dt.month == 12]
df2['Fecha'] = df2['Fecha'].dt.year

df2 = df2.rename(columns={'Fecha': 'Date', 'Valor': 'Population'})

df2['Gender'] = df2['Gender'].map({'Total': 'Combined',
                                   'Hombres': 'Male',
                                   'Mujeres': 'Female'}).fillna(df2['Gender'])

# df2.info()
# df2.head()

df2.drop(df2[df2['Age_text'].str.contains('y más años')].index, inplace=True)

df_filt = df2[(df2['Age_text'] != 'Todas las edades')
              & (df2['Gender'] != 'Combined')]

df_filt['Pop'] = df_filt['Population']

df_filt.loc[df_filt['Gender'] == 'Female', 'Pop'] *= -1

df_filt['Age'] = pd.to_numeric(df_filt['Age_text'].str.extract(r'(\d+)', expand=False),
                               downcast='integer',
                               errors='coerce')

df_filt = df_filt.sort_values(by=['Date', 'Age'], ascending=True)


Pop_1970 = int(df2.loc[(df2['Date'] == 1970) &
                       (df2['Age_text'] == 'Todas las edades') &
                       (df2['Gender'] == 'Combined'), 'Population'].iloc[0])
     

#%%

# Data visualization with dash.
app = Dash()

colors = {
    'background': 'rgb(0,0,0)',
    'text': 'rgb(127, 219, 255)',
}

fig = px.bar(df_filt,
             x='Pop',
             y='Age',
             color='Gender',
             animation_frame="Date",
             orientation='h',
             barmode='relative',
             hover_data={'Gender': True,
                         'Date': True,
                         'Population': ':,',
                         'Pop': False,
                         'Age': True
                         },
             range_x=[-max(df_filt['Population']), max(df_filt['Population'])],
             range_y=[0, max(df_filt['Age'])],
             width=1000,
             height=900,
             title=f'Total population in 1970: {Pop_1970:,}',
             )

fig.update_traces(marker_line_width=0)

fig.update_xaxes(title='Population',
                 title_font_size=18,
                 tickmode='array',
                 tickvals=[-400000, -300000, -200000, -100000,
                           0, 100000, 200000, 300000, 400000],
                 ticktext=['400k', '300k', '200k', '100k',
                           '0', '100k', '200k', '300k', '400k'])

fig.update_layout(title_font_size=22,
                  font_size=16,
                  plot_bgcolor=colors['background'],
                  paper_bgcolor=colors['background'],
                  font_color=colors['text']
                  )


for k in range(len(fig.frames)):

    year = int(fig.frames[k].name)
    Pop_year = int(df2.loc[(df2['Date'] == year) &
                           (df2['Age_text'] == 'Todas las edades') &
                           (df2['Gender'] == 'Combined'), 'Population'].iloc[0])

    fig.frames[k]['layout'].update(title_text=f'Total population in {
                                              year}: {Pop_year:,}')


app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[html.H1(children='Population Pyramid of Spain 1970-2023',
                      style={'margin-left': '50px',
                             'textAlign': 'left',
                             'color': colors['text']}),
              dcc.Loading(id='loading', type='cube',
                          children=dcc.Graph(figure=fig))
              ]
)


if __name__ == '__main__':
    app.run(debug=True, port=8054)

# http://127.0.0.1:8054/
