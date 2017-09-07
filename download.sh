#!/usr/bin/env bash
M_USER="felipe.kpereira@live.com"
M_PASS="rubyheron82"
M_FORMAT="AQCSV"
F_STATE="48"
F_COUNTIES=(005 025 027 029 037 039 041 043 049 055 057 061 065 067 071 085 091 109 113 121 135 141 139 149 157 167 171 179 181 183 189 199 201 203 209 215 221 227 231 233 243 245 251 253 257 273 291 303 315 321 323 309 311 329 331 339 341 343 347 349 355 361 367 373 375 381 395 397 409 415 423 439 441 449 451 453 457 465 469 471 473 479 485 491 497)
F_YEAR=(2002 2003 2004)
F_PARAM=(44201 42401 14129 42602 44201 81102 85129 88101 61101 61103 61102 61104 61105 61109 61112 68105 62101 62103 62108 62201 63301 63302 63303 63304 64101 68108 65101)

for county in "${F_COUNTIES[@]}"
do
    for year in "${F_YEAR[@]}"
    do
        mkdir -p ${F_STATE}/${county}/${year}
        for param in "${F_PARAM[@]}"
        do
            touch ${F_STATE}/${county}/${year}/${param}.csv
            wget -O ${F_STATE}/${county}/${year}/${param}.csv "https://aqs.epa.gov/api/rawData?user="${M_USER}"&pw="${M_PASS}"&format="${M_FORMAT}"&param="${param}"&bdate="${year}"0101&edate="${year}"1231&state="${F_STATE}"&county="${county}""
            sleep 5
        done
    done
done