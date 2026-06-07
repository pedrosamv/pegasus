df_serie_pbi= pd.read_excel(data, sheet_name=3)
df_anual= pd.read_excel(data, sheet_name=2)
df_deuda= pd.read_excel(data, sheet_name=7)
df_deuda_23= pd.read_excel(data, sheet_name=9)


df_serie_pbi["serie_tasa_pbi"] = pd.to_numeric(df_serie_pbi["serie_tasa_pbi"]) #que entienda que son numeros porque hay negativos.




fiscal_layout =html.Div([

    # Graph: PBI 
    html.Div([
        html.Div([  # gráfico + comentarios
            html.Div([ 
            html.H2("Tasa de crecimiento anual del PBI (%)", style={"margin": 0, "textAlign": "center"}),
            dbc.Button("💬", id="btn-pbi", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),


            dcc.Graph(
                id="grafico_pbi",
                figure=px.line(df_serie_pbi, x="year", y="serie_tasa_pbi")
                    .update_traces(
                        mode='lines',
                        marker=dict(size=6, color='#75AADB'),
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
                            title="Porcentaje (%)",
                            range=[-16, 15],
                            dtick=3,
                            showgrid=True,
                            gridcolor='#E0E0E0',
                            gridwidth=1
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        shapes=[
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
                    ),
                style={"width": "100%", "margin": "0 auto"}  # FULL WIDTH ✔
            ),

            html.Div([
                html.Div("Fecha: 31-08-2025",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
                html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),
            ], style={"alignSelf": "flex-start", "marginLeft": "10px"})
        ], style={
            "display": "flex",
            "flexDirection": "column",
            "margin": "0 auto",
            "width": "100%"     
        })

    ], style={"display": "flex", "flexDirection": "column", "width": "100%"}),

    dbc.Offcanvas(
        children=[
            html.P([
            "Este gráfico presenta la tasa de crecimiento anual del Producto Bruto Interno (PBI). "
            "En el caso de Argentina, se observa una ",
            html.Strong(" marcada volatilidad "),
            "a lo largo del tiempo. "
            "A diferencia de lo que ocurre en países con características económicas similares, "
            "donde los períodos de crecimiento o contracción suelen extenderse durante varios años consecutivos, "
            "la economía argentina muestra una ",
            html.Strong("dinámica más inestable. "),
            html.Br(),
            "En particular, durante las últimas dos décadas se evidencia una alternancia frecuente "
            "entre tasas de crecimiento positivas y negativas, sin una ",
            html.Strong("tendencia sostenida en el tiempo.")
           
            
            
        ])],
        id="offcanvas-pbi",
        title="Tasa de crecimiento anual del PBI (%)",
        is_open=False,
        placement="end",
        ),


    # Graph: Resultado fiscal y financiero
    html.Div([ 
            html.H2("Resultado fiscal y financiero (% del PBI)", style={"margin": 0, "textAlign": "center"}),
            dbc.Button("💬", id="btn-resultados", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "gap": "10px",
            "marginBottom": "10px"
        }),

    dcc.Graph(
            id="grafico_resultados",
            figure=px.line(
                df_anual,
                x="year",
                y=["r_primario_pbi","r_financiero_pbi"],
                labels={
                    "value": "Porcentaje del PBI",
                    "variable": "",
                    "r_primario_pbi": "Resultado Primario",
                    "r_financiero_pbi": "Resultado Financiero"
                },
                markers=True
            )
            .update_traces(
                selector=dict(name="Resultado Primario"),
                line=dict(color="#7B2CBF", width=3),
                hovertemplate="Año %{x}<br>Primario: %{y:.1f}%<extra></extra>"
            )
            .update_traces(
                selector=dict(name="Resultado Financiero"),
                line=dict(color="#1B5E20", width=3),
                hovertemplate="Año %{x}<br>Financiero: %{y:.1f}%<extra></extra>"
            )
            .update_layout(
                height=500,
                xaxis=dict(
                    title="Año",
                    tickmode="linear",
                    range=[2003, 2025],
                    showgrid=True,
                    gridcolor="#ECECEC",
                    showline=True,
                    linecolor="#CCCCCC"
                ),
                yaxis=dict(
                    title="Porcentaje del PBI",
                    range=[-16, 15],
                    dtick=3,
                    showgrid=True,
                    gridcolor="#ECECEC",
                    zeroline=False
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=40, r=20, t=20, b=40),

                shapes=[
                    dict(type="line", x0=a, x1=a, y0=-16, y1=15,
                        line=dict(color="#F0A500", width=1, dash="dot"))
                    for a in [2004, 2008, 2012, 2016, 2020, 2024]
                ]
            )
            .add_hline(
                y=0,
                line=dict(color="rgba(0,0,0,0.3)", width=2),
            ),
            style={"width": "100%", "margin": "0 auto"}
        ),


     dbc.Offcanvas(
        children=[
            html.P([
           html.P([
            "Este gráfico muestra el resultado fiscal primario y financiero como porcentaje del PBI. "
            "A partir de aproximadamente 2008 se observa una aceleración en el ",
            html.Strong("deterioro de la solvencia fiscal. "),
            html.Br(),
            "Hacia 2011, tanto el resultado primario como el financiero pasan a ser negativos. "
            "Esto implica que, incluso sin considerar los servicios de la deuda, los ingresos públicos "
            "resultan insuficientes para cubrir el gasto del sector público, dando lugar a un déficit persistente. ",
            html.Br(),
            "En consecuencia, la economía entra en una situación de déficit fiscal sistemático. ",
            html.Br(),
            "Esta dinámica es",
             html.Strong(" insostenible en el largo plazo, "), 
            "los déficits recurrentes deben corregirse, "
            "ya sea mediante financiamiento con emisión monetaria, un mayor endeudamiento, "
            "un aumento de la recaudación tributaria o a través de un ajuste del gasto público "
            "que permita generar resultados superavitarios.",
            html.Br(),
           
])

            
            
        ])],
        id="offcanvas-resultados",
        title="Resultado fiscal y financiero (% del PBI)",
        is_open=False,
        placement="end",
        ),


    #Graph: Deuda
    html.Div([

    # Fila con los dos gráficos
    html.Div([

        # Izquierda
        html.Div([
            html.H2("Composición de la deuda pública (% PIB) - 2025", style={"margin": 0, "textAlign": "center"}),
            dcc.Graph(
                id="grafico-torta-1",
                figure=px.pie(df_deuda, names="componente", values="deuda_porc"),
                style={"height": "400px"}
            )
        ], style={"width": "50%"}),

        # Derecha
        html.Div([
            html.H2("Composición de la deuda pública (% PIB) - 2023", style={"margin": 0, "textAlign": "center"}),
            dbc.Button("💬", id="btn-deuda", n_clicks=0, size="sm", color="primary"),
            dcc.Graph(
                id="grafico-torta-2",
                figure=px.pie(df_deuda_23, names="componente", values="deuda_porc"),
                style={"height": "400px"}
            )
        ], style={"width": "50%"})

    ], style={"display": "flex"}),

    # Bloque debajo de los gráficos
    html.Div([
        html.Div("Fecha: 31-08-2025", style={"color": "gray", "fontSize": "12px", "marginTop": "4px"}),
        html.Div("Fuente: Ministerio de Economía - Secretaría de Finanzas", style={"color": "gray", "fontSize": "12px"})
    ], style={"textAlign": "center", "marginTop": "10px"})

]),

    dbc.Offcanvas(
        children=[
            html.P([
            "La deuda pública nacional se compone mayoritariamente de ",
            html.Strong("títulos públicos"),
             ", es decir obligaciones de duda que emite el gobierno, seguido por el financiamiento mediante",
            html.Strong(" préstamos internacionales"),
            "y las ",
            html.Strong("letras del tesoro"),
             " estas últimas son ",
            html.Strong( "títulos de deuda"),
            " de corto plazo emitidos por el gobierno.",
            html.Br(),   
            "En el último año, uno de los cambios más destacables es la disminución de los préstamos internacionales, disminuyendo 4 puntos porcentuales desde 2023. En contraposición se observó un aumento en la emisión de letras del Tesoro. Esto se debe al traspaso de deuda en manos del Banco Central al Tesoro Nacional."
            
        ])],
        id="offcanvas-deuda",
        title="Composición de la deuda pública",
        is_open=False,
        placement="end",
        ),


    # Boton para volver
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
