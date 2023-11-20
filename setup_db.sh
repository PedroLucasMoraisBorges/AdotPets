#!/bin/bash

sql_slave_user='CREATE USER "mydb_slave_user"@"%" IDENTIFIED BY "mydb_slave_pwd"; GRANT REPLICATION SLAVE ON *.* TO "mydb_slave_user"@"%"; FLUSH PRIVILEGES;'
docker exec database_master sh -c "mysql -u root -pS3cret -e '$sql_slave_user'"

MS_STATUS=`docker exec database_master sh -c 'mysql -u root -pS3cret -e "SHOW MASTER STATUS"'`
CURRENT_LOG=`echo $MS_STATUS | awk '{print $6}'`
CURRENT_POS=`echo $MS_STATUS | awk '{print $7}'`

sql_set_master="CHANGE MASTER TO MASTER_HOST='database_master',MASTER_USER='mydb_slave_user',MASTER_PASSWORD='mydb_slave_pwd',MASTER_LOG_FILE='$CURRENT_LOG',MASTER_LOG_POS=$CURRENT_POS; START SLAVE;"
start_slave_cmd='mysql -u root -pS3cret -e "'
start_slave_cmd+="$sql_set_master"
start_slave_cmd+='"'
docker exec database_slave sh -c "$start_slave_cmd"

docker exec database_slave sh -c "mysql -u root -pS3cret -e 'SHOW SLAVE STATUS \G'"
