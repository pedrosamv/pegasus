
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