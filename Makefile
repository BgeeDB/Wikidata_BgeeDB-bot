include properties
SHELL = /bin/bash
export CONFIG_TEMPLATE

.PHONY: all clean

##Run install_pipenv, if pipenv is not installed.
run_bot: config_file
	@$(PIPENV) install 1>$@.tmp 2>$@.err
	@$(PIPENV) run $(PYTHON) $(APP_FILE) 1>> $@.tmp 2>> $@.err
	@mv $@.tmp $@

config_file:
	@echo "$$CONFIG_TEMPLATE" > $(APP_DIR)/config.py
	@touch $@

get_input_expression_data: download_wikidata_files sql_execute

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

install_pipenv:
	@curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | $(PYTHON) 1> $@.tmp 2> $@.err
	@mv $@.tmp $@

