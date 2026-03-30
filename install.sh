#!/data/data/com.termux/files/usr/bin/bash

echo "Starting Installation... Please wait."

# System Libraries သွင်းခြင်း
pkg update -y
pkg install python libjpeg-turbo zlib libpng freetype clang make python-dev -y

# Python Libraries သွင်းခြင်း
pip install django reportlab pillow

# Database Setup
python manage.py migrate
python manage.py collectstatic --noinput

echo "----------------------------------------"
echo "Installation Complete!"
echo "To start the app, type: python manage.py runserver"
echo "Then open Chrome and go to: http://127.0.0.1:8000"
echo "----------------------------------------"