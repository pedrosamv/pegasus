df_anual= pd.read_excel(data, sheet_name=2)
df_des= pd.read_excel(data, sheet_name=8)
df_lorenz=pd.read_excel(data, sheet_name=10)


df_des["year"] = pd.to_datetime(df_des["year"].astype(str), format="%Y") #esto es por las dudas que entienda que year es un datetime



social_layout = html.Div([



    #Graph: Pobreza
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

    # Graph: Desempleo
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
        title="Evolución de la Tasa Desempleo (% población económicamente activa)",
        is_open=False,
        placement="end",
        ),
    html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Banco Mundial",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),


#Curva de lorenz

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
        html.H2("Distribución del ingreso (por semestres)", style={"margin": 0}),
        dbc.Button("💬", id="btn-lorenz", n_clicks=0, size="sm", color="primary")
        
    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "gap": "10px",
        "marginBottom": "10px"
    }),

    # ---- Gráfico ----
    dcc.Graph(id="grafico_lorenz"),
     dbc.Offcanvas(
        children=[
        html.P([
            "La curva de Lorenz muestra la distribución efectiva del ingreso y la línea de perfecta igualdad. Cuanto mayor es la distancia entre ambas curvas, mayor es el nivel de desigualdad. Esta desigualdad puede medirse mediante el coeficiente de Gini, que cuantifica el área comprendida entre dichas curvas.",
            html.Br(),
            html.Br(),
            "Si observamos el primer semestre de 2024, el", 
            html.Strong(" 50% de la población explica el 16%"), 
            " del ingreso total del país, mientras que el último decil (el 10% más rico) concentra el", 
            html.Strong(" 32,6%."),
            html.Br(),
            "Estos resultados muestran una mejora relativa en comparación con el año 2003, cuando el último decil concentraba el 37,8% del ingreso total.",
            html.Br(),
            "Para el segundo semestre de 2024, el coeficiente de gini fue de 0,435.",
             html.Br(),
            html.Br(),
            html.Strong("Comparación Gini"),
            html.Br(),
            html.Strong("Brasil: "), "0.506 (2024 - IBGE) ",
            html.Br(),
            html.Strong("Uruguay: "), "0.40 (2024 - WB) ",
        ])],
        id="offcanvas-lorenz",
        title="Distribución del ingreso",
        is_open=False,
        placement="end",
        ),

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

