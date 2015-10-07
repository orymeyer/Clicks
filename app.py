from flask import Flask,jsonify,request,render_template,send_file,redirect,abort,session,url_for
from model import *
from user import *
import random,string
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(__name__)
app.secret_key =os.getenv("SECRET")


@app.route('/')
def getIndexPage():
    if not session.get('userName'):

        return redirect(url_for('welcomePage'))
    return render_template('index.html')

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
def showStatsPage():
    if not session.get('userName'):
        return redirect(url_for('welcomePage'))
    userName = session["userName"]
    kv,num= showStats(userName)
    return render_template('stats.html', kv=kv,num =num)

@app.route('/update/<link>',methods=['POST'])
def updatelink(link):
     details = request.args['details']
     update(link,details)
     return jsonify({'stats':'success'}), 200



@app.route('/stats/l/<link>')
def showLinkStats(link):
    if not session.get('userName'):
        return redirect(url_for('welcomePage'))
    lstats =  showLStats(link)
    if lstats is None:
        return "No Stats yet"
    id = lstats["sURL"]
    #return jsonify(lstats)
    return render_template('linkStat.html',id=id,data=lstats)


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

'''

if __name__ =='__main__':
    app.run(debug=True)
'''