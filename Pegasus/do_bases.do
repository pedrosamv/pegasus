clear all

import delimited "C:\Users\usuario\Dropbox\Pegasus\bases_originales\distribucion-personal-ingreso-por-deciles-trismestrales.csv"
gen porcentaje=.
forvalues i = 1/10 {
replace porcentaje= decil_`i'_ipcf/total_ipcf


}