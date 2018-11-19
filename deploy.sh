# This file does several things:
# - First, it creates a postgres rds instance using the aws cli, it has a while
#   loop as a postgres healthcheck (which currently takes too long)
# - Then uploads the environment paramenters (some of them returned by the cli)
#
# prior to calling this script, env variables SQL_PASSWORD and SECRET_KEY need to be set
# a quick and easy way to do so is using /dev/urandom: 
# export SQL_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
# export SECRET_KEY=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 50; echo '')
cd backend
pipenv install --dev --skip-lock

SQL_HOST=$(pipenv run python deploy/boto_create_rds.py)
echo $SQL_HOST
# sed "s@CHANGESECRETKEY@$SECRET_KEY@g" deploy/zappa_settings_template \
#     | sed "s@DBPASS@$SQL_PASSWORD@g" \
#     | sed "s@DBHOST@$SQL_HOST@g" \
#     > backend zappa_settings.json

# pipenv run zappa deploy prod
# API_ADDRESS=$(pipenv run zappa status prod \
#     | grep API \
#     | sed "s@: @\n@g" \
#     | grep http \
#     | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
# # add the API root of the endpoint created by Zappa into the
# # vue.js app
# # NOTE it does not have a trailing slash
# echo "export const apiRoot = '$API_ADDRESS'/api/v1.0" \
#     > frontend/src/store/modules/apiData.js
# # cd to vue dir, set env, build, deploy
# cd frontend
# # NODE_ENV=production
# npm run build
# npm run deploy
# cd ..
# # migrate DB
# pipenv run zappa manage prod migrate
# # create initial samples
# pipenv run zappa manage prod create_initial_risks