from flaskext.mysql import MySQL
from app import app

db = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'moviedb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db.init_app(app)
