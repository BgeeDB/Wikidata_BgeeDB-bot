#USE easybgee_v14_2; 
DROP TABLE IF EXISTS temp_wikidata_uberon_ids;
CREATE TABLE IF NOT EXISTS temp_wikidata_uberon_ids(
   uberon_anatomical_id      VARCHAR(255) CHARACTER SET utf8  NOT NULL COMMENT 'Uberon ids from Wikidata'
  ,PRIMARY KEY(uberon_anatomical_id)
);

#It loads the CSV data file from a local path.
LOAD DATA LOCAL INFILE "./wikidata_uberon_ids.csv" INTO TABLE temp_wikidata_uberon_ids FIELDS ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS 
 (@uberon_anatomical_id) SET uberon_anatomical_id  =  TRIM(  @uberon_anatomical_id ) ;