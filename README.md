# Coupon Manager

This project is a Django REST API application for managing and searching coupon codes. It includes admin features for managing coupons and user features for searching and availing coupons.

## Tech Stack

- Django
- Django REST Framework

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

## Setup Instructions

### Steps

```bash
git clone https://github.com/Hariom-work/Coupon-management.git

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser


###  Run the development server
python manage.py runserver
