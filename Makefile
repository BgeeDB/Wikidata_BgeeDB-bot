include properties
SHELL = /bin/bash

.PHONY: all clean

main: download_wikidata_files sql_execute

###### DOWNLOAD  files ##############
download_wikidata_files: file_wikidata_uberon 
	@echo "Downloaded files."
	@touch $@

file_wikidata_uberon: 
	curl "${URL_WD_UBERON_IDS}" -o ./wikidata_uberon_ids.csv
	@touch $@

sql_execute:   
	@mysql --syslog --verbose -u ${USER_MYSQL} -p${PASSWD_MYSQL} ${DB_NAME} < ${SQL_LOAD_WD_UBERON_IDS}  1>$@.tmp 2>$@.err
	@mysql -u ${USER_MYSQL} -p${PASSWD_MYSQL} ${DB_NAME} < ${SQL_GET_EXPRESSION_CALLS} > ${EXPRESSION_CALLS_FILE} 2>>$@.err
	@mysql -u ${USER_MYSQL} -p${PASSWD_MYSQL} ${DB_NAME} -e "DROP TABLE IF EXISTS temp_wikidata_uberon_ids;" 1>>$@.tmp 2>>$@.err
	@rm -f ./wikidata_uberon_ids.csv 1>>$@.tmp 2>>$@.err
	@mv $@.tmp $@
	@echo "Ended file generation to Bgee Wikidata bot."

