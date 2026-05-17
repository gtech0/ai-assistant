from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from config import Config
from models import db, Project, Risk
from llm_client import LLMClient
from report_service import ReportService

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
llm_client = LLMClient()

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_project', methods=['POST'])
def create_project():
    name = request.form.get('name', '').strip()
    if not name:
        flash("Название обязательно.", "error")
        return redirect(url_for('index'))

    params = {
        'name': name,
        'duration': request.form.get('duration', ''),
        'budget': request.form.get('budget', ''),
        'lifecycle_type': request.form.get('lifecycle_type', ''),
        'dev_type': request.form.get('dev_type', ''),
        'tech_stack': request.form.get('tech_stack', ''),
        'team': request.form.get('team', ''),
        'team_skill_level': safe_float(request.form.get('team_skill_level'), 3.0)
    }

    doc_file = request.files.get('documentation')
    doc_text = doc_file.read().decode('utf-8', errors='ignore') if doc_file else ""

    llm_risks = llm_client.generate_risks(params, doc_text)
    if not llm_risks:
        flash("Ошибка ИИ.", "error")
        return redirect(url_for('index'))

    project = Project(**params)
    db.session.add(project)
    db.session.commit()

    for r in llm_risks:
        prob = float(r.get('probability', 0.5))
        impact = int(r.get('impact', 3))
        risk = Risk(
            project_id=project.id,
            name=r.get('name', 'Unknown'),
            risk_type=r.get('risk_type'),
            factor_category=r.get('factor_category'),
            category=r.get('category', 'Other'),
            probability=prob,
            impact=impact,
            criticality=round(prob * (impact / 5.0), 2),
            strategy=r.get('strategy', 'Analysis'),
            owner="Project Manager",
            is_llm_generated=True
        )

        db.session.add(risk)
    db.session.commit()
    return redirect(url_for('view_risks', project_id=project.id))


@app.route('/risks/<int:project_id>')
def view_risks(project_id):
    project = Project.query.get_or_404(project_id)
    risks = Risk.query.filter_by(project_id=project_id).all()
    return render_template('risks.html', project=project, risks=risks)


@app.route('/update_risk/<int:risk_id>', methods=['POST'])
def update_risk(risk_id):
    risk = Risk.query.get_or_404(risk_id)
    try:
        risk.probability = float(request.form['probability'])
        risk.impact = int(request.form['impact'])
        risk.criticality = risk.probability * (risk.impact / 5.0)
        risk.owner = request.form['owner']
        risk.strategy = request.form['strategy']
        db.session.commit()
        flash('Updated', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", 'error')
    return redirect(request.referrer or url_for('view_risks', project_id=risk.project_id))


@app.route('/generate_ideas', methods=['POST'])
def generate_ideas():
    params = {
        'name': request.form.get('name', ''),
        'duration': request.form.get('duration', ''),
        'budget': request.form.get('budget', ''),
        'lifecycle_type': request.form.get('lifecycle_type', ''),
        'dev_type': request.form.get('dev_type', ''),
        'tech_stack': request.form.get('tech_stack', ''),
        'team': request.form.get('team', ''),
        'team_skill_level': safe_float(request.form.get('team_skill_level'), 3.0)
    }
    ideas = llm_client.generate_ideas(params, "")
    return jsonify({"ideas": ideas})


@app.route('/export_excel/<int:project_id>')
def export_excel(project_id):
    project = Project.query.get_or_404(project_id)
    risks = Risk.query.filter_by(project_id=project_id).all()
    buffer = ReportService.generate_excel_report(project, risks)
    return send_file(buffer, download_name=f"risks_{project.name}.xlsx", as_attachment=True)


def safe_float(value, default=0.0):
    if value is None:
        return default
    try:
        clean_value = str(value).strip()
        return float(clean_value) if clean_value else default
    except ValueError:
        return default


if __name__ == '__main__':
    app.run(debug=True, port=5000)
