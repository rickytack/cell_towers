
//dependencies (ystem packages)

Installed sudo apt-get install libpq-dev   on the host


//  Launch server

export PYTHONPATH=$(pwd)

export PYTHONPATH=/media/solomin/Диск/Cells/cell-tower

cd web_app

uvicorn app:app --reload --host 0.0.0.0 --port 8000


// Clear

docker-compose build --no-cache web_app
docker-compose build --no-cache --pull




psql -U $POSTGRES_USER -d $POSTGRES_DB
dropdb -U $POSTGRES_USER $POSTGRES_DB

\dt

select * from alembic_version limit 10;
select * from cell_tower limit 10;
SELECT COUNT(id)
FROM cell_tower;

alembic revision --autogenerate -m "Init"
alembic upgrade head


------------------------------------
http://127.0.0.1:8000/api/v1/towers
http://localhost:8000/api/v1/towers/area?bottom_left_lat=59.8&bottom_left_lon=30.1&top_right_lat=60.2&top_right_lon=30.7&limit=100
http://localhost:8000/api/v1/towers/triangles?bottom_left_lat=59.8&bottom_left_lon=30.1&top_right_lat=60.2&top_right_lon=30.7


Standard FastAPI Validation Error Response
json

{
  "detail": [
    {
      "type": "error_type",
      "loc": ["location", "of", "error"],
      "msg": "Error message",
      "input": "problematic_value",
      "ctx": {"additional": "context"}
    }
  ]
}


-------------------------
Frond
npm create vue@latest vue-frontend
cd vue-frontend
npm install axios  # For API calls
npm install leaflet @vue-leaflet/vue-leaflet   # OSM
npm install ol vue-ol # osm layers
npm install d3-contour d3-array
npm install leaflet.heat
npm install lodash-es

nvm install --lts
nvm use --lts
npm run dev

http://localhost:5173/


------------------------------------------

















---------------------------------------------
task worker

sudo apt-get install -y \
    protobuf-compiler \
    libprotobuf-dev \
    libgrpc++-dev  # Contains all gRPC C++ libraries

sudo apt-get install libgrpc-dev protobuf-compiler-grpc
