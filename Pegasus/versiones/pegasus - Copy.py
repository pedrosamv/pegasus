#Aca importe todos los chiches que voy a usar.
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output




df_mensual = pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=0)
df_trimestral= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=1)
df_anual= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=2)
df_serie_pbi= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=3)
df_tasa= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=4)
df_tcn= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=5)

df_tcn["fecha_tcn"] = pd.to_datetime(df_tcn["fecha_tcn"], format="%Y-%m-%d")
df_serie_pbi["serie_tasa_pbi"] = pd.to_numeric(df_serie_pbi["serie_tasa_pbi"])
df_tasa["fecha_tasa"] = pd.to_datetime(df_tasa["fecha"], format="%d-%m-%Y")

#df_anual["year"] = pd.to_datetime(df_anual["year"], format="%Y")
df_mensual["fecha"] = pd.to_datetime(df_mensual["year"].astype(str) + "-" + df_mensual["mes"].astype(str), format="%Y-%m")


#print(df_mensual.columns.tolist()) esto es para ver si leyo bien la base.

app = Dash(__name__)

# ========= Layouts de cada sección =========

# Pobreza
pobreza_layout = html.Div([
    html.H2("Evolución de la Pobreza", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_pobreza",
                    figure=px.scatter(df_anual, x="year", y="pobreza", size_max=60)
                            .update_traces(
                                mode='lines+markers',
                                marker=dict(symbol='circle', size=6, color='#75AADB'),
                                line=dict(color='#75AADB', width=2),
                                hovertemplate="Año: %{x}<br>Pobreza: %{y:.1f}%<extra></extra>"
                            )
                            .update_layout(
                                title="",
                                height=500,
                                xaxis=dict(
                                    title="Año",
                                    tickmode="array",
                                    tickvals=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
                                    ticktext=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,"2025*"],
                                    range=[2015, 2025.5],
                                    fixedrange=True,
                                    showgrid=True,
                                    gridcolor='#E0E0E0',
                                    gridwidth=1,
                                    showline=True,
                                    linecolor='#E0E0E0',
                                    linewidth=1
                                ),
                                yaxis=dict(
                                    title="Población bajo la línea de pobreza (%)",
                                    range=[-5, 100],
                                    dtick=10,
                                    zeroline=True,
                                    fixedrange=False,
                                    showgrid=True,
                                    gridcolor='#E0E0E0',
                                    gridwidth=1,
                                    showline=True,
                                    linecolor='#E0E0E0',
                                    linewidth=1
                                ),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                shapes=[
                                    dict(type="line", x0=2016, x1=2016, y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0=2020, x1=2020, y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0=2024, x1=2024, y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                ]
                            )
    ),
    dcc.Link("⬅ Volver al inicio", href="/", style={"display": "block", "marginTop": "20px"})
])

# PBI
pbi_layout = html.Div([
    html.H2("Crecimiento del PBI", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_pbi",
        figure=px.line(df_serie_pbi, x="year", y="serie_tasa_pbi")
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=6, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
    ),
    dcc.Link("⬅ Volver al inicio", href="/")
])

# Inflación
inflacion_layout = html.Div([
    html.H2("Inflación Mensual", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_inflacion",
        figure=px.scatter(df_mensual, x="fecha", y="inflacion_mensual", size_max=60)
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=6, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
    ),
    dcc.Link("⬅ Volver al inicio", href="/")
])

# Tipo de Cambio
tcn_layout = html.Div([
    html.H2("Tipo de Cambio Nominal", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_tcn",
        figure=px.line(df_tcn, x="fecha_tcn", y="tcn")
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=2, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
    ),
    dcc.Link("⬅ Volver al inicio", href="/")
])

# Tasa Leliq
tasa_layout = html.Div([
    html.H2("Tasa de Política Monetaria", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_tasa",
        figure=px.scatter(df_tasa, x="fecha_tasa", y="tasa_leliqs", size_max=60)
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=3, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
    ),
    dcc.Link("⬅ Volver al inicio", href="/")
])

# ========= Menú principal =========
card_style = {
    "border": "1px solid #ccc",
    "borderRadius": "10px",
    "padding": "20px",
    "margin": "10px",
    "width": "200px",
    "textAlign": "center",
    "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
    "cursor": "pointer",
    "display": "inline-block",
    "verticalAlign": "top",
}

home_layout = html.Div([
    html.H1("Argentina: ¿qué corno te pasa?", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        dcc.Link(
            html.Div([
                html.Div("📉", style={"fontSize": "40px"}),
                html.H4("Pobreza"),
                html.P("Evolución de la pobreza en Argentina."),
            ], style=card_style), href="/pobreza"
        ),

        dcc.Link(
            html.Div([
                html.Div("📊", style={"fontSize": "40px"}),
                html.H4("PBI"),
                html.P("Serie de tasa de crecimiento del PBI."),
            ], style=card_style), href="/pbi"
        ),

        dcc.Link(
            html.Div([
                html.Div("💸", style={"fontSize": "40px"}),
                html.H4("Inflación"),
                html.P("Evolución de la inflación mensual."),
            ], style=card_style), href="/inflacion"
        ),

        dcc.Link(
            html.Div([
                html.Div("💱", style={"fontSize": "40px"}),
                html.H4("Tipo de cambio"),
                html.P("Evolución del tipo de cambio nominal."),
            ], style=card_style), href="/tcn"
        ),

        dcc.Link(
            html.Div([
                html.Div("🏦", style={"fontSize": "40px"}),
                html.H4("Tasa de interés"),
                html.P("Evolución de la tasa de política monetaria."),
            ], style=card_style), href="/tasa"
        )
    ], style={"textAlign": "center"})
])

# ========= Layout con router =========
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

# ========= Callbacks para navegación =========
@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/pobreza":
        return pobreza_layout
    elif pathname == "/pbi":
        return pbi_layout
    elif pathname == "/inflacion":
        return inflacion_layout
    elif pathname == "/tcn":
        return tcn_layout
    elif pathname == "/tasa":
        return tasa_layout
    else:
        return home_layout


if __name__ == "__main__":
    app.run(debug=True)