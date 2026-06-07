#Aca importe todos los chiches que voy a usar.
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px


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
app.layout = html.Div([

    html.H1(
        "Argentina: que corno te pasa?",
        style={
            "textAlign": "center",
            "fontSize": "32px",
            "marginBottom": "10px",
            "fontWeight": "600",
            "fontFamily": "Montserrat"
        }
    ),

    # Bloque 1: Pobreza
    html.Div([

        html.Div([  # fila: gráfico + descripción
            html.Div([
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
                )
            ], style={"flex": 6, "padding": "10px"}),

            html.Div([  # descripción a la derecha
                html.H3("Descripción"),
                html.P("Este gráfico muestra la relación entre pobreza y año.")
            ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"})
        ], style={"display": "flex", "flexDirection": "row"}),

        # Comentarios debajo del bloque de pobreza
        html.Div("Fecha: 31-08-2025", style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
        html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                 style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),

# Bloque 2: PBI
html.Div([

    html.Div([  # descripción a la izquierda
        html.H3("Descripción"),
        html.P("Este gráfico muestra la serie de tasa de crecimiento del PBI.")
    ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"}),

    html.Div([  # gráfico + comentarios
        dcc.Graph(
            id="grafico_pbi",
            figure=px.line(df_serie_pbi, x="year", y="serie_tasa_pbi")
                .update_traces(
                    mode='lines+markers',  # gráfico principal sigue con líneas y puntos
                    marker=dict(symbol='circle', size=6, color='#75AADB'),
                    line=dict(color='#75AADB', width=2),
                    hovertemplate="Año: %{x}<br>Valor: %{y:.2f}<extra></extra>"
                )
                .update_layout(
                    title="",
                    height=500,
                    xaxis=dict(
                        title="Año",
                        tickmode="linear",
                        range=[2003, 2025],
                        showgrid=True,
                        gridcolor='#E0E0E0',
                        gridwidth=1,
                        showline=True,
                        linecolor='#E0E0E0',
                        linewidth=1,
                        rangeslider=dict(
                        visible=True,
                        thickness=0.05,
                        bgcolor='#E0E0E0',
                        borderwidth=0
                    )
                    ),
                    yaxis=dict(
                        title="Tasa de crecimiento anual del PBI (%)",
                        range=[-16, 15],
                        dtick=3,
                        showgrid=True,
                        gridcolor='#E0E0E0',
                        gridwidth=1
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    shapes=[  # líneas verticales amarillas-anaranjadas
                        dict(type="line", x0=2004, x1=2004, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=2008, x1=2008, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=2012, x1=2012, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=2016, x1=2016, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=2020, x1=2020, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=2024, x1=2024, y0=-15, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash"))
                    ]
                )
                .add_hline(
                    y=0,
                    line=dict(color='rgba(0,0,0,0.5)', width=2, dash='solid'),
                    opacity=1
                ),style={"width": "900px", "margin": "0 auto"}
        ),

        html.Div([  # comentarios alineados debajo del gráfico
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "2px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "2px"})
        ], style={"alignSelf": "flex-start", "marginLeft": "10px"})
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "margin": "0 auto"
    })

], style={"display": "flex", "flexDirection": "row"}),

    # Bloque 3: Inflacion
    html.Div([

        html.Div([  # fila: gráfico + descripción
            html.Div([
                dcc.Graph(
                    id="grafico_inflacion",
                    figure=px.scatter(df_mensual, x="fecha", y="inflacion_mensual", size_max=60)
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
                                    range=[pd.to_datetime("2016-11-01"), pd.to_datetime("2025-12-01")],
                                    showgrid=True,
                                    gridcolor='#E0E0E0',
                                    gridwidth=1,
                                    showline=True,
                                    linecolor='#E0E0E0',
                                    linewidth=1
                                ),
                                yaxis=dict(
                                    title="Inflación Mensual (variación en %)",
                                    range=[0, 28],
                                    dtick=5,
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
                                    dict(type="line", x0="2016-01-01", x1="2016-01-01", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0="2020-01-01", x1="2020-01-01", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0="2024-01-01", x1="2024-01-01", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                ]
                            )
                )
            ], style={"flex": 6, "padding": "10px"}),

            html.Div([  # descripción a la derecha
                html.H3("Descripción"),
                html.P("Mira ce aca hice la inflacion")
            ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"})
        ], style={"display": "flex", "flexDirection": "row"}),

        # Comentarios debajo del bloque de pobreza
        html.Div("Fecha: 31-08-2025", style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
        html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                 style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),

    # Bloque 2: PBI
    html.Div([

        html.Div([  # descripción a la izquierda
            html.H3("Descripción"),
            html.P("Este gráfico muestra la serie de tasa de crecimiento del PBI.")
        ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"}),
    html.Div([  # gráfico + comentarios
        dcc.Graph(
            id="grafico_tcn",
            figure=px.line(df_tcn, x="fecha_tcn", y="tcn")
                .update_traces(
                    mode='lines+markers',  # gráfico principal sigue con líneas y puntos
                    marker=dict(symbol='circle', size=2, color='#75AADB'),
                    line=dict(color='#75AADB', width=2),
                    hovertemplate="Año: %{x}<br>Valor: %{y:.2f}<extra></extra>"
                )
                .update_layout(
                    title="",
                    height=500,
                    xaxis=dict(
                        title="Año",
                        tickmode="linear",
                        tickformat="%Y",
                        dtick="M12",
                        showgrid=True,
                        range=["2025-01-01", df_tcn["fecha_tcn"].max()],
                        gridcolor='#E0E0E0',
                        gridwidth=1,
                        showline=True,
                        linecolor='#E0E0E0',
                        linewidth=1,
                        rangeslider=dict(
                        visible=True,
                        thickness=0.05,
                        bgcolor='#E0E0E0',
                        borderwidth=0
                    )
                    ),
                    yaxis=dict(
                        title="Tipo de cambio Nominal (en pesos)",
                        showgrid=True,
                        gridcolor='#E0E0E0',
                        gridwidth=1,
                        autorange=True  #hacer la escala movil
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                ),
            style={"width": "900px", "margin": "0 auto"}
        ),

        html.Div([  # comentarios alineados debajo del gráfico
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "2px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "2px"})
        ], style={"alignSelf": "flex-start", "marginLeft": "10px"})
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "margin": "0 auto"
    })

], style={"display": "flex", "flexDirection": "row"}),

    # Bloque 5: TASA
    html.Div([

        html.Div([  # fila: gráfico + descripción
            html.Div([
                dcc.Graph(
                    id="grafico_tasa",
                    figure=px.scatter(df_tasa, x="fecha_tasa", y="tasa_leliqs", size_max=60)
                            .update_traces(
                                mode='lines+markers',
                                marker=dict(symbol='circle', size=3, color='#75AADB'),
                                line=dict(color='#75AADB', width=2),
                                hovertemplate="Fecha: %{x|%d-%m-%Y}<br>Pobreza: %{y:.1f}%<extra></extra>"

                            )
                            .update_layout(
                                title="",
                                height=500,
                                xaxis=dict(
                                    title="Año",
                                    tickmode="array",
                                    tickformat="%Y",
                                    dtick="M12",
                                    range=["2024-01-01", df_tcn["fecha_tcn"].max()],
                                    fixedrange=True,
                                    showgrid=True,
                                    gridcolor='#E0E0E0',
                                    gridwidth=1,
                                    showline=True,
                                    linecolor='#E0E0E0',
                                    linewidth=1,
                                    rangeslider=dict(
                                    visible=True,
                                    thickness=0.05,
                                    bgcolor='#E0E0E0',
                                    borderwidth=0
                                )
                                ),
                                yaxis=dict(
                                    title="Población bajo la línea de pobreza (%)",
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
                                    dict(type="line", x0="01-01-2016", x1="01-01-2016", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0="01-01-2020", x1="01-01-2020", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                    dict(type="line", x0="01-01-2024", x1="01-01-2024", y0=0, y1=100,
                                         line=dict(color="#FFA500", width=1, dash="dash")),
                                ]
                            )
                )
            ], style={"flex": 6, "padding": "10px"}),

            html.Div([  # descripción a la derecha
                html.H3("Descripción"),
                html.P("Este gráfico muestra la tasa de politica monetaria.")
            ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"})
        ], style={"display": "flex", "flexDirection": "row"}),

        # Comentarios debajo del bloque de pobreza
        html.Div("Fecha: 31-08-2025", style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
        html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                 style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),

], style={"display": "flex", "flexDirection": "column"}),


#@app.callback(
  #  Output("grafico_tcn", "figure"),
 #   Input("grafico_tcn", "relayoutData")
#)
#def update_yaxis(relayout_data):
        #fig = px.line(df_tcn, x="fecha_tcn", y="tcn")

        # si hay rango elegido en x
        #if relayout_data and "xaxis.range" in relayout_data:
       #     x_min, x_max = relayout_data["xaxis.range"]

      #      # si el rango incluye años >= 2025
     #       if pd.to_datetime(x_max).year >= 2025:
    #            fig.update_layout(yaxis=dict(range=[500, None]))
   #         else:
  #              fig.update_layout(yaxis=dict(autorange=True))

 #       return fig


if __name__ == "__main__":
    app.run(debug=True)