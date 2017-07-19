from flask import url_for, render_template, request, redirect, session
from darts.app import app

@app.route('/enquete', methods=['GET', 'POST'])
def enquete():
    return render_template('enquete.html')