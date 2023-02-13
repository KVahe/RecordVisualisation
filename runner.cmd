cd "C:\Users\am_va\Desktop\Documents\PyProjects\RecordVisualisation"

docker run --name records-db -e POSTGRES_PASSWORD=swordfish -p 5432:5432 -d postgres

docker run -dt --name python-39 python

sleep 10

docker cp "postgres_tables.sql" records-db:/mnt/postgres_tables.sql

docker exec -it records-db bin/bash

psql -U postgres -f mnt/postgres_tables.sql

exit

docker cp "requirements_pip.txt" python-39:/mnt/requirements_pip.txt

docker exec -it python-39 bin/bash

pip install --upgrade pip

python -m venv vrt-env

sources vrt-env/bin/activate

pip install -r mnt/requirements_pip.txt

exit

# Create a network to connect the two containers
docker network create py-db-network

docker network connect py-db-network python-39

docker network connect py-db-network records-db


 