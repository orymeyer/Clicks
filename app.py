from flask import Flask,jsonify,request,render_template,redirect,session,url_for,make_response
from model import *
from user import *
from functools import wraps
import random,string
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(__name__)
app.secret_key =os.getenv("SECRET")



def login_required(f):
    @wraps(f)
    def login_function(*args, **kwargs):
        if not session.get('loggedIN'):
            return redirect(url_for('welcomePage',next=request.url))
        return f(*args, **kwargs)
    return login_function



@app.route('/')
@login_required
def getIndexPage():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]

    return render_template('index.html',userName=username)

@app.route('/welcome')
def welcomePage():
    return render_template('login.html')

@app.route('/link/generate',methods=['POST'])
def generateLink():
    bURL = request.form['URL']
    linkID ='l/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    username = session['userName']
    createLink(bURL,linkID,username)
    return jsonify({"status":"Success",'id': linkID}), 200

@app.route('/l/<sURL>')
def recordClick(sURL):
    UA =  request.user_agent.string
    REF = request.headers.get("Referer")
    provided_ips = request.access_route[0] #this one always works be remote_addr or x-forwarded-for
    bURL = recordLinkClick(sURL,provided_ips,UA,REF)
    return redirect(bURL,code=302)



@app.route('/stats')
@login_required
def showStatsPage():
    page = request.args.get("page")
    userName = session["userName"]
    kv,num= showStats(userName,page)
    return render_template('stats.html', kv=kv,num =num,userName=userName)

@app.route('/update/<link>',methods=['POST'])
def updatelink(link):
     details = request.args['details']
     update(link,details)
     return jsonify({'stats':'success'}), 200



@app.route('/stats/l/<link>')
@login_required
def showLinkStats(link):
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    lstats =  showLStats(link)
    if lstats is None:
        return "No Stats yet"
    id = lstats["sURL"]
    #return jsonify(lstats)
    return render_template('linkStat.html',id=id,data=lstats)



@app.route('/deleteAccount')
@login_required
def deleteAccount():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    if removeUser(username):
        return jsonify(status="Success")
    else:
        return jsonify(status="Failed")

@app.route('/delete/sURL')
@login_required
def delete(sURL):
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    if removesURL(sURL,username):
        return jsonify(status="Success")
    else:
        return jsonify(status="Failed")


@app.route('/pic')
def showPic():
    return render_template('page.html')




@app.route('/register', methods = ['POST'])
def new_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if username is None or password is None:
        return jsonify(status="Failed")# missing arguments
    elif returnUser(username):
        return jsonify(status="Failed")
    else:
        pass_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        registerUser(username,email,pass_hash)
    return jsonify(status="Success")


@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username is None or password is None:
        return jsonify(status="Failed")# missing arguments
    userPHash = returnPHash(username)
    if userPHash is False:
        return jsonify(status="AuthFailed")
    #print userPHash.encode('utf-8'), password
    if bcrypt.check_password_hash(userPHash.encode('utf-8'), password):
        session["loggedIN"]=True
        session["userName"]=username
        return jsonify(status="LoggedIN")
    else:
        return jsonify(status="AuthFailed")

@app.route('/logout')
def logout():
    session.pop('userName',None)
    session["loggedIN"]=False
    return redirect(url_for('welcomePage'))

@app.route('/page')
def page():
    return render_template('page.html')

@app.route('/accounts')
@login_required
def settings():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    return render_template('accounts.html',userName=username)


@app.route('/updateAccount', methods = ['POST'])
@login_required
def update():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    password = None


    newPassword = request.form['newPassword']
    oldPassword =  request.form['oldPassword']
    userPHash = returnPHash(username)

    if bcrypt.check_password_hash(userPHash.encode('utf-8'),oldPassword):
        newPassword = bcrypt.generate_password_hash(newPassword.encode('utf-8'))
        updateUser(username,newPassword)
        return jsonify(status="Success")
    else:
        return jsonify(status="Failed")




@app.route('/updateEmail', methods = ['POST'])
@login_required
def updateEmail():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    email = request.form['email']
    if updateEmail(username,email):
        return jsonify(status="Success")
    else:
        return jsonify(status="Failed")


@app.route('/export')
@login_required
def exportUserData():
    '''
    if not session.get('loggedIN'):
        return redirect(url_for('welcomePage'))
    '''
    username = session["userName"]
    data = exportData(username)
    response = make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename=urls.csv"
    return response





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

'''

if __name__ =='__main__':
    app.run(debug=True)

'''