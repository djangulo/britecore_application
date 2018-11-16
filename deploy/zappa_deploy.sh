# This file does several things:
# - First, it creates a postgres rds instance using the aws cli, it has a while
#   loop as a postgres healthcheck (which currently takes too long)
# - Then uploads the environment paramenters (some of them returned by the cli)
#
# prior to calling this script, env variables SQL_PASSWORD and SECRET_KEY need to be set
# a quick and easy way to do so is using /dev/urandom: 
# export SQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
# export SECRET_KEY=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
pipenv install --dev --skip-lock

sed "s@CHANGEME@$SQL_PASSWORD@g" deploy/rds-instance-template > deploy/rds-instance.json
aws rds create-db-instance --cli-input-json file://deploy/rds-instance.json
SQL_HOST=$(aws rds describe-db-instances \
    | grep -i Address \
    | sed "s@\: @\n@g" \
    | grep aws \
    | sed "s@,@@g")
while [ $SQL_HOST -n ]; do
    SQL_HOST=$(aws rds describe-db-instances \
    | grep -i Address \
    | sed "s@\: @\n@g" \
    | grep aws \
    | sed "s@,@@g")
    echo "waiting for RDS host address to be ready"
    sleep 1

done
sed "s@CHANGESECRETKEY@$SECRET_KEY@g" deploy/zappa_settings_template \
    | sed "s@DBPASS@$SQL_PASSWORD@g" \
    | sed s@"DBHOST@$SQL_HOST@g" \
    > zappa_settings.json

pipenv run zappa deploy prod
db_status=$(aws rds describe-db-instances \
    | grep -i DBInstanceStatus \
    | sed "s@: @\n@g" \
    | grep -i available \
    | sed "s@,@@g")
while [ $db_status != "available" ]; do
    db_status=$(aws rds describe-db-instances \
    | grep -i DBInstanceStatus \
    | sed "s@: @\n@g" \
    | grep -i available \
    | sed "s@,@@g")
    echo "waiting for RDS database to be available"
    sleep 0.1
done
pipenv run zappa manage prod migrate
pipenv run zappa manage prod create_initial_risks
