

sql_alive_create = "CREATE TABLE IF NOT EXISTS alive (date text, id integer, mainsys integer, mainradar integer, subsys integer, subradar integer)"
sql_alive_insert = "INSERT INTO alive(date, id, mainsys, mainradar, subsys, subradar) VALUES(?, ?, ?, ?, ?, ?)"
sql_alive_fetch = "SELECT * FROM alive"

sql_bd_info_create = "CREATE TABLE IF NOT EXISTS bd_info (date text, id integer, ip_0 integer, ip_1 integer, ip_ integer, susbradar integer)"
sql_bd_info_insert = "INSERT INTO bd_info (date, id, mainsys, mainradar, subsys, subradar) VALUES(?, ?, ?, ?, ?, ?)"
sql_bd_info_fetch = "SELECT * FROM alive"

sql_acq_data_create = "CREATE TABLE IF NOT EXISTS acq_data (date text, id integer, presence_0 integer, motion_0 integer, distance_0 integer, heart_0 integer, breath_0 integer, presence_1 integer, motion_1 integer, distance_1 integer, heart_1 integer, breath_1 integer, presence_2 integer, motion_2 integer, distance_2 integer, heart_2 integer, breath_2 integer, existence integer, obj_x integer, obj_y integer, obj_size integer)"
sql_acq_data_insert = "INSERT INTO acq_data (date, id, presence_0, motion_0, distance_0, heart_0, breath_0, presence_1, motion_1, distance_1, heart_1, breath_1, presence_2, motion_2, distance_2, heart_2, breath_2, existence, obj_x, obj_y, obj_size) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
sql_acq_data_fetch = "SELECT * FROM acq_data"
