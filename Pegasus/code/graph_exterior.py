
df_ied= pd.read_excel(data, sheet_name=14)
df_tot= pd.read_excel(data, sheet_name=13)
df_cc= pd.read_excel(data, sheet_name=12)

df_tot["fecha"] = pd.to_datetime(
    df_tot["fecha"],
    format="%d/%m/%Y",
    errors="coerce"
)

df_ied["fecha"] = pd.to_datetime(
    df_ied["fecha"],
    format="%Y/%m/%d",
    errors="coerce"
)


print(df_tot.dtypes)



exterior_layout = html.Div([



    #Graph: Cuenta corriente
    html.H2("", style={"textAlign": "center"}),

    html.Div([
        html.H2("Saldo de la Cuenta Corriente (%PBI)", style={"margin": 0}),
        dbc.Button("💬", id="btn-cc", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),
    
    dcc.Graph(
        id="grafico_cc",
        figure=px.scatter(df_cc, x="year", y="cc_pbi", size_max=60)
        .update_traces(
        mode='lines+markers',
        marker=dict(symbol='circle', size=6, color='#75AADB'),
        line=dict(color='#75AADB', width=2),
        hovertemplate="Año: %{x}<br>Porcentaje: %{y:.1f}%<extra></extra>"
        )
        .update_layout(
            title="",
            height=500,
            xaxis=dict(
                title="Año",
                tickmode="array",
                range=[1975, 2025],
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
                range=[-10, 10],
                dtick=2,
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
                dict(type="line", x0=1980, x1=1980, y0=-10, y1=10,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=1990, x1=1990, y0=-10, y1=10,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=2000, x1=2000, y0=-10, y1=10,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=2010, x1=2010, y0=-10, y1=10,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0=2020, x1=2020, y0=-10, y1=10,
                        line=dict(color="#FFA500", width=1, dash="dash")),
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
            "El gráfico presenta el ",
            html.Strong("saldo de la cuenta corriente"),
            " como ",
            html.Strong("porcentaje del PBI"),
            ". La cuenta corriente representa principalmente el ",
            html.Strong("saldo comercial de bienes y servicios"),
            " de un país con el resto del mundo. Desde el punto de vista macroeconómico, se cumple que ",
            html.Strong("Cuenta Corriente = Ahorro Nacional – Inversión"),
            ". Por lo tanto, un ",
            html.Strong("déficit"),
            " implica que la economía está invirtiendo por encima de su ahorro y se financia mediante endeudamiento externo o reducción de activos externos.",

            html.Br(), html.Br(),

            "Los déficits tienden a profundizarse durante fases de ",
            html.Strong("expansión del nivel de actividad"),
            " y ",
            html.Strong("apreciación del tipo de cambio real"),
            ", cuando las importaciones crecen más rápido que las exportaciones. En cambio, los ",
            html.Strong("superávits"),
            " suelen aparecer en contextos de crisis, devaluaciones o fuertes contracciones de la demanda interna, que reducen las importaciones y mejoran transitoriamente el saldo externo.",

            html.Br(), html.Br(),

            "Un ejemplo de esto es el ",
            html.Strong("superávit posterior a 2002"),
            ", explicado por una significativa depreciación real, la caída de las importaciones y la mejora en los términos de intercambio.",

            html.Br(), html.Br(),

            "En términos de sostenibilidad macroeconómica, los ",
            html.Strong("déficits persistentes"),
            " requieren ",
            html.Strong("financiamiento externo"),
            ". Cuando este se restringe, el ajuste suele producirse vía ",
            html.Strong("depreciación del tipo de cambio real"),
            ", ",
            html.Strong("reducción de importaciones"),
            " y ",
            html.Strong("caída del nivel de actividad"),
            ".",
        ])
                ],

        id="offcanvas-cc",
        title="Evolucion del saldo de la Cuenta Correinte",
        is_open=False,
        placement="end",
        ),

    html.Div([
            html.Div("Fecha: 08-02-2026",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Banco Mundial",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),

   
    #Graph: Indice TOT

    html.Div([
        html.H2("Indice de terminos de intercambio", style={"margin": 0}),
        dbc.Button("💬", id="btn-tot", n_clicks=0, size="sm", color="primary")
        ], style={
            "display": "flex",
            "alignItems": "center",   # centra verticalmente
            "justifyContent": "center",  # centra horizontalmente todo el bloque
            "gap": "10px",             # espacio entre título y botón
            "marginBottom": "10px"
        }),
    
    dcc.Graph(
        id="grafico_tot",
        figure=px.scatter(df_tot, x="fecha", y="tot", size_max=60)
        .update_traces(
        mode='lines+markers',
        marker=dict(symbol='circle', size=6, color='#75AADB'),
        line=dict(color='#75AADB', width=2),
        hovertemplate="Año: %{x}<br>Porcentaje: %{y:.1f}%<extra></extra>"
        )
        .update_xaxes(type="date")
        .update_layout(
            title="",
            height=500,
            xaxis=dict(
                title="Año",
                tickmode="array",
                range=["1989-6-01", "2025-12-31"],
                fixedrange=True,
                showgrid=True,
                gridcolor='#E0E0E0',
                gridwidth=1,
                showline=True,
                linecolor='#E0E0E0',
                linewidth=1
            ),
            yaxis=dict(
                title="Indice de terminos de intercambio (base 2006)",
                range=[50, 165],
                dtick=25,
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
                dict(type="line", x0="1990-01-01", x1="1990-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="1995-01-01", x1="1995-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2000-01-01", x1="2000-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2005-01-01", x1="2005-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2010-01-01", x1="2010-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2015-01-01", x1="2015-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2020-01-01", x1="2020-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
                dict(type="line", x0="2025-01-01", x1="2025-01-01", y0=50, y1=165,
                        line=dict(color="#FFA500", width=1, dash="dash")),
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
            "Un índice de términos de intercambio mide la evolución del ",
            html.Strong("precio relativo de las exportaciones respecto de las importaciones"),
            " (TOT = Px/Pm) de un país con relación a un año base (en este caso 2004). Un aumento del índice implica una mejora en los términos de intercambio, es decir, que el país puede obtener una mayor cantidad de importaciones por cada unidad exportada.",
            html.Br(),
            html.Br(),
            "La evolución de los términos de intercambio tiene efectos directos sobre el saldo de la cuenta corriente, ya que determina el valor relativo de las exportaciones e importaciones. Durante la ",
            html.Strong("primera década de los 2000"),
            ", Argentina experimentó una significativa ",
            html.Strong("mejora en los términos de intercambio"),
            ", lo que contribuyó a la reversión del ",
            html.Strong("déficit en cuenta corriente"),
            " observado en la década de 1990 y a la aparición de ",
            html.Strong("superávits en cuenta corriente"),
            " que persistieron aproximadamente hasta 2010, mejorando el poder de compra de las exportaciones nacionales",
            html.Br(),
        ])
        ],
        id="offcanvas-tot",
        title="Indice de Terminos de intercambio (base 2004)",
        is_open=False,
        placement="end",
        ),

    html.Div([
            html.Div("Fecha: 08-02-2026",
                     style={"color": "gray", "font-size": "12px", "margin-top": "4px"}),
            html.Div("Fuente: Instituto Nacional de Estadística y Censos de la República Argentina (INDEC)",
                     style={"color": "gray", "font-size": "12px", "margin-bottom": "10px"}),

    ], style={"display": "flex", "flexDirection": "column"}),


     #Graph: Indice IED - Necesito una base mas larga.





    #Boton volver
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

