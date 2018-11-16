# remember to configure your credentials in ~/.aws/credentials, sample structure:
# [default]
# aws_access_key_id=YOUR_ACCESS_KEY_ID
# aws_secret_access_key=YOUR_SECRET_KEY
docker-machine create \
    --driver amazonec2 \
    --amazonec2-open-port 80 \
    --amazonec2-region us-east-2 \
    britecore-app
eval $(docker-machine env britecore-app)
docker-compose up --build -d
