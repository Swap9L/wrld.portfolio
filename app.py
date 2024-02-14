from flask import Flask, flash,redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy

import base64

def img(pic):
    img = base64.b64encode(pic).decode("UTF-8") 
    return img


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/wrld'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://avnadmin:AVNS_c1mD4jIl_M69bwujawl@mysql-wrld-swap9l-wrld.a.aivencloud.com:24513/wrld2'
db = SQLAlchemy(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

userLogin=False

class Users(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=False)

    
class Portfolio(db.Model):
    pid=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, nullable=False)
    # uid=db.Column(db.Integer, db.foreignKey('users.user_id'), nullable=False)
    name=db.Column(db.String(100), nullable=False)
    title=db.Column(db.String(20), nullable=False)
    intro=db.Column(db.String(500), nullable=False)
    contact=db.Column(db.String(15), nullable=False)
    pic=db.Column(db.LargeBinary, nullable=False)
    url=db.Column(db.String(50), nullable=False)

class Skills(db.Model):
    skill_id=db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer, nullable=False)
    skill_name=db.Column(db.String(25), nullable=False)

class Education(db.Model):
    education_id=db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer ,nullable=False)
    degree=db.Column(db.String(50),nullable=False )
    institution=db.Column(db.String(25), nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    des=db.Column(db.String(500), nullable=False)

class Projects(db.Model):
    project_id=db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer, nullable=False)
    pname=db.Column(db.String(50), nullable=False)
    link=db.Column(db.String(100), nullable=False)
    pinfo=db.Column(db.String(500), nullable=False)
    pimg=db.Column(db.LargeBinary, nullable=False)

class Experience(db.Model):
    experience_id=db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer, nullable=False)
    job_title=db.Column(db.String(50), nullable=False)
    company_name=db.Column(db.String(50), nullable=False)
    year=db.Column(db.String(50), nullable=False)
    description=db.Column(db.String(500), nullable=False)

class Msg(db.Model):
    msgid=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    phone=db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(69), nullable=False)
    content=db.Column(db.String(1000), nullable=False)
    







# sd = Projects(pid="02", pname="999WRLD", pshortinfo="HTML, CSS, JS", pinfo="This is information about project. This is information about project.",  pimg='', uid="1" )
#db.session.add(sd)
#db.session.commit()




# sd = User(uid="01", username="Luffy", email="luffy@gmai.com",password="Mugiwara")

# db.session.add(sd)
# db.session.commit()
@app.route('/', methods=['GET'])
def home():
    info=Portfolio.query.first()
    info2=Portfolio.query.filter_by(title='FaZe Banks').first()
    img2=base64.b64encode(info2.pic).decode("utf-8")
    carduser=Users.query.filter_by(user_id=info.user_id).first()
    img=base64.b64encode(info.pic).decode("utf-8")
    return render_template('home.html', info=info, info2=info2, img=img, user=carduser, img2=img2)

@app.route('/form', methods=['Get','POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        content = request.form.get('feedback')

        newone=Msg(name=name, phone=phone, email=email, content=content)

        db.session.add(newone)
        db.session.commit()

    return render_template('form.html')



@app.route('/<string:username>', methods=['GET'])
def helloWrld(username):

    user=Users.query.filter_by(username=username).first()

    info=Portfolio.query.filter_by(user_id=user.user_id)
    if not info:
        return redirect('/dashboard')

    if not user:
        return render_template('login.html', message='Invalid Cred.')
        
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    skillinfo=Skills.query.filter_by(pid=info.pid).all()[::]
    projectinfo=Projects.query.filter_by(pid=info.pid).all()
    expinfo=Experience.query.filter_by(pid=info.pid).all()
    eduinfo=Education.query.filter_by(pid=info.pid).first()
    img2 = base64.b64encode(info.pic).decode("utf-8") 

    images=[]
    for proj in projectinfo:
        img = base64.b64encode(proj.pimg).decode("utf-8")
        images.append(img)
    images=[]
    for proj in projectinfo:
        img = base64.b64encode(proj.pimg).decode("utf-8")
        images.append(img)

    


    if 'user' in session == username :   
        if not info:
            return render_template('dashboard.html', user=user, info=info)
    img2 = base64.b64encode(info.pic).decode("utf-8") 

    return render_template('index.html', user=user, info=info, img=img2, skillinfo=skillinfo, expinfo=expinfo, username=username, projectinfo=projectinfo, images=images, eduinfo=eduinfo )


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if 'user' in session:
        return redirect('dashboard')


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username ).first()
        if not user:
            
            return render_template('login.html', error='Invalid Credentials .')
        user = Users.query.filter_by(password=password).first()
        if not user:
            
            return render_template('login.html', error='Invalid Credentials .')
        
        if user.password == password and user.username == username:
            
            # login_user(user)
            
            session['user']=user.username
            userLogin=True
            return redirect('dashboard')
            
            # session['user=user.username']
            # flash('Logged in successfully!', 'success')
            # return redirect(url_for('index'))  # Redirect to home page
        else:
            flash('Invalid username or password', 'danger')
            

    return render_template('login.html', error='Enter Credentials.')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    userLogin=False 
    flash('Logged out successfully!', 'success')
    return redirect('/login')


@app.route('/register', methods=['Get','POST'] )
def register():
    if request.method == "POST":

        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        password2=request.form['password2']

        olduser=Users.query.filter_by(username=username).first()
        if olduser:
            return render_template('register.html', error='Cannot use this username.')
        
        olduser=Users.query.filter_by(password=password).first()
        if olduser:
            return render_template('register.html', error='Cannot use this Password.')


        
        if password == password2:
            newuser=Users(username=username, email=email, password=password)
            db.session.add(newuser)
            db.session.commit()
            return redirect('/login')

        flash("Password Not Matching !")

    return render_template('register.html')




@app.route('/profile', methods=['Get','POST'])
def profile():
    userName=Users.query.filter_by(username=session['user']).first()


    if request.method == "POST":
        newUsername=request.form['newUsername']
        newEmail=request.form['newEmail']
        newPassword=request.form['newPassword']
        oldPassword=request.form['password']

        # user=Users.query.filter_by(username=session['user']).first()
        

        if oldPassword == userName.password:
            userName.username=newUsername,
            userName.email=newEmail 
            userName.password=newPassword
            db.session.commit()
    

    
            
            
    return render_template('profile.html', userinfo=userName,  )

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    user=Users.query.filter_by(username=session['user']).first()
    
    
    #--Info------------------------------------------------------------
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    
        
    if not info :    
        if request.method == "POST":
            
            name=request.form['name']
            title=request.form['title']
            intro=request.form['introduction']
            contact=request.form['contact']
            pic=request.files['userPicture'].read()
            url=request.form['url']

            addinfo = Portfolio( user_id=user.user_id, name=name, title=title, intro=intro, contact=contact, pic=pic, url=url)


            db.session.add(addinfo)
            db.session.commit()
            
            degree=request.form['degree']
            clg=request.form['clg']
            passdate=request.form['passdate']
            des=request.form['eduinfo']
            info=Portfolio.query.filter_by(user_id=user.user_id).first()
            addedu=Education(pid=info.pid, degree=degree, institution=clg, date=passdate, des=des)

            db.session.add(addedu)
            db.session.commit()

        info=Portfolio.query.filter_by(user_id=user.user_id).first()
        if not info:
            return render_template('dashboard.html', user=user, info=info,  )
        
        skillinfo=Skills.query.filter_by(pid=info.pid).first()
        if not skillinfo:
            return render_template('dashboard.html', user=user, info=info , eduinfo=eduinfo )
        
        expinfo=Experience.query.filter_by(pid=info.pid).first()
        if not expinfo:
            return render_template('dashboard.html', user=user, info=info, eduinfo=eduinfo )
        
        eduinfo=Education.query.filter_by(pid=info.pid).first()
        if not eduinfo:
            return render_template('dashboard.html', user=user, info=info, eduinfo=eduinfo )


        def showimg(pic):
            img = base64.b64encode(pic).decode("utf-8") 
            return img
        # img2 = base64.b64encode(info.pic).decode("utf-8") 

    else:
        if request.method == "POST":
            newname=request.form['name']
            newtitle=request.form['title']
            newintro=request.form['introduction']
            newcontact=request.form['contact']
            newpic=request.files['userPicture'].read()
            newurl=request.form['url']


            info.name=newname
            info.title=newtitle
            info.intro=newintro
            info.contact=newcontact 
            info.pic=newpic
            info.url=newurl
            db.session.commit()

            eduinfo=Education.query.filter_by(pid=info.pid).first()
            if not eduinfo :
                degree=request.form['degree']
                clg=request.form['clg']
                passdate=request.form['passdate']
                des=request.form['eduinfo']
                
                addedu=Education(pid=info.pid, degree=degree, institution=clg, date=passdate, des=des)

                db.session.add(addedu)
                db.session.commit()
                return redirect('/dashboard') 
            else:
                newdegree=request.form['degree']
                newclg=request.form['clg']
                newpassdate=request.form['passdate']
                newdes=request.form['eduinfo']

                eduinfo.degree=newdegree
                eduinfo.institution=newclg
                eduinfo.date=newpassdate
                eduinfo.des=newdes

                db.session.commit()
    

    #------------------------------------------------------------------------
            
        

    #--Skills------------------------------------------------------------
    

    # else:
        # if request.method == "POST":
            # newskill1=request.form['skill1']
            # newskill2=request.form['skill2']
            # newskill3=request.form['skill3']
            # newskill4=request.form['skill4']
            # newskill5=request.form['skill5']
            # newskill6=request.form['skill6']
            # newskill7=request.form['skill7']
            # newskill8=request.form['skill8']

            # skillinfo.skill_name=newskill

            # for i in range(1,9):
            #     skill=skill+i
                
            #     db.session.commit()

    skillinfo=Skills.query.filter_by(pid=info.pid).all()
    

    #------------------------------------------------------------------------
            
            
    #--Project-----------------------------------------------------
    # Proj=Projects.query.filter_by(pid=Portfolio.pid).all()
    # if not Proj:    
    #     if request.method == "POST":
            
    #         name=request.form['name']
    #         title=request.form['title']
    #         intro=request.form['introduction']
    #         contact=request.form['contact']
    #         pic=request.files['userPicture'].read()
    #         url=request.form['url']

    #         addinfo = Portfolio( user_id=user.user_id, name=name, title=title, intro=intro, contact=contact, pic=pic, url=url)

    #         db.session.add(addinfo)
    #         db.session.commit()

    #     info=Portfolio.query.filter_by(user_id=user.user_id).first()
    #     if not info:
    #         return render_template('dashboard.html', user=user, info=info)
    #     img2 = base64.b64encode(info.pic).decode("utf-8") 

    # else:
    #     if request.method == "POST":
    #         newname=request.form['name']
    #         newtitle=request.form['title']
    #         newintro=request.form['introduction']
    #         newcontact=request.form['contact']
    #         newpic=request.files['userPicture'].read()
    #         newurl=request.form['url']

    #         info.name=newname
    #         info.title=newtitle,
    #         info.intro=newintro
    #         info.contact=newcontact 
    #         info.pic=newpic
    #         info.url=newurl

    #         db.session.commit()

    #     info=Portfolio.query.filter_by(user_id=user.user_id).first()
    #     if not info:
    #         return render_template('dashboard.html', user=user, info=info)
    #     img2 = base64.b64encode(info.pic).decode("utf-8") 
        
    #------------------------------------------------------------------------

    #--Experience----------------------------------------------------



    #--Edu----------------------------------------------------------
    
            
           
        
        

        
    #--------------------------------------------------------------
    projectinfo=Projects.query.filter_by(pid=info.pid).all()
    expinfo=Experience.query.filter_by(pid=info.pid).all()
    eduinfo=Education.query.filter_by(pid=info.pid).first()
    img2 = base64.b64encode(info.pic).decode("utf-8") 

    images=[]
    for proj in projectinfo:
        img = base64.b64encode(proj.pimg).decode("utf-8")
        images.append(img)

    return render_template('dashboard.html', user=user, info=info, img=img2, skillinfo=skillinfo , skills=Skills, projectinfo=projectinfo,expinfo=expinfo, eduinfo=eduinfo, images=images )


@app.route('/skillsinfo', methods=['GET','POST'])
def skillsinfo():
    #--Skills------------------------------------------------------------
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    skillinfo=Skills.query.filter_by(pid=info.pid).first()

    
    if request.method == "POST":
            
        skill1=request.form['skill1']
            
        skillcheck=Skills.query.filter_by(skill_name=skill1)
        if not skillcheck:
            pass
        
        addskill=Skills(skill_name=skill1, pid=info.pid)
        db.session.add(addskill)
            
        db.session.commit()


    skillinfo=Skills.query.filter_by(pid=info.pid).all()

    def rmskill(skill_name):
        Skills.query.filter_by(skill_name=skillinfo.skill_name).delete()
    #------------------------------------------------------------------------
    
    return redirect('/dashboard#skill')




@app.route('/dashboard/clearskills', methods=['GET','POST'])
def clearskills():
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    skillinfo=Skills.query.filter_by(pid=info.pid).all()
    

    # skillname=request.form['skill']
    Skills.query.filter_by(pid=info.pid).delete()
    db.session.commit()

    return redirect('/dashboard#skill')
    # return render_template('dashboard.html', skillinfo=skillinfo, skills=Skills, info=info, user=user   )

@app.route('/projectinfo', methods=['GET','POST'])
def projectinfo():
    #--Project----------------------------------------------------
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    projinfo=Projects.query.filter_by(pid=info.pid).first()
    skillinfo=Skills.query.filter_by(pid=info.pid).all()
    
    if request.method == "POST":
            
        projname=request.form['projectName']
        link=request.form['link']
        prinfo=request.form['projectDescription']
        projimg=request.files['projectImage'].read()
            
        projectcheck=Projects.query.filter_by(pid=info.pid).first()
        if not projectcheck:
            pass
        
        addproj=Projects(pid=info.pid, pname=projname, link=link , pinfo=prinfo, pimg=projimg)
        db.session.add(addproj)
            
        db.session.commit()


    
    # img2 = base64.b64encode(projectinfo.pimg).decode("utf-8") 
    #--find another card for displaying project info without img
    return redirect('/dashboard#projects')
    #------------------------------------------------------------------------
    
    


@app.route('/dashboard/clearproj', methods=['GET','POST'])
def clearproj():
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    projinfo=Projects.query.filter_by(pid=info.pid).all()
    

    # skillname=request.form['skill']
    Projects.query.filter_by(pid=info.pid).delete()
    db.session.commit()

    return redirect('/dashboard#projects')


@app.route('/expinfo', methods=['GET','POST'])
def expinfo():
    #--Experience-------------------------------------------------
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    projinfo=Projects.query.filter_by(pid=info.pid).first()
    expinfo=Experience.query.filter_by(pid=info.pid).all()
    
    if request.method == "POST":
            
        exptitle=request.form['title']
        exporg=request.form['org']
        expyear=request.form['year']
        expdes=request.form['des']
        expcheck=Experience.query.filter_by(pid=info.pid).first()
        if not expcheck:
            pass
        
        addexp=Experience(pid=info.pid, job_title=exptitle, company_name=exporg, year=expyear, description=expdes)
        db.session.add(addexp)
            
        db.session.commit()


    projectinfo=Projects.query.filter_by(pid=info.pid).all()
    # img2 = base64.b64encode(projectinfo.pimg).decode("utf-8") 
    #--find another card for displaying project info without img
    return redirect('/dashboard#experience')

@app.route('/dashboard/clearexp', methods=['GET','POST'])
def clearexp():
    user=Users.query.filter_by(username=session['user']).first()
    info=Portfolio.query.filter_by(user_id=user.user_id).first()
    expinfo=Experience.query.filter_by(pid=info.pid).all()
    

    # skillname=request.form['skill']
    Experience.query.filter_by(pid=info.pid).delete()
    db.session.commit()

    return redirect('/dashboard#experience')

# if __name__  == '__main__':
#     app.run(debug=True)
