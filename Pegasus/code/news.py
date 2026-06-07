# ========== News Layout ===========
# Lee noticias desde una hoja "noticias" del Excel principal (base_data.xlsx)
# Columnas: fecha | semana_inicio | rubro | titular | cuerpo | analisis | tiene_foto | pie_foto

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta
import os

# DESPUÉS
_DATA_PATH = r"C:/Users/usuario/Dropbox/Python/Pegasus/noticias_template.xlsx"

TAG_STYLES = {
    "fiscal":    {"background": "#EEEDFE", "color": "#3C3489"},
    "monetario": {"background": "#E6F1FB", "color": "#0C447C"},
    "exterior":  {"background": "#E1F5EE", "color": "#085041"},
    "social":    {"background": "#FAEEDA", "color": "#633806"},
    "mercados":  {"background": "#FAECE7", "color": "#712B13"},
}

RUBROS = ["todos", "fiscal", "monetario", "exterior", "social", "mercados"]

# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_week_start(fecha):
    """Devuelve el lunes de la semana como string YYYY-MM-DD."""
    if pd.isna(fecha):
        return None
    if isinstance(fecha, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                fecha = datetime.strptime(fecha, fmt)
                break
            except ValueError:
                continue
    if not isinstance(fecha, datetime):
        fecha = pd.Timestamp(fecha).to_pydatetime()
    lunes = fecha - timedelta(days=fecha.weekday())
    return lunes.strftime("%Y-%m-%d")


def _fmt_week_label(semana_key):
    """'2026-05-18'  →  '18–24 may 2026'"""
    MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
    lunes   = datetime.strptime(semana_key, "%Y-%m-%d")
    domingo = lunes + timedelta(days=6)
    if lunes.month == domingo.month:
        return f"{lunes.day}–{domingo.day} {MESES[lunes.month-1]} {lunes.year}"
    return (f"{lunes.day} {MESES[lunes.month-1]} – "
            f"{domingo.day} {MESES[domingo.month-1]} {domingo.year}")


def _load_noticias():
    """Carga la hoja 'noticias' del Excel y devuelve un dict semana → [noticias]."""
    try:
        df = pd.read_excel(_DATA_PATH, sheet_name="noticias")
    except Exception as e:
        return {}, f"Error al leer el Excel: {e}"

    df.columns = df.columns.str.strip().str.lower()

    # Calcular semana_inicio si está vacío
    if "semana_inicio" not in df.columns:
        df["semana_inicio"] = df["fecha"].apply(_get_week_start)
    else:
        mask = df["semana_inicio"].isna() | (df["semana_inicio"].astype(str).str.strip() == "")
        df.loc[mask, "semana_inicio"] = df.loc[mask, "fecha"].apply(_get_week_start)

    df["semana_inicio"] = df["semana_inicio"].apply(
        lambda x: _get_week_start(x) if not isinstance(x, str) or "-" not in str(x) else str(x)[:10]
    )
    df["rubro"] = df["rubro"].str.strip().str.lower().fillna("general")
    df["analisis"] = df.get("analisis", pd.Series([""] * len(df))).fillna("")
    df["tiene_foto"] = df.get("tiene_foto", pd.Series(["NO"] * len(df))).fillna("NO").str.upper()
    df["pie_foto"] = df.get("pie_foto", pd.Series([""] * len(df))).fillna("")

    noticias_dict = {}
    for _, row in df.iterrows():
        key = str(row["semana_inicio"])[:10]
        if key not in noticias_dict:
            noticias_dict[key] = []
        noticias_dict[key].append(row.to_dict())

    semanas_ordenadas = dict(sorted(noticias_dict.items(), reverse=True))
    return semanas_ordenadas, None


# ── Render helpers ────────────────────────────────────────────────────────────

def _tag_badge(rubro):
    style = TAG_STYLES.get(rubro, {"background": "#F1EFE8", "color": "#444441"})
    return html.Span(rubro, style={
        "fontSize": "10px", "fontWeight": "500",
        "padding": "2px 9px", "borderRadius": "20px",
        "textTransform": "uppercase", "letterSpacing": "0.4px",
        **style
    })


def _news_card(n, idx):
    rubro    = str(n.get("rubro", "")).strip()
    titular  = str(n.get("titular", ""))
    cuerpo   = str(n.get("cuerpo", ""))
    analisis = str(n.get("analisis", "")).strip()
    foto     = str(n.get("tiene_foto", "NO")).upper() == "SI"
    pie      = str(n.get("pie_foto", ""))
    fecha    = n.get("fecha", "")
    if hasattr(fecha, "strftime"):
        fecha = fecha.strftime("%d/%m/%Y").lower()

    children = [
        html.Div([
            _tag_badge(rubro),
            html.Span(str(fecha), style={
                "fontSize": "11px", "color": "#888780", "marginLeft": "8px"
            }),
        ], style={"marginBottom": "6px"}),

        html.Div(titular, style={
            "fontSize": "15px", "fontWeight": "500",
            "lineHeight": "1.35", "marginBottom": "8px"
        }),
    ]

    # Párrafos del cuerpo
    for p in cuerpo.split("\\n"):
        if p.strip():
            children.append(html.P(p.strip(), style={
                "fontSize": "13px", "lineHeight": "1.65",
                "color": "#5F5E5A", "marginBottom": "6px"
            }))

    # Foto placeholder (se reemplaza con html.Img cuando tengás rutas reales)
    if foto:
        children.append(html.Div([
            html.I(className="ti ti-photo", style={"fontSize": "20px"}, **{"aria-hidden": "true"}),
            html.Span(pie or "imagen", style={"fontSize": "12px", "marginLeft": "6px"}),
        ], style={
            "border": "0.5px solid #D3D1C7",
            "borderRadius": "8px",
            "padding": "20px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "color": "#888780",
            "margin": "10px 0",
        }))

    # Bloque de análisis colapsable
    if analisis:
        analisis_id = f"analisis-{idx}"
        btn_id      = f"btn-analisis-{idx}"
        children += [
            dbc.Button(
                [html.I(className="ti ti-message-circle",
                        style={"fontSize": "13px", "marginRight": "5px"},
                        **{"aria-hidden": "true"}),
                 "Ver análisis"],
                id=btn_id,
                color="link",
                size="sm",
                style={"padding": "0", "fontSize": "12px",
                       "color": "#888780", "textDecoration": "none"},
                n_clicks=0,
            ),
            dbc.Collapse(
                html.Div([
                    html.Div("Análisis editorial", style={
                        "fontSize": "10px", "fontWeight": "500",
                        "color": "#534AB7", "letterSpacing": "0.5px",
                        "textTransform": "uppercase", "marginBottom": "5px",
                    }),
                    html.Div(analisis, style={
                        "fontSize": "12px", "lineHeight": "1.65",
                        "color": "#5F5E5A", "fontStyle": "italic",
                    }),
                ], style={
                    "borderLeft": "2px solid #7F77DD",
                    "padding": "10px 14px",
                    "background": "#F5F5F5",
                    "borderRadius": "0 6px 6px 0",
                    "marginTop": "8px",
                }),
                id=analisis_id,
                is_open=False,
            ),
        ]

    return html.Div(children, style={
        "padding": "16px 0",
        "borderBottom": "0.5px solid #E0E0E0",
    })


def _build_feed(semana_key, rubro_filtro="todos"):
    noticias_dict, error = _load_noticias()
    if error:
        return [html.Div(f"⚠ {error}", style={"color": "red", "padding": "1rem"})]

    if not noticias_dict:
        return [html.Div("No hay noticias cargadas en el Excel.",
                         style={"color": "#888", "padding": "1rem"})]

    items = noticias_dict.get(semana_key, [])
    if rubro_filtro != "todos":
        items = [n for n in items if n.get("rubro", "").strip().lower() == rubro_filtro]

    if not items:
        return [html.Div("Sin noticias para esta semana / rubro.",
                         style={"color": "#888", "fontStyle": "italic", "padding": "0.5rem 0"})]

    return [_news_card(n, f"{semana_key}-{i}") for i, n in enumerate(items)]


def _build_semanas_options():
    noticias_dict, _ = _load_noticias()
    semanas = sorted(noticias_dict.keys(), reverse=True)
    return semanas


# ── Layout principal ──────────────────────────────────────────────────────────

def _make_layout():
    semanas = _build_semanas_options()
    semana_actual = semanas[0] if semanas else _get_week_start(datetime.today().strftime("%Y-%m-%d"))
    label_actual  = _fmt_week_label(semana_actual) if semana_actual else "—"

    rubro_pills = []
    for r in RUBROS:
        rubro_pills.append(
            html.Span(r if r != "todos" else "Todas", **{
                "id": f"pill-{r}",
                "n_clicks": 0,
                "data-rubro": r,
            }, style={
                "fontSize": "11px",
                "padding": "3px 12px",
                "borderRadius": "20px",
                "cursor": "pointer",
                "border": "0.5px solid #D3D1C7",
                "color": "#5F5E5A",
                "background": "#F1EFE8" if r == "todos" else "white",
                "marginRight": "6px",
            })
        )

    layout = dbc.Container(fluid=True, style={"padding": "0 24px"}, children=[

        # ── Encabezado ────────────────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("Pulso económico",
                          style={"fontSize": "22px", "fontWeight": "500"}),
                html.Span("Argentina",
                          style={"fontSize": "12px", "color": "#888780", "marginLeft": "10px"}),
            ]),
            # Navegador de semanas
            html.Div([
                html.Button("‹", id="news-btn-prev", n_clicks=0, style={
                    "background": "none", "border": "0.5px solid #D3D1C7",
                    "borderRadius": "6px", "padding": "4px 12px",
                    "cursor": "pointer", "fontSize": "16px",
                }),
                html.Span(label_actual, id="news-week-label", style={
                    "fontSize": "13px", "color": "#5F5E5A",
                    "minWidth": "160px", "textAlign": "center",
                }),
                html.Button("›", id="news-btn-next", n_clicks=0, style={
                    "background": "none", "border": "0.5px solid #D3D1C7",
                    "borderRadius": "6px", "padding": "4px 12px",
                    "cursor": "pointer", "fontSize": "16px",
                }),
            ], style={"display": "flex", "alignItems": "center", "gap": "10px"}),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "baseline",
            "borderBottom": "2px solid #2C2C2A",
            "padding": "16px 0 10px",
        }),

        # ── Barra de rubros ───────────────────────────────────────────────────
        html.Div(rubro_pills, style={
            "display": "flex", "flexWrap": "wrap", "gap": "4px",
            "padding": "10px 0",
            "borderBottom": "0.5px solid #E0E0E0",
        }),

        # ── Stores ────────────────────────────────────────────────────────────
        dcc.Store(id="news-semana-actual", data=semana_actual),
        dcc.Store(id="news-rubro-activo",  data="todos"),
        dcc.Store(id="news-semanas-lista", data=semanas),

        # ── Grid: feed + sidebar ──────────────────────────────────────────────
        dbc.Row([
            # Feed de noticias
            dbc.Col([
                html.Div(id="news-feed-container",
                         children=_build_feed(semana_actual)),
            ], md=8, style={"borderRight": "0.5px solid #E0E0E0",
                            "paddingRight": "24px", "paddingTop": "16px"}),

        ]),
    ])

    return layout


news_layout = _make_layout()