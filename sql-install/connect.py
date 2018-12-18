import mysql.connector
import os

ext_passwd = os.getenv('MYSQL_ROOT_PASSWORD').strip('\n')
ext_host = os.getenv('MYSQL_HOST').strip('\n')

os.system("gunzip /root/MASTER.txt.gz")
os.system("gunzip /root/ACFTREF.txt.gz")

config_db = {
  'host': "mysql",
  'user': "root",
  'passwd': "k8spassword" 
}

config_db['passwd'] = ext_passwd
config_db['host'] = ext_host

print ("external host is %s" % ext_host)

mydb = mysql.connector.connect(**config_db) 
mycursor = mydb.cursor()


DB_NAME= 'planespotter'

TABLES = {}

TABLES['plane'] = (
    "CREATE TABLE `MASTER` ("
	"`N-NUMBER` VARCHAR(255) NOT NULL,"
	"SERIAL_NUMBER VARCHAR(255) NULL,"
	"MFR_MDL_CODE VARCHAR(255) NULL,"
	"ENG_MFR_MDL VARCHAR(255) NULL,"
	"YEAR_MFR VARCHAR(255) NULL,"
	"TYPE_REGISTRANT VARCHAR(255) NULL,"
	"NAME VARCHAR(255) NULL,"
	"STREET VARCHAR(255) NULL,"
	"STREET2 VARCHAR(255) NULL,"
	"CITY VARCHAR(255) NULL,"
	"STATE VARCHAR(255) NULL,"
	"ZIP_CODE VARCHAR(255) NULL,"
	"REGION VARCHAR(255) NULL,"
	"COUNTY VARCHAR(255) NULL,"
	"COUNTRY VARCHAR(255)NULL,"
	"LAST_ACTION_DATE VARCHAR(255) NULL,"
	"CERT_ISSUE_DATE VARCHAR(255) NULL,"
	"CERTIFICATION VARCHAR(255) NULL,"
	"TYPE_AIRCRAFT VARCHAR(255) NULL,"
	"TYPE_ENGINE VARCHAR(255) NULL,"
	"STATUS_CODE VARCHAR(255) NULL,"
	"MODE_S_CODE VARCHAR(255) NULL,"
	"FRACT_OWNER VARCHAR(255) NULL,"
	"AIR_WORTH_DATE VARCHAR(255) NULL,"
	"`OTHER_NAMES(1)` VARCHAR(255) NULL,"
	"`OTHER_NAMES(2)` VARCHAR(255) NULL,"
	"`OTHER_NAMES(3)` VARCHAR(255) NULL,"
	"`OTHER_NAMES(4)` VARCHAR(255) NULL,"
	"`OTHER_NAMES(5)` VARCHAR(255) NULL,"
	"EXPIRATION_DATE VARCHAR(255) NULL,"
	"UNIQUE_ID VARCHAR(255) NULL,"
	"KIT_MFR VARCHAR(255) NULL,"
	"KIT_MODEL VARCHAR(255) NULL,"
	"MODE_S_CODE_HEX VARCHAR(255) NULL,"
	"PRIMARY KEY (`N-NUMBER`)"
    ") ENGINE=InnoDB")

TABLES['ACFTREF'] = (
    "CREATE TABLE `ACFTREF` ("
	"CODE VARCHAR(255) NOT NULL,"
	"MFR VARCHAR(255) NULL,"
	"MODEL VARCHAR(255) NULL,"
	"`TYPE-ACFT` VARCHAR(255) NULL,"
	"`TYPE-ENG` VARCHAR(255) NULL,"
	"`AC-CAT` VARCHAR(255) NULL,"
	"`BUILD-CERT-IND` VARCHAR(255) NULL,"
	"`NO-ENG` VARCHAR(255) NULL,"
	"`NO-SEATS` VARCHAR(255) NULL,"
	"`AC-WEIGHT` VARCHAR(255) NULL,"
	"SPEED VARCHAR(255) NULL,"
	"PRIMARY KEY (CODE)"
    ") ENGINE=InnoDB")



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

def delete_database(cursor):
    try:
        cursor.execute(
            "DROP DATABASE IF EXISTS {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed deleting database: {}".format(err))
        exit(1)

def create_tables(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name))
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def load_tables(cursor, filename, dbname):
    fullname= "/" + "root" + "/" + filename
    try:
        cursor.execute(
            "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS" %(fullname, dbname))
    except mysql.connector.Error as err:
        print("Failed loading database: {}".format(err))
        exit(1)

def create_user(cursor,usern,passw):
    userx = usern
    try:
        cursor.execute(
            "CREATE USER '%s'@'%s' IDENTIFIED BY '%s'" %(userx, "%", passw))
    except mysql.connector.Error as err:
        print("failed create user: {}".format(err))

def delete_user(cursor, usern):
    userx = usern
    try:
        cursor.execute(
            "DROP USER '%s'@'%s'" %(userx, "%"))
    except mysql.connector.Error as err:
        print("failed delete user: {}".format(err))

def grant_access(cursor, usern):
    userx = usern
    try:
        cursor.execute(
            "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%s' WITH GRANT OPTION" %(DB_NAME,userx, "%"))
    except mysql.connector.Error as err:
        print("failed grant user: {}".format(err))
        exit(1)

def check_database(cursor, tablename):
     cursor.execute("""
         SELECT COUNT(*)
         FROM information_schema.tables
         WHERE table_name = '{0}'
         """.format(tablename.replace('\'', '\'\'')))
     if cursor.fetchone()[0] == 1:
         return True
   
     return False


#delete_user(mycursor, 'planespotter')
#delete_database(mycursor)
if (check_database(mycursor, 'MASTER') == False):
    create_database(mycursor)
    create_tables(mycursor)
    load_tables(mycursor, 'MASTER.txt', 'MASTER')
    load_tables(mycursor, 'ACFTREF.txt', 'ACFTREF')
    create_user(mycursor, 'planespotter', 'VMware1!')
    grant_access(mycursor,'planespotter')
    mydb.commit();

mydb.close()

