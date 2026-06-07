clear all


* IED
import delimited "C:\Users\usuario\Downloads\flujos-de-inversion-extranjera-directa-por-sector-bcra.csv", clear

keep indice_tiempo total agricultura_ganaderia_caza_silvi ensenianza construccion industria_manufacturera explotacion_minas_canteras otras_sociedades_financieras suministr_agua_cloacs_resid_recu suministro_electricidad_gas_vapo salud_humana_servicios_sociales

export excel "C:\Users\usuario\Downloads\ie", replace firstrow(variables)


* TOT - trimestral
import delimited "C:\Users\usuario\Downloads\indice-terminos-intercambio-trimestral-base-2004.csv", clear
keep indice_tiempo indice_terminos_intercambio

export excel "C:\Users\usuario\Downloads\tot", replace firstrow(variables)

*Balanza de pagos.
import delimited "C:\Users\usuario\Downloads\balance-pagos-datos-historicos.csv", clear

keep indice_tiempo cuenta_corriente_mercancias_expo cuenta_corriente_mercancias_impo cuenta_corriente_mercancias_sald cuenta_capital_total variacion_reservas

export excel "C:\Users\usuario\Downloads\bp", replace firstrow(variables)
