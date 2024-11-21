BASE_DIR=$(pwd)

if [[ ! -d "$BASE_DIR/frontend/node_modules" ]]; then
    echo "Front end libraries absent, kindly run local_setup.sh first!"
    exit 1
fi

echo "Starting frontend server...."
cd $BASE_DIR/frontend
npm run dev