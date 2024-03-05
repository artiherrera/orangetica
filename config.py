# Configuración de la conexión a la base de datos
host = "mc.cluster-capzd6ri1feb.us-west-1.rds.amazonaws.com"
port = "5432"
user = "luis"
password = "T#m$2G7v"
dbname = "prod-idmcn"  # Reemplaza esto con el nombre de tu base de datos


DATABASE_CONNECTION_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
