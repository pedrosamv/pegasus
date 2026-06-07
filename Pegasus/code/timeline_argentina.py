

# ── Datos ────────────────────────────────────────────────────────────────────
events = [
    {"year": 1950, "label": "ISI", "text": "Aplicación del modelo económico basado en la Industrialización por Sustitución de Importaciones. Se buscaba reemplazar bienes manufacturados importados por producción nacional. Esto se tradujo en altos aranceles a las importaciones, acceso al crédito industrial y la creación de instituciones orientadas a promover y financiar la producción local", "side": "left", "color": "#1565C0"},
    {"year": 1976, "label": "Crisis del Estado", "text": "Crisis del Estado Benefactor con un fuerte desequilibrio fiscal, inicio de un proceso de desindustrialización, fuerte crecimiento del sector financiero y tablita cambiaria (devaluaciones programadas)", "side": "right", "color": "#C62828"},
    {"year": 1980, "label": "Deuda externa", "text": "Aumento de la deuda externa, consecuencia de la liberalización financiera y las altas tasas de interés internas. La devaluación y alto nivel de especulación financiera incentivaron la fuga de capitales.", "side": "left", "color": "#FFD344"},
    {"year": 1991, "label": "Convertibilidad", "text": "Inicio de la convertibilidad, con la adopción de un régimen de tipo de cambio fijo, acompañado por una profunda liberalización de los mercados y reformas laborales. Estas transformaciones impulsaron el ingreso de inversión extranjera directa (IED), pero también contribuyeron al deterioro de las condiciones laborales y la pérdida de participación relativa del sector industrial en la economía.", "side": "right", "color": "#2E7D32"},
    {"year": 2000, "label": "Fin de la convertibilidad", "text": "Las recurrentes crisis internacionales de la época y la alta desregulación financiera generaron una fuga de capitales, presionando el tipo de cambio y haciendo el esquema cambiario insostenible. Además, el fuerte descontento social por la alta tasa de pobreza y las condiciones laborales, hicieron que a principios de los 2000 se abandonara este esquema. ", "side": "left", "color": "#C928A0"},
    {"year": 2008, "label": "Post-convertibilidad", "text": "La fuerte devaluación del peso y la reforma laboral mejoraron los salarios y aumentaron el empleo registrado. También se observó un doble superávit gemelo, en parte explicado por el aumento de los términos de intercambio (TOT), incentivando así la producción local, con un fuerte impacto en el sector agro. El sector industrial también presentó un fuerte crecimiento al retomarse las medidas proteccionistas, principalmente aranceles.", "side": "right", "color": "#3292B8"},
    {"year": 2015, "label": "Cambio de gobierno", "text": "Fuerte periodo de endeudamiento, el principal fue el préstamo con el FMI de 50 000 millones de dólares, el más grande de la historia del organismo y equivalente a un 11 % del PBI de la Argentina en 2018. Con el gran descontento financiero, el BCRA incrementó drásticamente las tasas de interés de las LEBACs durante 2018 para frenar una corrida cambiaria, generando una fuerte recesión en la economía con un alto nivel de inflacion. ", "side": "left", "color": "#E65100"},
    {"year": 2020, "label": "Pandemia", "text": "Pandemia y cuarentena.", "side": "right", "color": "#6A1B9A"},
]

FONTS_URL = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap"

WRAP = {
    "background": "#ffffff",
    "minHeight": "100vh",
    "padding": "48px 24px 100px",
    "fontFamily": "'Source Sans 3', sans-serif",
    "color": "#1a1a2e",
}

INNER = {
    "maxWidth": "1100px",
    "margin": "0 auto",
}

TITLE_STYLE = {
    "fontFamily": "'Playfair Display', serif",
    "fontSize": "clamp(1.8rem, 4vw, 2.6rem)",
    "color": "#111111",
    "letterSpacing": "-0.5px",
    "marginBottom": "6px",
}

SUBTITLE_STYLE = {
    "fontSize": "0.95rem",
    "color": "#888888",
    "fontWeight": "300",
    "marginBottom": "56px",
    "letterSpacing": "0.3px",
}

TIMELINE_STYLE = {
    "position": "relative",
    "display": "flex",
    "flexDirection": "column",
}

ROW_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "1fr 56px 1fr",
    "alignItems": "start",
    "minHeight": "110px",
    "padding": "12px 0",
    "position": "relative",
}

NODE_COL_STYLE = {
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",
    "position": "relative",
    "zIndex": "2",
    "paddingTop": "4px",
}

YEAR_STYLE = {
    "fontSize": "0.68rem",
    "fontWeight": "600",
    "letterSpacing": "1.5px",
    "color": "#999999",
    "marginTop": "6px",
    "textTransform": "uppercase",
    "fontFamily": "'Source Sans 3', sans-serif",
}

CARD_BASE = {
    "background": "#f8f9fa",
    "border": "1px solid #e0e0e0",
    "borderRadius": "8px",
    "padding": "14px 16px",
    "maxWidth": "420px",
    "position": "relative",
}

CARD_LEFT  = {**CARD_BASE, "marginLeft": "auto",  "marginRight": "16px"}
CARD_RIGHT = {**CARD_BASE, "marginRight": "auto", "marginLeft": "16px"}

LABEL_STYLE = {
    "fontSize": "0.68rem",
    "fontWeight": "600",
    "letterSpacing": "1.2px",
    "textTransform": "uppercase",
    "marginBottom": "5px",
    "fontFamily": "'Source Sans 3', sans-serif",
}

TEXT_STYLE = {
    "fontSize": "0.88rem",
    "lineHeight": "1.6",
    "color": "#444444",
    "fontWeight": "300",
    "fontFamily": "'Source Sans 3', sans-serif",
}

LINE_STYLE = {
    "position": "absolute",
    "left": "50%",
    "transform": "translateX(-50%)",
    "top": "0",
    "bottom": "0",
    "width": "2px",
    "background": "linear-gradient(to bottom, transparent, #cccccc 3%, #cccccc 97%, transparent)",
    "zIndex": "1",
    "pointerEvents": "none",
}


def make_event_row(event):
    dot = html.Div(style={
        "width": "14px", "height": "14px", "borderRadius": "50%",
        "border": "2px solid #ffffff", "flexShrink": "0",
        "boxShadow": "0 0 0 3px rgba(0,0,0,0.08)",
        "background": event["color"],
    })

    node = html.Div([dot, html.Div(str(event["year"]), style=YEAR_STYLE)], style=NODE_COL_STYLE)

    card = html.Div([
        html.Div(event["label"], style={**LABEL_STYLE, "color": event["color"]}),
        html.Div(event["text"],  style=TEXT_STYLE),
    ], style=CARD_LEFT if event["side"] == "left" else CARD_RIGHT)

    empty = html.Div()
    children = [card, node, empty] if event["side"] == "left" else [empty, node, card]
    return html.Div(children, style=ROW_STYLE)


def build_timeline_layout():
    rows = [make_event_row(e) for e in events]
    return html.Div([
        html.Link(rel="stylesheet", href=FONTS_URL),
        html.Div([
            # ← ya no va html.Div(style=LINE_STYLE) acá
            html.H1("Argentina — No sabes que corno haces y nunca lo hiciste.", style=TITLE_STYLE),
            html.Div([html.Div(style=LINE_STYLE)] + rows, style=TIMELINE_STYLE),  # ← línea dentro del contenedor de rows
            dcc.Link("← Volver al inicio", href="/", style={
                "color": "#1565C0", "fontSize": "0.9rem",
                "fontFamily": "'Source Sans 3', sans-serif",
                "textDecoration": "none", "display": "inline-block", "marginTop": "60px",
            }),
        ], style=INNER),
    ], style=WRAP)


# ── Layout exportable ────────────────────────────────────────────────────────
timeline_layout = build_timeline_layout()
