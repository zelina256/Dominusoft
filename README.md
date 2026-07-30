# Dominusoft Web - Setup and Run

Follow these steps to open and run the project locally.

## 1. Open the project folder

## 2. Create a virtual environment

```powershell
python -m venv venv
```

## 3. Activate the virtual environment

```powershell
venv\Scripts\activate
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## 5. Apply database migrations

```powershell
python manage.py migrate
```

## 6. Run the development server

```powershell
python manage.py runserver
```

## 7. Open in browser

Go to:

```text
http://127.0.0.1:8000/
```
