import yaml
from sqlalchemy import create_engine

def configure_engine():
	with open('.config.yml', 'r') as f:
	    config = yaml.load(f)

	USERNAME = config['username']
	PASSWORD = config['password']

	# URI of our database.
	DATABASEURI = 'postgresql://{user}:{password}@w4111a.eastus.cloudapp.azure.com/proj1part2'.format(user=USERNAME, password=PASSWORD)

	# create a database engine connected to the URI above.
	return create_engine(DATABASEURI, convert_unicode=True)
