from flask import url_for, render_template, request, redirect, session
from darts.app import app

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    return render_template('ranking.html')
