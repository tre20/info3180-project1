"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import Myprofile
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app import oid, lm, created_on


class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     


@app.before_request
def before_request():
    g.user = current_user
    
###
# Routing for your application.
###
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    print app.config['OPENID_PROVIDERS']
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    import os
    from flask import Flask, request, redirect, url_for
    from werkzeug import secure_filename
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        image = request.files['image']
        biography = request.form['biography']
        age = request.form['age']
        
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        created_on = time.strftime('%m %d %Y')
        
        # write the information to the database
        newprofile = Myprofile(first_name=first_name,last_name=last_name,gender=gender, image=filename, biography=biography, created_on=created_on)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {}, who is a {} was added to the database with image: {}".format(request.form['first_name'],request.form['last_name'],request.form['gender'], filename)

    form = ProfileForm()
    return render_template('profile_add.html',form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    import json
    profiles = Myprofile.query.all()
    if request.method == "GET":
        profList = str(profiles)
        
        return jsonify({"users":profList})
            #return jsonify({"id":[i].id, "gender":[i].gender, "image":[i].image)
    return render_template('profile_list.html',profiles=profiles)

@app.route('/profile/<int:id>',methods=["POST","GET"])
def profile_view(id):
    profile = Myprofile.query.get(id)
    if request.method == "GET":
        return jsonify({"data":"no instructions for GET"})
    if request.method == "POST" and 'Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json':
        return jsonify({"id":profile.id, "gender":profile.gender, "image":profile.image, "age": profile.age, "profile_created_on":created_on })
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")