@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
echo Setup complete. Press any key to exit.
pause