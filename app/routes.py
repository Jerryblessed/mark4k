import os, io, pypdf
from flask import Blueprint, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
from .utils import call_agent, extract_code_blocks, build_zip, generate_pdf

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('chat.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username taken')
        else:
            user = User(username=request.form['username'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    history = session.get("history", [])
    history.append({"role": "user", "content": msg})
    reply = call_agent(history)
    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-10:]
    return jsonify({"reply": reply, "code_blocks": extract_code_blocks(reply)})

@main.route("/analyze-pdf", methods=["POST"])
@login_required
def analyze_pdf():
    if "file" not in request.files: return jsonify({"error": "No file"}), 400
    pdf_file = request.files["file"]
    reader = pypdf.PdfReader(io.BytesIO(pdf_file.read()))
    text = "\n".join(p.extract_text() for p in reader.pages)[:5000]
    prompt = f"Analyze this PDF text and summarize: {text}"
    reply = call_agent([{"role": "user", "content": prompt}])
    return jsonify({"reply": reply, "code_blocks": []})

@main.route("/download-zip", methods=["POST"])
def dl_zip():
    data = request.get_json()
    return send_file(build_zip(data.get("code_blocks", [])), mimetype="application/zip", as_attachment=True, download_name="project.zip")

@main.route("/download-plan", methods=["POST"])
def dl_pdf():
    data = request.get_json()
    return send_file(generate_pdf("Mark4k Plan", data.get("content", "")), mimetype="application/pdf", as_attachment=True, download_name="plan.pdf")
