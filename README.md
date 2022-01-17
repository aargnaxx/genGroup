# genGroup
FER diplomski projekt: Aplikacija za pronalaženje različitih varijanti gena grupiranjem

## Usage
Run `pip install -r requirements.txt` to install all of the packages needed to run backend part of the app. 

Move to `frontend` directory and run `npm install` in order to download the frontend dependencies.

Before running the application run the migrations by `python manage.py migrate`

If you want to spin up a local webserver for testing run:
- `python manage.py runserver 8001`
- in another shell go to `frontend` directory and run `npm run serve`
- point your browser to `http://localhost:8080`

