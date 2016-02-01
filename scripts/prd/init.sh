#!/bin/bash
if [[ ! -z $1 ]] ; then
    RACEDATE=$1
fi

if [[ -z $RACEDATE ]] ; then
    echo 'Provide a race date, such as 2016-02-01'
    exit 1
fi

if [[ -z "$AP_API_KEY" ]] ; then
    echo "Missing environmental variable AP_API_KEY. Try 'export AP_API_KEY=MY_API_KEY_GOES_HERE'."
    exit 1
fi

date "+STARTED: %H:%M:%S"
echo "------------------------------"

echo "Initialize races"
cat /home/ubuntu/elex-loader/fields/races.txt | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE
python /home/ubuntu/elex-ftp-loader/init.py --races | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE -c "COPY races FROM stdin DELIMITER ',' CSV HEADER;"

echo "Initialize reporting units"
cat /home/ubuntu/elex-loader/fields/reporting_units.txt | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE
python /home/ubuntu/elex-ftp-loader/init.py --reporting-units | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE -c "COPY reporting_units FROM stdin DELIMITER ',' CSV HEADER;"

echo "Initialize candidates"
cat /home/ubuntu/elex-loader/fields/candidates.txt | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE
python /home/ubuntu/elex-ftp-loader/init.py --candidates | psql -h $ELEX_DB_HOST -U elex -d elex_$RACEDATE -c "COPY candidates FROM stdin DELIMITER ',' CSV HEADER;"

echo "------------------------------"
date "+ENDED: %H:%M:%S"