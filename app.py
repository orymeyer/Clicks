from flask import Flask,jsonify,request,render_template,send_file,redirect
from model import *
import random,string
app = Flask(__name__)

@app.route('/')
def getIP():
    return render_template('index.html')


@app.route('/link/generate',methods=['POST'])
def generateLink():
    bURL = request.form['URL']
    linkID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    createLink(bURL,linkID)
    return jsonify({'id': linkID}), 200

@app.route('/<sURL>')
def recordClick(sURL):
    UA =  request.user_agent.string
    REF = request.headers.get("Referer")
    provided_ips = request.access_route #this one always works be remote_addr or x-forwarded-for
    bURL = recordLinkClick(sURL,provided_ips,UA,REF)
    return redirect(bURL,code=302)

@app.route('/api/link/<link>')
def showStats(link):
    lstats =  showLinkStats(link)
    lstats["_id"] = None
    return jsonify({'stats':lstats}), 200


@app.route('/link/<link>')
def showStatsPage(link):
    lstats =  showLinkStats(link)
    lstats["_id"] = None
    id = lstats["lid"]

    return render_template('stats.html',id=id,data=lstats)

@app.route('/update/<link>',methods=['POST'])
def updatelink(link):
     details = request.args['details']
     update(link,details)
     return jsonify({'stats':'success'}), 200

@app.route('/pic')
def showPic():

    return render_template('page.html')


if __name__ == '__main__':
    app.run(debug=True)
