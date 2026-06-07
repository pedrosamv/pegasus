

df_tcn= pd.read_excel(data, sheet_name=5)
df_tasa= pd.read_excel(data, sheet_name=4)




df_tcn["fecha_tcn"] = pd.to_datetime(df_tcn["fecha_tcn"], format="%Y-%m-%d") #que lo lea como fecha
df_tasa["fecha_tasa"] = pd.to_datetime(df_tasa["fecha"], format="%d-%m-%Y") #que lo lea como fecha



monetary_layout =html.Div([

    # Graph: Inflacion
    html.Div([
            html.Div([
        html.H2("Tasa de Inflación", style={"margin": 0}),
        dbc.Button("💬", id="btn-inflacion", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),
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

        dbc.Offcanvas(
    children=[
    html.P([
        "Este gráfico muestra la tasa de inflación mensual en porcentaje.",
        html.Br(),
        "Desde 2022 se observa una aceleración en el crecimiento de la inflación, alcanzando un máximo de ",
        html.Strong("25,5% en diciembre de 2023."),
        html.Br(),
        "El último dato oficial corresponde a julio de 2025, cuando la inflación mensual fue de ",
        html.Strong("1,9%."),
        html.Br(),
        html.Br(),
        html.Strong("Comparación:"),
        html.Br(),
        html.Strong("Brasil: "), 
        "27,3% (2023) ",
        html.Br(),
        html.Strong("Uruguay: "), 
        "17,3% (2024) ",
        html.Br(),
        html.Strong("Chile: "), 
        "22,3% (2024) "
    ])],
    id="offcanvas-inflacion",
    title="Tasa de Inflación",
    is_open=False,
    placement="end",
    ),

    html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),


            ], style={"display": "flex", "flexDirection": "column"}),




        #Graph: Tipo de Cambio Nominal



    # Graph: TCN
    html.Div([
            html.Div([
                html.H2("Tipo de cambio nominal", style={"margin": 0}),
            ]),
            dbc.Button("💬", id="btn-tcn", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "12px",
            "marginBottom": "10px"
        }),

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
                title="Tipo de cambio (peso por dolar)",
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
                        x1=pd.to_datetime("2016-01-01"), y0=0, y1=1400,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=pd.to_datetime("2020-01-01"),
                        x1=pd.to_datetime("2020-01-01"), y0=0, y1=1400,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=pd.to_datetime("2024-01-01"),
                        x1=pd.to_datetime("2024-01-01"), y0=0, y1=1400,
                        line=dict(color="#FFA500", width=1, dash="dash")),
            ])
            ),

    dbc.Offcanvas(
        children=[
        html.P([
            "Este gráfico muestra el tipo de cambio nominal (pesos por dólar) a lo largo de los años.",
            html.Br(),
             html.Br(),
            "Luego de la pandemia en el 2020 y principalmente sobre las elecciones de 2023, el valor del dólar aumento drásticamente, pasando de ",
            html.Strong("$180 en diciembre del 2022 hasta $829 a finales de 2023. "),
            html.Br(),
              html.Br(),
            "Otro suceso importante puede observarse en abril de 2025, cuando el Banco Central removió el régimen de",
            html.Strong(" tipo de cambio fijo"),
            " que se implementaba en el país hasta ese momento, pasandoa un ",
            html.Strong("esquema por bandas."),
            "En este mismo, el Banco Central se comprometía a solo intervenir en el valor del TCN cuando este pudiera traspasar los límites del mismo. ",
             html.Br(),
              html.Br(),
            "Inicialmente estos se establecieron en $1000 y $1400 pesos, en los cuales el tipo de cambio fluctúa libremente según la oferta y la demanda, y estos se ajustarían a un ",
            html.Strong("ritmo mensual del -1% y +1%.")
            
            
        ])],
        id="offcanvas-tcn",
        title="Tipo de Cambio Nominal",
        is_open=False,
        placement="end",
        ),
    html.Div([
            html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Ministerio de Economía",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),


            ], style={"display": "flex", "flexDirection": "column"}),


    # Graph: Tasa de interes
     html.Div([
            html.Div([
                html.H2("Tasa de Politica Monetaria", style={"margin": 0}),
            ]),
            dbc.Button("💬", id="btn-i", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "12px",
            "marginBottom": "10px"
        }),

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
    
    dbc.Offcanvas(
        children=[
        html.P([
            "La Tasa de Política Monetaria es una de las principales herramientas con las que cuenta el Banco Central para influir sobre la actividad económica y la inflación. ",
            html.Br(),
            "Un ",
            html.Strong("aumento "),
             "de la tasa de interés encarece el crédito y restringe el acceso al financiamiento, afectando particularmente a la inversión y al consumo. ",
            html.Br(),
            "Esta medida podía implementarse con el objetivo de ",
            html.Strong("reducir"),
            " la tasa de inflación, dado que al desacelerar la actividad económica mediante la contracción de la demanda agregada se genera una presión a la baja sobre el nivel de precios. ",
            html.Br(),
            "Sin embargo, su efectividad puede verse limitada en contextos donde predominan expectativas inflacionarias desancladas o persisten desequilibrios macroeconómicos estructurales que condicionan la dinámica inflacionaria.",
            html.Br(),
            html.Br(),
            "Por ejemplo, entre fines de 2018 y 2020 la inflación mensual se aceleró de manera significativa, pasando de valores cercanos al 1,6 % a aproximadamente 5,1 %, a pesar del fuerte endurecimiento de la política monetaria. ",
            "En los meses posteriores al inicio de este período, la tasa de política monetaria se elevó abruptamente desde niveles cercanos al 40 % hasta alcanzar un pico de 82,99 % en septiembre de 2019. ",
            "Para comienzos de 2020 se observó una desaceleración de la inflación, con una profunda recesión y contracción de la demanda"

            
            
            
            
        ])],
        id="offcanvas-i",
        title="Tasa de Politica Monetaria",
        is_open=False,
        placement="end",
        ),

    html.Div([
        html.Div("Fecha: 31-08-2025",
                    style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
        html.Div("Fuente: Ministerio de Economía",
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

