# genGroup
FER diplomski projekt: Aplikacija za pronalaženje različitih varijanti gena grupiranjem

## Usage
Run `pip install -r requirements.txt` to install all of the packages needed to run backend part of the app. 

Move to `frontend` directory and run `npm install` in order to download the frontend dependencies.
After that run `npm run build` to create static files.

Before running the application run the migrations by `python manage.py migrate` and `python manage.py collectstatic` to collect static files 

If you want to spin up a local webserver for testing run:
- `python manage.py runserver 800`
- point your browser to `http://localhost:8000`

