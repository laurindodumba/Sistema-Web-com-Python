

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel('faturamento.xlsx', nrows=4000, sheet_name='Planilha1', engine='openpyxl')

    
# Criando gráficos
fig = px.bar(df, x="Produto", y="Total", color="Filial", barmode="group")

#Criar uma lista de forma dinâmica para que o usuário possa interagir  nas escolhas 

opcoes = list(df['Filial'].unique()) 
opcoes.append("Todas as filiais")




app.layout = html.Div(children=[
    html.H1(children='DASH CONTROLE DE FATURAMENTO '),

    html.Div(children='''
        Dash: Aplicação web para controle de faturamento por filial
    '''),

dcc.Dropdown(opcoes, 'Todas as filias',  id='lista_filiais'),
html.Div(id='txt_soma_faturamento_filial'),


    dcc.Graph(
        id='grafico_faturamento_filial', 
        figure=fig
    )
])

#Criar os callbacks

@app.callback(
    Output('grafico_faturamento_filial', 'figure'),
    Input('lista_filiais', 'value')
)
def update_output(value):
    if value == 'Todas as filiais':
        fig = px.bar(df, x="Produto", y="Total", color="Filial", barmode="group")
    else:
        tabela_filtrada = df.loc[df['Filial'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Total", color="Filial", barmode="group")

        return fig


# Atualiza a soma do faturamento

@app.callback(
    Output('txt_soma_faturamento_filial', 'children'),
    Input('lista_filiais', 'value')
)
def update_output(value):
    if value == 'Todas as Filiais':
        soma_fat = round(df['Total'].sum(),2)
    else:
        tabela_filtrada = df.loc[df['Filial'] == value, :]
        soma_fat= round(tabela_filtrada['Total'].sum(),2)
    return f'Faturamento Total é de: R$' + str(soma_fat)

if __name__ == '__main__':
    app.run(debug=True)
