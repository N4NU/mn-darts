from flask import url_for, render_template, request, redirect, session
from darts.app import app
from darts.models import db, Enquete_posts
import datetime

@app.route('/enquete', methods=['GET', 'POST'])
def enquete():
    if request.method == 'GET':
        return render_template('enquete.html')
    else:
        service = request.form.get('service')
        comment = request.form.get('comment')

        if comment == None or comment == '' or  service == None or service == '':
            return redirect(url_for('enquete'))

        new_thread = Enquete_posts(posted_at=datetime.datetime.utcnow(), service=service, message=comment, ip_addr=request.environ['REMOTE_ADDR'])
        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('enquete'))
