if [ ! -d "venv" ]; then
    python3 -m venv venv
    pip install -r requirements.txt
else
    pip install -r requirements.txt
    echo "Virtual environment already exists"    
fi    
source venv/bin/activate
#python -B -m uvicorn main:app --reload
