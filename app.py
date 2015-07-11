from flask import Flask,jsonify,request,render_template,send_file
from model import *
import random,string
app = Flask(__name__)

@app.route('/')
def getIP():
    return render_template('index.html')


@app.route('/link/generate')
def generateLink():
    linkID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    createTrap(linkID)
    return jsonify({'id': linkID}), 200

@app.route('/link/click/<link>')
def recordClick(link):
    #IP = request.remote_addr
    print request.user_agent.string
    IP =  str(request.headers["x-forwarded-for"]);
    recordLinkClick(link,IP)
    return render_template('page.html')

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
    
@app.route('update/<link>',methods=['POST'])
def updatelink(id,details):
     update(id,details)
     return jsonify({'stats':'success'}), 200

@app.route('/pic')
def showPic():

    return render_template('page.html')


if __name__ == '__main__':
    app.run(debug=True)