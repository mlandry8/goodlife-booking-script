python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python booking_script.py --dry --headless --time "6:00PM - 7:00PM" --days 7
