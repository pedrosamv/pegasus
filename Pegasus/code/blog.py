
# Aca van a estar los dfirentes .py de cada blog.
import pdfplumber


#Esto es para decirle que cada vez que le pida leer_pdf efectivamente lo haga.
def leer_pdf(ruta):
    texto = ""

    with pdfplumber.open(ruta) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n\n"

    return texto



texto_convertibilidad = leer_pdf(
    os.path.join(ROOT_DIR, "convertibilidad.pdf")
)
FONTS_URL = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap"

WRAP = {
    "background": "#ffffff",
    "minHeight": "100vh",
    "padding": "64px 24px 100px",
    "fontFamily": "'Source Sans 3', sans-serif",
    "color": "#000000",
}

INNER = {
    "maxWidth": "780px",       # columna de lectura cómoda
    "margin": "0 auto",
}

EYEBROW_STYLE = {
    "fontSize": "0.68rem",
    "fontWeight": "600",
    "letterSpacing": "2px",
    "textTransform": "uppercase",
    "color": "#2E7D32",        # verde post-convertibilidad, igual que en timeline
    "marginBottom": "12px",
    "fontFamily": "'Source Sans 3', sans-serif",
}

TITLE_STYLE = {
    "fontFamily": "'Playfair Display', serif",
    "fontSize": "clamp(1.8rem, 4vw, 2.8rem)",
    "color": "#043D03",
    "letterSpacing": "-0.5px",
    "lineHeight": "1.2",
    "marginBottom": "8px",
}

DIVIDER_STYLE = {
    "border": "none",
    "borderTop": "1px solid #e0e0e0",
    "margin": "32px 0",
}

BODY_STYLE = {
    "fontSize": "1rem",
    "lineHeight": "1.85",
    "color": "#000000",
    "hyphens": "auto", 
    "fontWeight": "300",
    "whiteSpace": "pre-line",   # respeta saltos de línea del PDF
    "textAlign": "justify",
    "fontFamily": "'Source Sans 3', sans-serif",
}

# ── Layout ────────────────────────────────────────────────────────────────────
convertibilidad_layout = html.Div([
    html.Link(rel="stylesheet", href=FONTS_URL),
    html.Div([


        html.H1("La convertibilidad argentina", style=TITLE_STYLE),
        html.Hr(style=DIVIDER_STYLE),

        html.Div(texto_convertibilidad, style=BODY_STYLE),

        html.Hr(style=DIVIDER_STYLE),
        dcc.Link("← Volver al inicio", href="/", style={
            "color": "#1565C0",
            "fontSize": "0.9rem",
            "fontFamily": "'Source Sans 3', sans-serif",
            "textDecoration": "none",
        }),

    ], style=INNER),
], style=WRAP)

