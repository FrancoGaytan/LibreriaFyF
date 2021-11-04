from main import app



class ConfigDatabase(object):
   app.config['MYSQL_HOST']='localhost'
   app.config['MYSQL_USER']='root'
   app.config['MYSQL_PASSWORD']=''
   app.config['MYSQL_DB']='libreria_f&f'