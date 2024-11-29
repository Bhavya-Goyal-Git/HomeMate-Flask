echo "================================================"
echo "Welcome to backend Run for HomeMate...."
echo "================================================"

BASE_DIR=$(pwd)

if [[ ! -d "$BASE_DIR/backend/env" ]]; then
    echo "Backend virtual environment absent, run local_setup.sh first!"
    exit 1
fi

echo "Activating virtual environment......"
source "$BASE_DIR/backend/env/bin/activate"
echo "Virtual environment activated..."

if [[ ! -d "$BASE_DIR/backend/instance" ]]; then
    echo "Database for backend absent, creating one now...."
    python3 "$BASE_DIR/backend/dbmaker.py"
    if [[ $? -ne 0 ]]; then
        echo "Problem while creating database, kindly check.."
        exit 1
    else
        echo "Database creation done successfully..."
    fi
else
    echo "Database already exists...."
fi

echo "Starting backend server now...."
python3 "$BASE_DIR/backend/run.py"
#after sever stops:
deactivate