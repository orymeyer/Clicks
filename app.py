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
    provided_ips = request.access_route[0] #this one always works be remote_addr or x-forwarded-for
    bURL = recordLinkClick(sURL,provided_ips,UA,REF)
    return redirect(bURL,code=302)



@app.route('/stats')
def showStatsPage():
    kv,num= showStats()
    return render_template('stats.html', kv=kv,num =num)

@app.route('/update/<link>',methods=['POST'])
def updatelink(link):
     details = request.args['details']
     update(link,details)
     return jsonify({'stats':'success'}), 200



@app.route('/stats/<link>')
def showLinkStats(link):
    lstats =  showLStats(link)
    if lstats is None:
        return "No Stats yet"
    id = lstats["sURL"]
    #return jsonify(lstats)
    return render_template('linkStat.html',id=id,data=lstats)


@app.route('/pic')
def showPic():
    return render_template('page.html')


if __name__ == '__main__':
    app.run(debug=True)
