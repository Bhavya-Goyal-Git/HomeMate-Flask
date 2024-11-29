echo "================================================"
echo "Welcome to Local Setup for HomeMate...."
echo "================================================"
BASE_DIR=$(pwd)

if [[ ! -d "$BASE_DIR/backend/env" ]]; then
    echo "Virtual environment absent for backend. Creating one now....."
    python3 -m venv "$BASE_DIR/backend/env"
    if [[ $? -eq 0 ]]; then
            echo "Virtual environment created SUCCESSFULLY...."
    else
        echo "Virtual environment creation FAILED. Please look into it manually...."
        exit 1
    fi
else
    echo "Virtual environment already exists..."
fi

echo "Activating virtual environment for packages installation..."
source "$BASE_DIR/backend/env/bin/activate"
pip install -r "$BASE_DIR/backend/requirements.txt"

if [[ $? -eq 0 ]]; then
    echo "Packages installed SUCCESSFULLY...."
else
    echo "Packages installation FAILED. Please check the requirements file or network issues."
    deactivate
    exit 1
fi

deactivate

echo "Moving to frontend setup now...."
if [[ ! -d "$BASE_DIR/frontend/node_modules" ]]; then
    echo "Frontend libraries absent, installing them now...."
    cd "$BASE_DIR/frontend"
    npm install
    if [[ $? -eq 0 ]]; then
        echo "Frontend packages installed SUCCESSFULLY...."
    else
        echo "Packages installation FAILED. Please check npm issues manually..."
        exit 1
    fi
fi

echo "------- Setup completed :) -------------"