sat-db-drop:
	export INFLUX_URI='http://192.168.59.103:8086/query?pretty=true';
	curl --get ${INFLUX_URI} --user admin:admin --data-urlencode 'q=DROP DATABASE "edu_hm_lst_sattracker"'

sat-db-select:
	export INFLUX_URI='http://192.168.59.103:8086/query?pretty=true';
	curl --get ${INFLUX_URI} --user admin:Armoojwi --data-urlencode 'db=edu_hm_lst_sattracker' --data-urlencode 'q=select * from "01_position";' | jq '.'
