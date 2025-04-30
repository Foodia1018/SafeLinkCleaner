"""
Route definitions for the SafeLink Protection Cleaner application
"""
import os
import json
import time
import logging
import pandas as pd
import threading
from flask import render_template, request, jsonify, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
from app import app, db
from models import EmailList, Email, SecurityStats, ProcessingJob
from email_processor import process_email_list, get_security_system_stats, analyze_email_domain
from email_validator import is_valid_email, is_valid_domain

# Configure logger
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page route"""
    # Get recent email list processing jobs
    recent_lists = EmailList.query.order_by(EmailList.created_at.desc()).limit(10).all()
    
    # Get overall statistics
    total_processed = EmailList.query.count()
    total_emails = db.session.query(db.func.sum(EmailList.original_count)).scalar() or 0
    total_cleaned = db.session.query(db.func.sum(EmailList.cleaned_count)).scalar() or 0
    removal_rate = (total_emails - total_cleaned) / total_emails * 100 if total_emails else 0
    
    # Get security system statistics
    security_stats = db.session.query(
        SecurityStats.security_system, 
        db.func.sum(SecurityStats.count).label('total')
    ).group_by(SecurityStats.security_system).all()
    
    security_data = [{'name': stat.security_system, 'count': stat.total} for stat in security_stats]
    
    return render_template(
        'dashboard.html',
        recent_lists=recent_lists,
        total_processed=total_processed,
        total_emails=total_emails,
        total_cleaned=total_cleaned,
        removal_rate=removal_rate,
        security_data=json.dumps(security_data)
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'emailList' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['emailList']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    # Validate file extension
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext not in ['csv', 'txt', 'xlsx']:
        flash('Invalid file format. Please upload CSV, TXT, or XLSX files.', 'error')
        return redirect(request.url)
    
    # Process file
    try:
        # Read email addresses from file
        emails = []
        if file_ext == 'csv':
            df = pd.read_csv(file)
            # Check if the CSV has an 'email' column
            if 'email' in df.columns:
                emails = df['email'].tolist()
            else:
                # Try to use the first column
                emails = df.iloc[:, 0].tolist()
        elif file_ext == 'txt':
            content = file.read().decode('utf-8')
            emails = [line.strip() for line in content.split('\n') if line.strip()]
        elif file_ext == 'xlsx':
            df = pd.read_excel(file)
            # Check if the Excel file has an 'email' column
            if 'email' in df.columns:
                emails = df['email'].tolist()
            else:
                # Try to use the first column
                emails = df.iloc[:, 0].tolist()
        
        # Filter out empty items and validate email format
        emails = [email for email in emails if isinstance(email, str) and is_valid_email(email)]
        
        # Create a new email list in the database
        email_list = EmailList(
            filename=filename,
            original_count=len(emails)
        )
        db.session.add(email_list)
        db.session.commit()
        
        # Start processing in a background thread
        processing_job = ProcessingJob(
            list_id=email_list.id,
            status='queued'
        )
        db.session.add(processing_job)
        db.session.commit()
        
        # Start the background thread for processing
        thread = threading.Thread(
            target=process_email_list_background,
            args=(email_list.id, processing_job.id, emails)
        )
        thread.daemon = True
        thread.start()
        
        flash(f'Upload successful! Processing {len(emails)} emails...', 'success')
        return redirect(url_for('results', list_id=email_list.id))
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

def process_email_list_background(list_id, job_id, emails):
    """Process email list in a background thread"""
    try:
        # Update job status
        job = ProcessingJob.query.get(job_id)
        job.status = 'processing'
        db.session.commit()
        
        # Process the email list
        start_time = time.time()
        result = process_email_list(emails)
        
        # Update database with results
        email_list = EmailList.query.get(list_id)
        email_list.cleaned_count = len(result['cleaned_list'])
        email_list.processed = True
        email_list.processing_time = time.time() - start_time
        
        # Add individual emails to the database
        batch_size = 100
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i+batch_size]
            email_objects = []
            
            for email_address in batch:
                domain = email_address.split('@')[-1]
                removed = email_address not in result['cleaned_list']
                
                # Find reason if removed
                reason = None
                security_system = None
                if removed:
                    for removed_email in result['removed_emails']:
                        if removed_email['email'] == email_address:
                            reason = removed_email['reason']
                            if 'Protected by ' in reason:
                                security_system = reason.replace('Protected by ', '')
                            break
                
                email_obj = Email(
                    address=email_address,
                    domain=domain,
                    valid=email_address in result['cleaned_list'],
                    removed=removed,
                    reason=reason,
                    security_system=security_system,
                    list_id=list_id
                )
                email_objects.append(email_obj)
            
            db.session.bulk_save_objects(email_objects)
            db.session.commit()
            
            # Update progress
            job.progress = min(100, int((i + len(batch)) / len(emails) * 100))
            db.session.commit()
        
        # Add security system statistics
        security_stats = get_security_system_stats(result['removed_emails'])
        for system, count in security_stats.items():
            stat = SecurityStats(
                security_system=system,
                count=count,
                list_id=list_id
            )
            db.session.add(stat)
        
        # Update job status to completed
        job.status = 'completed'
        job.progress = 100
        job.completed_at = time.time()
        db.session.commit()
        
        logger.info(f"Completed processing email list {list_id}")
    
    except Exception as e:
        logger.error(f"Error in background processing: {str(e)}")
        # Update job status to failed
        job = ProcessingJob.query.get(job_id)
        job.status = 'failed'
        job.error = str(e)
        db.session.commit()

@app.route('/results/<int:list_id>')
def results(list_id):
    """Results page for a specific email list"""
    email_list = EmailList.query.get_or_404(list_id)
    job = ProcessingJob.query.filter_by(list_id=list_id).first()
    
    # Get security system statistics
    security_stats = SecurityStats.query.filter_by(list_id=list_id).all()
    security_data = [{'name': stat.security_system, 'count': stat.count} for stat in security_stats]
    
    # Get sample removed emails
    removed_emails = Email.query.filter_by(list_id=list_id, removed=True).limit(50).all()
    
    # Get domain statistics
    domain_stats = db.session.query(
        Email.domain, 
        db.func.count(Email.id).label('count')
    ).filter_by(list_id=list_id).group_by(Email.domain).order_by(db.text('count DESC')).limit(10).all()
    
    domain_data = [{'domain': stat.domain, 'count': stat.count} for stat in domain_stats]
    
    return render_template(
        'results.html',
        email_list=email_list,
        job=job,
        security_data=json.dumps(security_data),
        domain_data=json.dumps(domain_data),
        removed_emails=removed_emails
    )

@app.route('/api/job-status/<int:job_id>')
def job_status(job_id):
    """API endpoint to get job status"""
    job = ProcessingJob.query.get_or_404(job_id)
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'error': job.error
    })

@app.route('/export/<int:list_id>/<format>')
def export(list_id, format):
    """Export cleaned email list in the specified format"""
    if format not in ['csv', 'json', 'xlsx']:
        flash('Invalid export format', 'error')
        return redirect(url_for('results', list_id=list_id))
    
    email_list = EmailList.query.get_or_404(list_id)
    
    # Get cleaned emails
    cleaned_emails = Email.query.filter_by(list_id=list_id, removed=False).all()
    cleaned_data = [{'email': email.address, 'domain': email.domain} for email in cleaned_emails]
    
    # Create temporary file
    filename = f"cleaned_emails_{list_id}.{format}"
    temp_path = os.path.join('/tmp', filename)
    
    if format == 'csv':
        df = pd.DataFrame(cleaned_data)
        df.to_csv(temp_path, index=False)
    elif format == 'json':
        with open(temp_path, 'w') as f:
            json.dump(cleaned_data, f)
    elif format == 'xlsx':
        df = pd.DataFrame(cleaned_data)
        df.to_excel(temp_path, index=False)
    
    return send_file(
        temp_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/octet-stream'
    )

@app.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint to analyze a single email domain"""
    data = request.json
    email = data.get('email', '')
    
    if not is_valid_email(email):
        return jsonify({
            'error': 'Invalid email format'
        }), 400
    
    domain = email.split('@')[-1]
    
    analysis = analyze_email_domain(domain)
    return jsonify(analysis)
