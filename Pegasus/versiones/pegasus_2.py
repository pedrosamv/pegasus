#Aca importe todos los chiches que voy a usar.
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


df_mensual = pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=0)
df_trimestral= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=1)
df_anual= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=2)
df_serie_pbi= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=3)
df_tasa= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=4)
df_tcn= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=5)
df_deuda= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=7)
df_des= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=8)
df_deuda_23= pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=9)


df_tcn["fecha_tcn"] = pd.to_datetime(df_tcn["fecha_tcn"], format="%Y-%m-%d")
df_serie_pbi["serie_tasa_pbi"] = pd.to_numeric(df_serie_pbi["serie_tasa_pbi"])
df_tasa["fecha_tasa"] = pd.to_datetime(df_tasa["fecha"], format="%d-%m-%Y")


#df_anual["year"] = pd.to_datetime(df_anual["year"], format="%Y")
df_mensual["fecha"] = pd.to_datetime(df_mensual["year"].astype(str) + "-" + df_mensual["mes"].astype(str), format="%Y-%m")
df_w_des["fecha_desempleo"] = pd.to_datetime(df_w_des["year"].astype(str) + "-" + df_w_des["mes"].astype(str), format="%Y-%m")




#print(df_mensual.columns.tolist()) esto es para ver si leyo bien la base.


#app = Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




# ========= Layouts de cada sección =========


#Social
social_layout= html.Div([




  html.H2("", style={"textAlign": "center"}),
    # Botón arriba a la derecha
    html.Div([
        html.H2("Evolución de la Pobreza", style={"margin": 0}),
        dbc.Button("💬", id="btn-desempleo", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),
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
    dbc.Offcanvas(
        children=[
            html.P([
            "Este gráfico muestra el porcentaje de la población argentina bajo la línea de pobreza desde 2016. "
            "En promedio, durante los últimos 10 años, el 37,2% de los argentinos ha sido considerado pobre. ",
            html.Br(),
            "El último dato oficial corresponde a 2024, año en el que aproximadamente la ",
            html.Strong("mitad de la población argentina (52%)"),
            " se encontraba por debajo de la línea de pobreza. ",
            html.Br(),
            "La estimación más reciente para el corriente año indica un ",
            html.Strong("31,7%."),
            html.Br(),
            html.Br(),
            html.Strong("Comparación:"),
            html.Br(),
            html.Strong("Brasil: "), "27,3% (2023) ",
            html.Br(),
            html.Strong("Uruguay: "), "17,3% (2024) ",
            html.Br(),
            html.Strong("Chile: "), "22,3% (2024) "
        ])],
        id="offcanvas-pobreza",
        title="Evolucion de la Tasa de Pobreza (2016-2025)",
        is_open=False,
        placement="end",
        ),


    #Grafico desempleo
    html.H2("", style={"textAlign": "center"}),
    # Botón arriba a la derecha
    html.Div([
        html.H2("Tasa de desempleo", style={"margin": 0}),
        dbc.Button("💬", id="btn-desempleo", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),
    dcc.Graph(
        id="grafico_desempelo",
        figure=px.scatter(df_w_des, x="fecha_desempleo", y="desempleo", size_max=60)
         .update_layout(
            title="",
            height=500,
            xaxis=dict(
                title="Año",
                tickmode="array",
                range=[pd.to_datetime("2003-1"), pd.to_datetime("2025-1")],
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
                range=[40, 80],
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
                dict(type="line", x0=2016, x1=2016, y0=40, y1=80,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=2020, x1=2020, y0=40, y1=80,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=2024, x1=2024, y0=40, y1=80,
                        line=dict(color="#FFA500", width=1, dash="dash")),
            ]
        )
        ),
    dbc.Offcanvas(
        children=[
            html.P([
            "Este gráfico muestra el porcentaje de la población argentina bajo la línea de pobreza desde 2016. "
            "En promedio, durante los últimos 10 años, el 37,2% de los argentinos ha sido considerado pobre. ",
            html.Br(),
            "El último dato oficial corresponde a 2024, año en el que aproximadamente la ",
            html.Strong("mitad de la población argentina (52%)"),
            " se encontraba por debajo de la línea de pobreza. ",
            html.Br(),
            "La estimación más reciente para el corriente año indica un ",
            html.Strong("31,7%."),
            html.Br(),
            html.Br(),
            html.Strong("Comparación:"),
            html.Br(),
            html.Strong("Brasil: "), "27,3% (2023) ",
            html.Br(),
            html.Strong("Uruguay: "), "17,3% (2024) ",
            html.Br(),
            html.Strong("Chile: "), "22,3% (2024) "
        ])],
        id="offcanvas-desempleo",
        title="Evolucion de la Tasa de Pobreza (2016-2025)",
        is_open=False,
        placement="end",
        ),


    html.H2(" Rari -Salario O Ingresos (PPP - $)", style={"textAlign": "center"}),
    dcc.Graph(
    id="grafico_salario",
    figure=px.scatter(df_w_des, x="fecha_desempleo", y=["w_formal","w_informal"], size_max=60)
            .update_layout(
            title="",
            height=500,
            xaxis=dict(
                title="Año",
                tickmode="array",
                range=[pd.to_datetime("2003-1"), pd.to_datetime("2025-1")],
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
                range=[0, 20],
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


#Monetario
monetary_layout=html.Div([
        # Columna izquierda: gráfico
        html.Div([
            dcc.Graph(
                id="grafico_inflacion",
                figure=px.scatter(df_mensual, x="fecha", y="inflacion_mensual", size_max=60)
                .update_traces(
                    mode='lines+markers',
                    marker=dict(symbol='circle', size=6, color='#75AADB'),
                    line=dict(color='#75AADB', width=2),
                    hovertemplate="Fecha: %{x}<br>Inflación: %{y:.1f}%<extra></extra>"
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
                        dict(type="line", x0=pd.to_datetime("2016-01-01"),
                             x1=pd.to_datetime("2016-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=pd.to_datetime("2020-01-01"),
                             x1=pd.to_datetime("2020-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=pd.to_datetime("2024-01-01"),
                             x1=pd.to_datetime("2024-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                    ]
                )
            )
        ], style={"flex": 6, "padding": "10px"}),


    html.H2("Tipo de Cambio Nominal", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_tcn",
        figure=px.line(df_tcn, x="fecha_tcn", y="tcn")
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=2, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
        .update_layout(
            title="",
            height=500,
            xaxis=dict(
                title="Año",
                tickmode="array",
                range=[pd.to_datetime("2016-11-01"), pd.to_datetime("2025-08-26")],
                showgrid=True,
                gridcolor='#E0E0E0',
                gridwidth=1,
                showline=True,
                linecolor='#E0E0E0',
                linewidth=1
            ),
            yaxis=dict(
                title="Inflación Mensual (variación en %)",
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
                dict(type="line", x0=pd.to_datetime("2016-01-01"),
                        x1=pd.to_datetime("2016-01-01"), y0=0, y1=100,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=pd.to_datetime("2020-01-01"),
                        x1=pd.to_datetime("2020-01-01"), y0=0, y1=100,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=pd.to_datetime("2024-01-01"),
                        x1=pd.to_datetime("2024-01-01"), y0=0, y1=100,
                        line=dict(color="#FFA500", width=1, dash="dash")),
            ])
            ),


    html.H2("Tasa de Política Monetaria", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_tasa",
        figure=px.scatter(df_tasa, x="fecha_tasa", y="tasa_leliqs", size_max=60)
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=3, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
        .update_layout(
        title="",
        height=500,
        xaxis=dict(
            title="Año",
            tickmode="array",
            showgrid=True,
            gridcolor='#E0E0E0',
            gridwidth=1,
            showline=True,
            linecolor='#E0E0E0',
            linewidth=1
        ),
        yaxis=dict(
            title="Inflación Mensual (variación en %)",
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
            dict(type="line", x0=pd.to_datetime("2016-01-01"),
                    x1=pd.to_datetime("2016-01-01"), y0=0, y1=100,
                    line=dict(color="#FFA500", width=1, dash="dash")),
            dict(type="line", x0=pd.to_datetime("2020-01-01"),
                    x1=pd.to_datetime("2020-01-01"), y0=0, y1=100,
                    line=dict(color="#FFA500", width=1, dash="dash")),
            dict(type="line", x0=pd.to_datetime("2024-01-01"),
                    x1=pd.to_datetime("2024-01-01"), y0=0, y1=100,
                    line=dict(color="#FFA500", width=1, dash="dash")),
        ]
    )
    ),
    dcc.Link("⬅ Volver al inicio", href="/")
])


# Fiscal
fiscal_layout = html.Div([
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


    html.H2("Crecimiento del PBI", style={"textAlign": "center"}),
    dcc.Graph(
        id="grafico_r_fiscal",
        figure=px.line(df_anual, x="year", y=["r_primario_pbi","r_financiero_pbi"])
        .update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=6, color='#75AADB'),
            line=dict(color='#75AADB', width=2)
        )
    ),
html.Div([
    # Primer gráfico
    html.Div([
        html.H2("Crecimiento del PBI - 2025", style={"textAlign": "center"}),
        dcc.Graph(
            id="grafico-torta-1",
            figure=px.pie(
                df_deuda,
                names="componente",
                values="deuda_porc",
                hole=0
            ),
            style={"height": "400px"}  # 🔹 alto fijo
        )
    ], style={"width": "50%", "display": "inline-block"}),


    # Segundo gráfico
    html.Div([
        html.H2("Crecimiento del PBI - 2023", style={"textAlign": "center"}),
        dcc.Graph(
            id="grafico-torta-2",
            figure=px.pie(
                df_deuda_23,
                names="componente",
                values="deuda_porc",
                hole=0
            ),
            style={"height": "400px"}  # 🔹 alto fijo
        )
    ], style={"width": "50%", "display": "inline-block"})
], style={"display": "flex"}),




    dcc.Link("⬅ Volver al inicio", href="/")
])


# Tasa Leliq
exterior_layout = html.Div([
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


    # Encabezado
    html.Div([
        html.H1(
            "Argentina, que corno te pasa?",
            style={
                "color": "white",
                "font-family": "Arial, sans-serif",
                "margin-bottom": "10px"
            }
        ),
        html.P(
            "Mira ce, en esta paginita podes mirar datitos faciles de argentina, todo esta chequeado",
            style={
                "color": "white",
                "font-family": "Arial, sans-serif",
                "font-size": "16px",
                "margin-top": "0"
            }
        )
    ], style={
        "background-color": "#000967",  # azul oscuro
        "padding": "40px",
        "text-align": "center"
    }),


    # Gráfico inicial pobreza
    html.Div([
        # Columna izquierda: gráfico
        html.Div([
            dcc.Graph(
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


        # Columna derecha: descripción + comparación
        html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),


            html.Div([
                # Descripción
                html.Div([
                    html.H3("Descripción:"),
                    html.Div([
                        "Este gráfico muestra el porcentaje de la población argentina bajo la línea de pobreza desde 2016.",
                        html.Br(),
                        "En promedio, durante los últimos 10 años, el 37,2% de los argentinos ha sido considerado pobre.",
                        html.Br(),
                        "El último dato oficial corresponde a 2024, año en el que aproximadamente la ",
                        html.Strong("mitad de la población argentina (52%)"),
                        " se encontraba por debajo de la línea de pobreza.",
                        html.Br(),
                        "La estimación más reciente para el corriente año indica un ",
                        html.Strong("31,7%.")
                    ], style={"lineHeight": "1.5"})
                ], style={"flex": "1", "padding": "10px"}),


                # Comparación
                html.Div([
                    html.H3("Comparación:"),
                    html.Div([
                        html.Strong("Brasil: "), "27,3% (2023) ",
                        html.Br(),
                        html.Strong("Uruguay: "), "17,3% (2024) ",
                        html.Br(),
                        html.Strong("Chile: "), "22,3% (2024) "
                    ], style={"lineHeight": "1.5"})
                ], style={"flex": "1", "padding": "10px"}),


            ], style={"display": "flex", "flexDirection": "row"})
        ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"}),


    ], style={"display": "flex", "flexDirection": "column"}),


    # Gráfico inicial inflación
    html.Div([
        # Columna izquierda: gráfico
        html.Div([
            dcc.Graph(
                id="grafico_inflacion",
                figure=px.scatter(df_mensual, x="fecha", y="inflacion_mensual", size_max=60)
                .update_traces(
                    mode='lines+markers',
                    marker=dict(symbol='circle', size=6, color='#75AADB'),
                    line=dict(color='#75AADB', width=2),
                    hovertemplate="Fecha: %{x}<br>Inflación: %{y:.1f}%<extra></extra>"
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
                        dict(type="line", x0=pd.to_datetime("2016-01-01"),
                             x1=pd.to_datetime("2016-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=pd.to_datetime("2020-01-01"),
                             x1=pd.to_datetime("2020-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                        dict(type="line", x0=pd.to_datetime("2024-01-01"),
                             x1=pd.to_datetime("2024-01-01"), y0=0, y1=100,
                             line=dict(color="#FFA500", width=1, dash="dash")),
                    ]
                )
            )
        ], style={"flex": 6, "padding": "10px"}),


        # Columna derecha: descripción + comparación
        html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),


            html.Div([
                # Descripción
                html.Div([
                    html.H3("Descripción:"),
                    html.Div([
                        "Este gráfico muestra la tasa de inflación mensual en porcentaje.",
                        html.Br(),
                        "Desde 2022 se observa una aceleración en el crecimiento de la inflación, alcanzando un máximo de ",
                        html.Strong("25,5% en diciembre de 2023."),
                        html.Br(),
                        "El último dato oficial corresponde a julio de 2025, cuando la inflación mensual fue de ",
                        html.Strong("1,9%.")
                    ], style={"lineHeight": "1.5"})
                ], style={"flex": "1", "padding": "10px"}),


                # Comparación
                html.Div([
                    html.H3("Comparación:"),
                    html.Div([
                        html.Strong("Brasil: "), "27,3% (2023) ",
                        html.Br(),
                        html.Strong("Uruguay: "), "17,3% (2024) ",
                        html.Br(),
                        html.Strong("Chile: "), "22,3% (2024) "
                    ], style={"lineHeight": "1.5"})
                ], style={"flex": "1", "padding": "10px"}),


            ], style={"display": "flex", "flexDirection": "row"})
        ], style={"flex": 4, "padding": "20px", "borderRadius": "10px"}),


    ], style={"display": "flex", "flexDirection": "column"}),  # <-- cierre agregado aquí


    # Secciones
    html.Div([
        dcc.Link(
            html.Div([
                html.Div("📉", style={"fontSize": "40px"}),
                html.H4("Social"),
                html.P("Evolución de la pobreza en Argentina."),
            ], style=card_style), href="/social"
        ),


        dcc.Link(
            html.Div([
                html.Div("📊", style={"fontSize": "40px"}),
                html.H4("Fiscal"),
                html.P("Serie de tasa de crecimiento del PBI."),
            ], style=card_style), href="/fiscal"
        ),


        dcc.Link(
            html.Div([
                html.Div("💸", style={"fontSize": "40px"}),
                html.H4("Monetario"),
                html.P("Evolución de la inflación mensual."),
            ], style=card_style), href="/monetario"
        ),


        dcc.Link(
            html.Div([
                html.Div("💱", style={"fontSize": "40px"}),
                html.H4("Exterior"),
                html.P("Evolución del tipo de cambio nominal."),
            ], style=card_style), href="/exterior"
        ),




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
    if pathname == "/social":
        return social_layout
    elif pathname == "/fiscal":
        return fiscal_layout
    elif pathname == "/monetario":
        return monetary_layout
    elif pathname == "/exterior":
        return exterior_layout
    else:
        return home_layout


@app.callback(
    Output("offcanvas-pobreza", "is_open"),
    Input("btn-pobreza", "n_clicks"),
    State("offcanvas-pobreza", "is_open")
)
def toggle_pobreza(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("offcanvas-desempleo", "is_open"),
    Input("btn-desempleo", "n_clicks"),
    State("offcanvas-desempleo", "is_open")
)
def toggle_desempleo(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open




if __name__ == "__main__":
    app.run(debug=True)
