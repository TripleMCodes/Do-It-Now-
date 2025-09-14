from flask import render_template, request, redirect, url_for, flash
from models import Tasks, Users, UserMassages, AdminDb
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import logging
logging.basicConfig(level=logging.DEBUG)



def app_routes(app, db, bcrypt):

    @app.route('/')
    @app.route('/index')
    def index():
        
        if current_user.is_authenticated:

            user = Users.query.get(current_user.get_id())
            tasks = user.tasks
            return render_template('index.html', tasks=tasks)
        else: return render_template('signup.html')
        

    @app.route('/saveTask', methods=['POST'])
    def saveTask():
        data = request.get_json()
        task  = data.get("task")
        date = datetime.now()
        uid = current_user.get_id()
        todo = Tasks(task_name=task, date=date, uid=uid)

        db.session.add(todo)
        db.session.commit()
        return ""
    
    @app.route('/delTask', methods=['DELETE'])
    def delTask():
        data = request.get_json()
        task = data.get("task")
        task = str(task)
        logging.debug(f'The task to be deleted is {task}')
        task_to_delete = Tasks.query.filter_by(task_name=task).first()
        logging.debug(f'The task: {task_to_delete}')
    
        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()
            logging.debug('task deleted')
            return '', 200 
        else:
            logging.debug(f'No task found with name: {task}')
            return '', 404
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        
        elif request.method == 'POST':
            try:
                username = request.form.get('username')
                password = request.form.get('password')
                logging.debug(f'The user name is {username}')

                h_password = bcrypt.generate_password_hash(password)

                user = Users(username=username, password=h_password)

                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            except Exception as e:
                flash("User name already exists, Please choose another")
                return redirect(url_for('signup'))
        
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if username == 'admin':
                user = AdminDb.query.filter(AdminDb.name == username).first()
                if user.check_password(password):

                    total_users = Users.query.count()
                    users = Users.query.all()
                    tasks = Tasks.query.all()
                    tasks_done = Tasks.query.filter(Tasks.status =="done").all()
                    tasks_undone = Tasks.query.filter(Tasks.status =="undone").all()
                    feedbacks = db.session.query(UserMassages.name, UserMassages.email, UserMassages.message).all()

                    return render_template('admin.html', total_users=total_users, users=users, tasks=tasks, tasks_done=tasks_done, tasks_undone=tasks_undone , feedbacks=feedbacks)
                else:
                    return redirect(url_for('signup'))
            elif Users.query.filter(Users.username == username).first():
                user = Users.query.filter(Users.username == username).first()
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash(f'Incorrect password')
                    return redirect(url_for('login'))
            else:
                flash(f'{username} is not a valid user name')
                return redirect(url_for('login'))
    
    @app.route('/taskdone', methods=['POST'])
    def taskDone():
        data = request.get_json()
        task  = data.get("task")
        task = Tasks.query.filter_by(task_name=task, uid=current_user.get_id()).first()

        if task.status == "undone":
            task.status = "done"
        else:
            task.status = "undone"

        db.session.commit()
        return ''

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/about')
    def about():
        return render_template("about.html")
    
    @app.route('/contact', methods=["POST", "GET"])
    def contact():
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            feedback = UserMassages(name=name, email=email, message=message)
            db.session.add(feedback)
            db.session.commit()

            return render_template('contact.html')
        return render_template('contact.html')
    
    
    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/admin')
    @login_required
    def admin_page():
            logging.debug(current_user)
            if str(current_user) == 'administrator':
                admin = str(current_user)
                user = Users.query.filter(Users.username == admin).first()
                
                return render_template('admin.html')
            return "<h1>Page not found</h2>"
    
    #Don't uncomment (if you don't know why this is here)
    # @app.route('/create_admin')
    # def create_admin():
    #     if AdminDb.query.first():
    #         return "<h1>Admin already created</h2>"
    #     password  = generate_password_hash("Nk0s1@2oo|")
    #     admin = AdminDb(name='admin', password_hash=password)
    #     db.session.add(admin)
    #     db.session.commit()