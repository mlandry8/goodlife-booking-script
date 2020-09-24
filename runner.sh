python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python booking_script.py  --dry --headless --time "4:30PM - 5:30PM" --days 7
deactivate
