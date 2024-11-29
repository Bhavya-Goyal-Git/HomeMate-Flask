echo "==========================================================================="
echo "Welcome to Run for Celery beat, for Scheduled backend jobs, HomeMate"
echo "==========================================================================="

BASE_DIR=$(pwd)

if [[ ! -d "$BASE_DIR/backend/env" ]]; then
    echo "Backend virtual environment absent, run local_setup.sh first!"
    exit 1
fi

echo "Activating virtual environment......"
source "$BASE_DIR/backend/env/bin/activate"
echo "Virtual environment activated..."

if [[ $(redis-cli ping) != "PONG" ]]; then
    echo "Redis server inactive... check issue manually.........."
    exit 1
fi

if pgrep -x "MailHog" > /dev/null; then
    echo "MailHog is running.... "
else
    echo "MailHog is not running.... Run MailHog first in another window then run this again!"
    exit 1
fi

echo "Starting celery beat now..........."
cd "$BASE_DIR/backend"
celery -A run.celery beat --loglevel=info

deactivate