from flask import Flask, render_template, redirect, url_for, request
from models import db, Job
from fetch_jobs import fetch_jobs
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate
import atexit
from datetime import datetime, timedelta
from dateutil import parser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize last_refreshed with the current time when the app starts
last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Pagination settings
RESULTS_PER_PAGE = 10

def insert_jobs(jobs_data):
    for job in jobs_data:
        # Check if the job with the same URL already exists in the database
        if not Job.query.filter_by(url=job.get('link')).first():
            new_job = Job(
                title=job.get('title'),
                company=job.get('company'),
                location=job.get('location'),
                description=job.get('snippet'),
                url=job.get('link'),
                date_posted=job.get('updated')
            )
            db.session.add(new_job)
            logging.info("Inserted job: %s", new_job.title)  # Log inserted jobs for debugging
    db.session.commit()

@app.before_first_request
def create_tables():
    db.create_all()

def parse_date(date_str):
    """Attempts to parse a date string in multiple formats."""
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        return "Unknown Date"

@app.route('/', methods=['GET', 'POST'])
def index():
    title_filter = request.args.get('title', '')
    date_filter = request.args.get('date_posted', '')
    location_filter = request.args.get('location', '')
    page = request.args.get('page', 1, type=int)

    query = Job.query.filter(Job.status.notin_(["Applied", "Scheduled for Interview"]))
    
    if title_filter:
        query = query.filter(Job.title.ilike(f"%{title_filter}%"))
    if date_filter:
        query = query.filter(Job.date_posted == date_filter)
    if location_filter:
        query = query.filter(Job.location.ilike(f"%{location_filter}%"))

    jobs = query.paginate(page=page, per_page=RESULTS_PER_PAGE)

    for job in jobs.items:
        job.date_posted = parse_date(job.date_posted)

    return render_template(
        'index.html',
        jobs=jobs,
        title_filter=title_filter,
        date_filter=date_filter,
        location_filter=location_filter,
        last_refreshed=last_refreshed
    )

@app.route('/applied')
def applied_jobs():
    location_filter = request.args.get('location', '')
    page = request.args.get('page', 1, type=int)

    query = Job.query.filter_by(status="Applied")
    
    if location_filter:
        query = query.filter(Job.location.ilike(f"%{location_filter}%"))

    jobs = query.paginate(page=page, per_page=RESULTS_PER_PAGE)

    for job in jobs.items:
        job.date_posted = parse_date(job.date_posted)

    return render_template(
        'applied_jobs.html',
        jobs=jobs,
        location_filter=location_filter
    )

@app.route('/interview-scheduled')
def interview_scheduled_jobs():
    location_filter = request.args.get('location', '')
    page = request.args.get('page', 1, type=int)

    query = Job.query.filter_by(status="Scheduled for Interview")
    
    if location_filter:
        query = query.filter(Job.location.ilike(f"%{location_filter}%"))

    jobs = query.paginate(page=page, per_page=RESULTS_PER_PAGE)

    for job in jobs.items:
        job.date_posted = parse_date(job.date_posted)

    return render_template(
        'interview_scheduled_jobs.html',
        jobs=jobs,
        location_filter=location_filter
    )

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        location = request.form['location']
        if keyword:
            jobs_data = fetch_jobs(keyword, location)
            insert_jobs(jobs_data)
            return redirect(url_for('index'))
        else:
            error = "Please enter a keyword to search."
            return render_template('search.html', error=error)
    return render_template('search.html')


@app.route('/update_status/<int:job_id>', methods=['POST'])
def update_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.status = request.form['status']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/schedule_interview', methods=['POST'])
def schedule_interview():
    job_id = request.form.get('job_id')
    interview_date = request.form.get('interview_date')
    
    job = Job.query.get_or_404(job_id)
    job.status = "Scheduled for Interview"
    job.interview_date = datetime.strptime(interview_date, "%Y-%m-%d").date()
    db.session.commit()
    
    return redirect(url_for('applied_jobs'))

@app.route('/update_interview_status/<int:job_id>', methods=['POST'])
def update_interview_status(job_id):
    job = Job.query.get_or_404(job_id)
    interview_status = request.form.get('interview_status')
    job.interview_status = interview_status
    db.session.commit()
    return redirect(url_for('interview_scheduled_jobs'))

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('interview_scheduled_jobs'))

def scheduled_job():
    """Fetch new jobs periodically based on predefined keywords, with error handling."""
    global last_refreshed
    keywords = ['data scientist', 'data analyst', 'data engineer']  # Example keywords

    try:
        for keyword in keywords:
            jobs_data = fetch_jobs(keyword)
            with app.app_context():
                insert_jobs(jobs_data)

        last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Scheduled job ran and jobs were fetched.")
    except Exception as e:
        logging.error("Error in scheduled_job: %s", e)

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_job, trigger="interval", days=1)  # Daily interval

scheduler.start()

with app.app_context():
    scheduled_job()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
