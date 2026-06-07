#Librerias

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, html, dcc, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os 
import plotly.graph_objects as go
import textwrap
from dash import clientside_callback, ClientsideFunction


pip freeze > requirements.txt
git add requirements.txt
git commit -m "Agregar requirements"
git push



#Rutas
data= r"C:\Users\usuario\Dropbox\Python\Pegasus\base_data.xlsx"
code = r"C:\Users\usuario\Dropbox\Python\Pegasus\code"


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="background-color: white; color: #111111; margin: 0;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


globals_dict = globals()

# ========= Menu principal =========
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



# ========= Menu Horizontal =========
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Nav([
            dbc.DropdownMenu(
                label="Blog",
                nav=True,
                in_navbar=True,
                children=[

                    dbc.DropdownMenuItem(
                        "¿Qué pasó en la convertibilidad?",
                        href="/convertibilidad"
                    ),

                    dbc.DropdownMenuItem(
                        "Deuda Argentina: cómo se compone y cómo afecta la tasa de interés",
                        href="/deuda"
                    ),
                    dbc.DropdownMenuItem(
                        "Por que corno importa la tasa de interes?",
                        href="/tmm"
                    ),
                     dbc.DropdownMenuItem(
                        "Que pasa con la pobreza?",
                        href="/tmm"
                    ),


                ],
            ),

            dbc.NavItem(
                dbc.NavLink(
                    "Serie de tiempo",
                    href="/serie-tiempo",
                    className="nav-link",
                    style={"cursor": "pointer"}
                ),
            ),
             dbc.NavItem(
                dbc.NavLink(
                    "Noticias",
                    href="/news",
                    className="nav-link",
                    style={"cursor": "pointer"}
                ),
             ),
            
        ],
        navbar=True)
    ]),
    color="white",
    dark=False,
    className="shadow-sm"
)


# ========= Graphs inicio =========
df_anual= pd.read_excel(data, sheet_name=2)
df_mensual = pd.read_excel(data, sheet_name=0)
df_mensual["fecha"] = pd.to_datetime(df_mensual["year"].astype(str) + "-" + df_mensual["mes"].astype(str), format="%Y-%m")  #que junte las variables anio y mes para poner tipo datetime con y/m.

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

    navbar,

    # Gráfico inicial pobreza
    
    html.Div([
        # Columna izquierda: gráfico
        html.Div([
            html.H2("Tasa de pobreza", style={"margin": 0, "textAlign": "center"}),
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
            html.H2("Tasa de Inflación", style={"margin": 0, "textAlign": "center"}),
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
                html.P("Pobreza - Desempleo - Distribución del ingreso"),
            ], style=card_style), href="/social"
        ),

        dcc.Link(
            html.Div([
                html.Div("📊", style={"fontSize": "40px"}),
                html.H4("Fiscal"),
                html.P("PBI - Resultado fiscal - Deuda Pública"),
            ], style=card_style), href="/fiscal"
        ),

        dcc.Link(
            html.Div([
                html.Div("💸", style={"fontSize": "40px"}),
                html.H4("Monetario"),
                html.P("Inflación - TCN - Tasa de política monetaria"),
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

# ========= Graphs Argentina =========

# ========== Social ===========


with open(os.path.join(code, "graph_social.py"), encoding="utf-8") as social_layout:
    exec(social_layout.read(), globals())



# ========== Monetario ===========


with open(os.path.join(code, "graph_monetary.py"), encoding="utf-8") as monetary_layout:
    exec(monetary_layout.read(), globals())



# ========== Fiscal ===========


with open(os.path.join(code, "graph_fiscal.py"), encoding="utf-8") as fiscal_layout:
    exec(fiscal_layout.read(), globals())
    

# ========== Exterior ===========


with open(os.path.join(code, "graph_exterior.py"), encoding="utf-8") as exterior_layout:
    exec(exterior_layout.read(), globals())




# ========== Linea de tiempo ===========

with open(os.path.join(code, "timeline_argentina.py"), encoding="utf-8") as timeline_layout:
    exec(timeline_layout.read(), globals())


# ========== Blog ===========

with open(os.path.join(code, "blog.py"), encoding="utf-8") as blog_layout:
   exec(blog_layout.read(), globals())


# ========== News ===========

with open(os.path.join(code, "news.py"), encoding="utf-8") as news_layout:
   exec(news_layout.read(), globals())




# ========= Layout con router =========
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content")
])


# ========= Callbacks =========
with open(os.path.join(code, "callbacks.py"), encoding="utf-8") as callbacks_layout:
    exec(callbacks_layout.read(), globals())


if __name__ == "__main__":
    app.run(debug=True)
