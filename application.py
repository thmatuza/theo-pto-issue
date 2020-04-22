from flask import Flask, render_template
from datetime import datetime, timedelta
import time
import ssl

app = Flask(__name__)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/manifest.mpd')
def manifest():
    now = datetime.now()
    start = now + timedelta(seconds=-60)
    unixtime = time.mktime(start.timetuple())
    txt = "PT{unixtime:.6f}S"
    strStart = txt.format(unixtime = unixtime)
    audio_pto = 239616
    audio_pto += 1 # if you comment out this, THEOplayer 2.69.1 can play it without problem.
    return render_template('manifest.mpd', start=strStart, audio_pto=audio_pto)

if __name__ == '__main__':
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain('cert/server.crt', 'cert/server.key')
    app.run(debug=True, host='0.0.0.0', port=8443, ssl_context=ctx)
