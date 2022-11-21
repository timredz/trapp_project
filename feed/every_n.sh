#!/bin/bash
source /home/timredz/trapp_project/venv/bin/activate

python /home/timredz/trapp_project/feed/candles.py
python /home/timredz/trapp_project/feed/orderbook.py
python /home/timredz/trapp_project/feed/matching.py
