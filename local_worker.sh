echo "================================================"
echo "Welcome to Celery workers Run for backend Jobs of HomeMate....."
echo "This will start a redis server as well as celery workers!"
echo "================================================"

BASE_DIR=$(pwd)

if [[ ! -d "$BASE_DIR/backend/env" ]]; then
    echo "Backend virtual environment absent, run local_setup.sh first!"
    exit 1
fi

echo "Activating virtual environment......"
source "$BASE_DIR/backend/env/bin/activate"
echo "Virtual environment activated..."

echo "Opening a redis-server now........"
sudo service redis-server start
if [[ $(redis-cli ping) != "PONG" ]]; then
    echo "Problem starting redis server... check issue manually.........."
    exit 1
fi

echo "Starting celery workers now..........."
cd "$BASE_DIR/backend"
celery -A run.celery worker --loglevel=info
echo "Stopping Redis server......"
sudo service redis-server stop
deactivate