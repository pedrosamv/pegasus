# ========= Callbacks =========



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
    elif pathname == "/serie-tiempo":
        return timeline_layout
    elif pathname == "/news":
            return news_layout
    elif pathname == "/convertibilidad":
        return convertibilidad_layout
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

@app.callback(  #este es el boton de comentario de pbi
    Output("offcanvas-pbi", "is_open"),
    Input("btn-pbi", "n_clicks"),
    State("offcanvas-pbi", "is_open")
)
def toggle_pbi(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de lorenz
    Output("offcanvas-lorenz", "is_open"),
    Input("btn-lorenz", "n_clicks"),
    State("offcanvas-lorenz", "is_open")
)

def toggle_lorenz(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de Resultados fiscal y financiero
    Output("offcanvas-resultados", "is_open"),
    Input("btn-resultados", "n_clicks"),
    State("offcanvas-resultados", "is_open")
)

def toggle_resultados(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de deuda
    Output("offcanvas-deuda", "is_open"),
    Input("btn-deuda", "n_clicks"),
    State("offcanvas-deuda", "is_open")
)

def toggle_deuda(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open



@app.callback(  #este es el boton de comentario de inflacion
    Output("offcanvas-inflacion", "is_open"),
    Input("btn-inflacion", "n_clicks"),
    State("offcanvas-inflacion", "is_open")
)

def toggle_inflacion(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de TCN
    Output("offcanvas-tcn", "is_open"),
    Input("btn-tcn", "n_clicks"),
    State("offcanvas-tcn", "is_open")
)

def toggle_tcn(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de TCN
    Output("offcanvas-i", "is_open"),
    Input("btn-i", "n_clicks"),
    State("offcanvas-i", "is_open")
)

def toggle_i(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de CC
    Output("offcanvas-cc", "is_open"),
    Input("btn-cc", "n_clicks"),
    State("offcanvas-cc", "is_open")
)

def toggle_resultados(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(  #este es el boton de comentario de TOT
    Output("offcanvas-tot", "is_open"),
    Input("btn-tot", "n_clicks"),
    State("offcanvas-tot", "is_open")
)

def toggle_resultados(n_clicks, is_open):
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

# ── Callbacks de noticias — pegá esto al final de tu callbacks.py ─────────────
# (los toggles de análisis son clientside para no recargar el feed completo)

from dash import clientside_callback, ClientsideFunction

# Toggle individual de cada análisis — clientside (sin round-trip al servidor)
app.clientside_callback(
    """
    function(n, is_open) {
        if (n) return !is_open;
        return is_open;
    }
    """,
    Output({"type": "analisis-collapse", "index": dash.MATCH}, "is_open"),
    Input({"type": "btn-analisis",       "index": dash.MATCH}, "n_clicks"),
    State({"type": "analisis-collapse",  "index": dash.MATCH}, "is_open"),
    prevent_initial_call=True,
)


@app.callback(
    Output("news-feed-container", "children"),
    Output("news-week-label",     "children"),
    Output("news-semana-actual",  "data"),
    Input("news-btn-prev",        "n_clicks"),
    Input("news-btn-next",        "n_clicks"),
    Input("news-rubro-activo",    "data"),
    State("news-semana-actual",   "data"),
    State("news-semanas-lista",   "data"),
    prevent_initial_call=True,
)
def navegar_semana(prev_clicks, next_clicks, rubro, semana_actual, semanas):
    from dash import ctx
    if not semanas:
        return [], "Sin semanas", semana_actual

    idx = semanas.index(semana_actual) if semana_actual in semanas else 0

    if ctx.triggered_id == "news-btn-prev" and idx < len(semanas) - 1:
        idx += 1
    elif ctx.triggered_id == "news-btn-next" and idx > 0:
        idx -= 1

    nueva_semana = semanas[idx]
    label = _fmt_week_label(nueva_semana)
    feed  = _build_feed(nueva_semana, rubro or "todos")
    return feed, label, nueva_semana


@app.callback(
    Output("news-rubro-activo",   "data"),
    Output("news-feed-container", "children", allow_duplicate=True),
    [Input(f"pill-{r}", "n_clicks") for r in RUBROS],
    State("news-semana-actual", "data"),
    prevent_initial_call=True,
)
def filtrar_rubro(*args):
    from dash import ctx
    semana_actual = args[-1]
    triggered = ctx.triggered_id or "pill-todos"
    rubro = triggered.replace("pill-", "")
    feed  = _build_feed(semana_actual or "", rubro)
    return rubro, feed