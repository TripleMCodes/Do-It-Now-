# Do It App

A small Flask-based to-do web application that supports user signup/login, task creation, toggling task status, deletion, and an admin dashboard for viewing users, tasks, and user feedback.

## Features
- User signup and login (passwords hashed with Bcrypt)
- Create, delete and mark tasks as done/undone
- Contact/feedback form (stored in the database)
- Admin view showing users, tasks and feedback
- SQLite database (configured by default)

## Quick start (Windows, PowerShell)

1. Clone the repository (or copy the project folder).
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. (Optional) Set environment variables for Flask CLI (PowerShell):

```powershell
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
```

5. Initialize / apply database migrations

If you don't have the `migrations/` folder or want to recreate migrations:

```powershell
flask db init
flask db migrate -m "initial"
flask db upgrade
```

If the repo already contains `migrations/`, simply run:

```powershell
flask db upgrade
```

6. Run the app:

```powershell
# Option A - using Flask CLI (recommended when using migrations)
flask run

# Option B - run directly
python run.py
```

Then open http://127.0.0.1:5000/ in your browser.

## Creating an admin user

There is a simple admin table (`AdminDb`) used by the app. You can create an admin account from the Flask shell:

```powershell
$env:FLASK_APP = "run.py"
flask shell

# inside the shell
from app import db, create_app
app = create_app()
from models import AdminDb
with app.app_context():
    admin = AdminDb(name='admin')
    admin.set_password('your-secure-password')
    db.session.add(admin)
    db.session.commit()
    print('Admin created')
```

Replace `'your-secure-password'` with a strong password. The routes expect an admin username of `admin`.

## Configuration notes
- The application currently uses SQLite by default via `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'` in `app.py`.
- The secret key is set directly in `app.py` as `app.secret_key = 'some key'`. For production, set a secure secret via environment variables and update the config.

## Tests / Validation
This project does not include automated tests. You can verify basic behavior manually:
- Signup a new user and create tasks on the index page
- Test login/logout
- Use the contact form and check the DB table `usermassages`

## Troubleshooting
- If migrations fail, remove the `migrations/` folder (if safe) and re-run `flask db init` / `migrate` / `upgrade`.
- If `flask` CLI isn't found, ensure your virtualenv is activated and `flask` was installed from `requirements.txt`.

## Contributing
Small fixes and documentation improvements welcome. Open an issue or pull request with proposed changes.

## License
This project is licensed under the MIT License — see the `LICENSE` file for details.