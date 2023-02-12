docker run --name records-bd -e POSTGRES_PASSWORD=swordfish -p 5432:5432 -d postgres

docker exec records-bd psql -U postgres -f "C:\Users\am_va\Desktop\Documents\PyProjects\RecordVisualisation\postgres_tables.sql"

docker cp "C:\Users\am_va\Desktop\Documents\PyProjects\RecordVisualisation\postgres_tables.sql" records-bd:/mnt/postgres_tables.sql

 psql -U postgres -f mnt/postgres_tables.sql