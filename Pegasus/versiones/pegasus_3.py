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
df_lorenz=pd.read_excel(r"C:\Users\usuario\Dropbox\Pegasus\base_data.xlsx", sheet_name=10)

df_tcn["fecha_tcn"] = pd.to_datetime(df_tcn["fecha_tcn"], format="%Y-%m-%d") #que lo lea como fecha
df_serie_pbi["serie_tasa_pbi"] = pd.to_numeric(df_serie_pbi["serie_tasa_pbi"]) #que entienda que son numeros porque hay negativos.
df_tasa["fecha_tasa"] = pd.to_datetime(df_tasa["fecha"], format="%d-%m-%Y") #que lo lea como fecha
df_mensual["fecha"] = pd.to_datetime(df_mensual["year"].astype(str) + "-" + df_mensual["mes"].astype(str), format="%Y-%m")  #que junte las variables anio y mes para poner tipo datetime con y/m.
df_des["year"] = pd.to_datetime(df_des["year"].astype(str), format="%Y") #esto es por las dudas que entienda que year es un datetime
#df_lorenz["fecha"] = pd.to_datetime(df_lorenz["year"], format="%Y-%m")


#print(df_mensual.columns.tolist()) esto es para ver si leyo bien la base.

#app = Dash(__name__)
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)



# ========= Layouts de cada sección =========

#Social
social_layout= html.Div([




  html.H2("", style={"textAlign": "center"}),
    # Botón arriba a la derecha
    html.Div([
        html.H2("Evolución de la Pobreza", style={"margin": 0}),
        dbc.Button("💬", id="btn-pobreza", n_clicks=0, size="sm", color="primary")
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

    html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),


html.H2("", style={"textAlign": "center"}),

    html.Div([
        html.H2("Evolución del Desempleo", style={"margin": 0}),
        dbc.Button("💬", id="btn-desempleo", n_clicks=0, size="sm", color="primary")
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "10px",
        "marginBottom": "10px"
    }),
    dcc.Graph(
    id="grafico_desempleo",
    figure=px.scatter(df_des, x="year", y="desempleo", size_max=60)
         .update_traces(
        mode='lines+markers',
        marker=dict(symbol='circle', size=6, color='#75AADB'),
        line=dict(color='#75AADB', width=2),
        hovertemplate="Año: %{x}<br>desempleo: %{y:.1f}%<extra></extra>"
        )
        .update_layout(
            title="",
            height=500,
            xaxis=dict(
                 title="Año",
                tickmode="auto",
                fixedrange=True,
                showgrid=True,
                gridcolor='#E0E0E0',
                gridwidth=1,
                showline=True,
                linecolor='#E0E0E0',
                linewidth=1
            ),
            yaxis=dict(
                title="Tasa de desempleo (% poblacion activa)",
                range=[-5, 30],
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
        )
    ),
    dbc.Offcanvas(
        children=[
            html.P([
            "Este gráfico muestra la evolución del porcentaje de la población económicamente activa que se encuentra desocupada, es decir, personas en edad de trabajar que tienen empleo o lo buscan activamente.",
            html.Br(),
            "Se observa un fuerte aumento del desempleo durante los primeros años de la convertibilidad, hasta 1995. Luego hay una mejora temporal, seguida de un rápido incremento hacia fines de la década, probablemente asociado a la crisis del modelo económico.",
            html.Br(),
            "Estos niveles relativamente altos se mantienen hasta los años posteriores a la crisis de 2001, tras lo cual se advierte una marcada caída y una etapa de mayor estabilidad.",
            html.Br(),
            "El último dato oficial corresponde a 2024, año en el que aproximadamente ",
            html.Strong("el 7,9% de la población económicamente activa"),
            " se encontraba desempleada.",
            html.Br(),
            html.Br(),
            html.Strong("Comparación:"),
            html.Br(),
            html.Strong("Brasil: "), "6,2% (2024) ",
            html.Br(),
            html.Strong("Uruguay: "), "7,4% (2024) ",
            html.Br(),
            html.Strong("Chile: "), "8,5% (2024) "
        ])],
        id="offcanvas-desempleo",
        title="Evolucion de la Tasa de Pobreza (2016-2025)",
        is_open=False,
        placement="end",
        ),
    html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Banco Mundial",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),



 # ---- Filtro de Año ----
    html.Div([
        html.Label("Seleccionar año:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="selector-anio-lorenz",
            options=[
                {"label": col, "value": col}
                for col in df_lorenz.columns if col != "decil"
            ],
            value="2003-12",
            multi=True, 
            clearable=False,
            style={"width": "220px", "margin": "0 auto"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # ---- Título + botón ----
    html.Div([
        html.H2("Distribución del ingreso", style={"margin": 0}),
        
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "10px",
        "marginBottom": "10px"
    }),

    # ---- Gráfico ----
    dcc.Graph(id="grafico_lorenz"),


html.Div([
            html.Div("Fecha: 8-12-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Centro de Estudios Distributivos, Laborales y Sociales (CEDLAS)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),

    dcc.Link(
    "⬅ Volver al inicio",
    href="/",
    style={
        "display": "inline-block",
        "marginTop": "20px",
        "padding": "10px 18px",
        "backgroundColor": "#000967",  # ← fondo azul solicitado
        "color": "white",               # ← flecha y texto blancos
        "borderRadius": "12px",
        "textDecoration": "none",
        "fontSize": "16px",
        "fontWeight": "500",
        "boxShadow": "0px 2px 6px rgba(0,0,0,0.20)",
    }
    )



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
    html.Div([
    html.Div([  # gráfico + comentarios
        html.Div("Tasa de crecimiento anual del PBI (%)", style={"textAlign": "center"}),
        dcc.Graph(
            id="grafico_pbi",
            figure=px.line(df_serie_pbi, x="year", y="serie_tasa_pbi")
                .update_traces(
                    mode='lines',  # gráfico principal sigue con líneas y puntos
                    marker=dict( size=6, color='#75AADB'),
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
                ),style={"width": "100%", "margin": "0 auto"}
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
        "margin": "0 auto"
    })

], style={"display": "flex", "flexDirection": "column", "width": "100%"}),



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
card_style = {   #esto es para ponerlo facha.
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
@app.callback(Output("page-content", "children"),   #aca poner los call para los botones.
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

@app.callback(  #este es el boton de comentario de pobreza
    Output("offcanvas-pobreza", "is_open"),
    Input("btn-pobreza", "n_clicks"),
    State("offcanvas-pobreza", "is_open")
)
def toggle_pobreza(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(    #este es el boton de comentario de desempleo
    Output("offcanvas-desempleo", "is_open"),
    Input("btn-desempleo", "n_clicks"),
    State("offcanvas-desempleo", "is_open")
)
def toggle_desempleo(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("grafico_lorenz", "figure"),
    Input("selector-anio-lorenz", "value")
)
def actualizar_grafico_lorenz(anios_seleccionados):

    fig = go.Figure()

    # --- Línea de perfecta igualdad (amarilla) ---
    fig.add_trace(go.Scatter(
        x=[0, 10],
        y=[0, 100],
        mode="lines",
        name="Línea de perfecta igualdad",
        line=dict(color="#FFA500", width=3, dash="dash")  # AMARILLO
    ))

    # --- Líneas de años seleccionados ---
    if isinstance(anios_seleccionados, str):
        anios_seleccionados = [anios_seleccionados]

    for anio in anios_seleccionados:
        fig.add_trace(go.Scatter(
            x=df_lorenz["decil"],
            y=df_lorenz[anio],
            mode="lines+markers",
            name=str(anio),
            marker=dict(size=6),
            line=dict(width=2)
        ))

    # --- Layout igual a tus otros gráficos ---
    fig.update_layout(
        title="Curva de Lorenz",
        height=500,
        xaxis=dict(
            title="Decil",
            tickmode="array",
            tickvals=df_lorenz["decil"],
            showgrid=True,
            gridcolor="#E0E0E0",
            gridwidth=1,
            showline=True,
            linecolor="#E0E0E0",
            linewidth=1
        ),
        yaxis=dict(
            title="Participación acumulada del ingreso (%)",
            range=[-5, 105],
            dtick=10,
            showgrid=True,
            gridcolor="#E0E0E0",
            gridwidth=1,
            showline=True,
            linecolor="#E0E0E0",
            linewidth=1
        ),
        plot_bgcolor="rgba(0,0,0,0)",     # fondo del área transparente
        paper_bgcolor="rgba(0,0,0,0)",    # fondo del papel transparente
        legend=dict(title="Años")
    )

    return fig



if __name__ == "__main__":
    app.run(debug=True)