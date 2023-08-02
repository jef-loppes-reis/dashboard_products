from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from data_base import main


app = Dash(__name__)

df = main()
df_img1 = df.query('(pedido_compra or estoque > 0) and ~codpro.duplicated()').reset_index(drop=True)
df_img1_groups = pd.DataFrame(df_img1.value_counts('grupo')).reset_index().rename({'count':'qtd_groups'}, axis=1).head(10)

fig = px.bar(df_img1_groups, title='QTD de SKUs distintos com pedido de compra ou em estoque no grupo.', x="grupo", y="qtd_groups")

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    generate_table(df)
])


if __name__ == '__main__':
    app.run_server(debug=True)