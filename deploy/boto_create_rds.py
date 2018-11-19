"""
Creates an RDS instance, waits for the callback and returns the RDS
instance address.
"""
import boto3
import json
import os
with open('deploy/rds-instance.json') as fh:
    rds_options = json.load(fh)
    fh.close()
master_password = os.environ.get('SQL_PASSWORD')
if master_password:
    rds_options['MasterUserPassword'] = os.getenv('SQL_PASSWORD')
else:
    raise Exception('SQL_PASSWORD environment variable not set, aborting')
    os.sys.exit()
client = boto3.client('rds')
waiter = client.get_waiter('db_instance_available')
instance = client.create_db_instance(**rds_options)
waiter.wait()
instances = client.describe_db_instances()
address = [
    i for i in instances['DBInstances'] if i[
        'DBInstanceIdentifier'] == rds_options[
            'DBInstanceIdentifier']][0][
                'Endpoint']['Address']
os.sys.stdout.write(address)
