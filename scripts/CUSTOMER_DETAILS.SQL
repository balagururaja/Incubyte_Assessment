/*-----------------------------------------------------------------------------------------------------------
--
--   NAME:           CUSTOMER_DETAILS.SQL
--
--   DESCRIPTION:    This script insert data FROM STG.CUSTOMER_STG to CONS.CUSTOMER
--
--   INPUT TABLES:   STG.CUSTOMER_STG
--
--   OUTPUT TABLES:  CONS.CUSTOMER
--
--   PREMODULE:      Copy data FROM STG.CUSTOMER_STG TO CONS.CUSTOMER in Redshift
--
--   POSTMODULE:     NA
--
--  ----------------------------------------------------------------------------
--  Change History
--  ----------------------------------------------------------------------------
--  ChangeDate/Version   Author                    		Description
--  ----------------------------------------------------------------------------
#   1.1	  				Balagururaja Alagarsamy			Initial Version

------------------------------------------------------------------------------------------------------------------*/
/*Insert data from stg table to cons table*/
INSERT INTO CONS.TABLE_#COUNTRY_NAME#
(
	CUSTOMER_NAME
	,CUSTOMER_ID
	,CUSTOMER_OPEN_DATE
	,LAST_CONSULTED_DATE
	,VACCINATION_TYPE
	,DOCTOER_CONSULTED
	,STATE,
	,COUNTRY
	,POSTAL_CODE
	,DATE_OF_BIRTH
	,ACTIVE_CUSTOMER
)
SELECT 
	CUSTOMER_NAME
	,CUSTOMER_ID
	,CUSTOMER_OPEN_DATE
	,LAST_CONSULTED_DATE
	,VACCINATION_TYPE
	,DOCTOER_CONSULTED
	,STATE,
	,COUNTRY
	,POSTAL_CODE
	,DATE_OF_BIRTH
	,ACTIVE_CUSTOMER
FROM STG.CUSTOMER_STG
WHERE COUNTRY IN ('#COUNTRY_CODE#');	