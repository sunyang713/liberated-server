import yaml
from sqlalchemy import create_engine

def configure_engine():
    """
    Configure an instance of a database engine.
    """
    with open('.config.yml', 'r') as f:
        config = yaml.load(f)

    USERNAME = config['username']
    PASSWORD = config['password']

    # Database URI.
    DATABASEURI = 'postgresql://{user}:{password}@w4111a.eastus.cloudapp.azure.com/proj1part2'.format(user=USERNAME, password=PASSWORD)

    # Return a database engine connected to the URI above.
    return create_engine(DATABASEURI, convert_unicode=True)
