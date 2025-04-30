"""
Email processor module for SafeLink Protection Cleaner.
Handles the processing of email lists to detect and remove emails protected by security systems.
"""
import asyncio
import logging
import time
import concurrent.futures
from collections import Counter
from email_validator import is_valid_email, is_valid_domain, check_mx_record
from security_patterns import is_protected_by_security_system
from config import DISPOSABLE_EMAIL_DOMAINS, MAX_THREADS, BATCH_SIZE

# Configure logger
logger = logging.getLogger(__name__)

async def process_email_async(email):
    """
    Process a single email asynchronously
    
    Args:
        email (str): Email address to process
        
    Returns:
        dict: Processing result with status and reason if removed
    """
    if not is_valid_email(email):
        return {
            'email': email,
            'valid': False,
            'removed': True,
            'reason': 'Invalid Email Format'
        }
    
    # Extract domain from email
    domain = email.split('@')[-1]
    
    # Check if domain is in disposable email list
    if domain.lower() in [d.lower() for d in DISPOSABLE_EMAIL_DOMAINS]:
        return {
            'email': email,
            'valid': False,
            'removed': True,
            'reason': 'Disposable Email Domain'
        }
    
    # Check if domain is valid
    if not is_valid_domain(domain):
        return {
            'email': email,
            'valid': False,
            'removed': True,
            'reason': 'Invalid Domain'
        }
    
    # Check if domain has MX records
    has_mx = await asyncio.to_thread(check_mx_record, domain)
    if not has_mx:
        return {
            'email': email,
            'valid': False,
            'removed': True,
            'reason': 'No MX Records'
        }
    
    # Check if domain is protected by a security system
    is_protected, security_system = await asyncio.to_thread(is_protected_by_security_system, domain)
    if is_protected:
        return {
            'email': email,
            'valid': True,
            'removed': True,
            'reason': f'Protected by {security_system}'
        }
    
    # Email is valid and not protected
    return {
        'email': email,
        'valid': True,
        'removed': False,
        'reason': None
    }

async def process_batch_async(emails):
    """
    Process a batch of emails asynchronously
    
    Args:
        emails (list): List of email addresses
        
    Returns:
        list: Processing results for each email
    """
    tasks = [process_email_async(email) for email in emails]
    return await asyncio.gather(*tasks)

def process_email_list(emails):
    """
    Process a list of emails to filter out protected and invalid ones
    
    Args:
        emails (list): List of email addresses
        
    Returns:
        dict: Processing results with cleaned list and removed emails
    """
    logger.info(f"Processing {len(emails)} emails")
    start_time = time.time()
    
    # Create event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Process emails in batches
    results = []
    for i in range(0, len(emails), BATCH_SIZE):
        batch = emails[i:i+BATCH_SIZE]
        batch_results = loop.run_until_complete(process_batch_async(batch))
        results.extend(batch_results)
        logger.debug(f"Processed batch {i//BATCH_SIZE + 1}/{len(emails)//BATCH_SIZE + 1}")
    
    # Close event loop
    loop.close()
    
    # Separate cleaned and removed emails
    cleaned_list = [result['email'] for result in results if not result['removed']]
    removed_emails = [{'email': result['email'], 'reason': result['reason']} for result in results if result['removed']]
    
    logger.info(f"Processed {len(emails)} emails in {time.time() - start_time:.2f} seconds")
    logger.info(f"Removed {len(removed_emails)} emails, {len(cleaned_list)} emails remaining")
    
    return {
        'original_list_size': len(emails),
        'clean_list_size': len(cleaned_list),
        'removed_emails': removed_emails,
        'cleaned_list': cleaned_list
    }

def get_security_system_stats(removed_emails):
    """
    Get statistics for removed emails by security system
    
    Args:
        removed_emails (list): List of removed emails with reasons
        
    Returns:
        dict: Count of emails removed by each security system
    """
    security_systems = {}
    
    for email in removed_emails:
        reason = email.get('reason', '')
        if 'Protected by ' in reason:
            security_system = reason.replace('Protected by ', '')
            security_systems[security_system] = security_systems.get(security_system, 0) + 1
    
    return security_systems

def analyze_email_domain(domain):
    """
    Analyze a single email domain for detailed information
    
    Args:
        domain (str): Domain to analyze
        
    Returns:
        dict: Analysis results
    """
    # Check if domain is valid
    valid_domain = is_valid_domain(domain)
    
    # Check if domain has MX records
    has_mx = check_mx_record(domain) if valid_domain else False
    
    # Check if domain is protected by a security system
    is_protected, security_system = is_protected_by_security_system(domain) if valid_domain else (False, None)
    
    # Check if domain is a disposable email domain
    is_disposable = domain.lower() in [d.lower() for d in DISPOSABLE_EMAIL_DOMAINS]
    
    return {
        'domain': domain,
        'valid_domain': valid_domain,
        'has_mx_records': has_mx,
        'is_protected': is_protected,
        'security_system': security_system,
        'is_disposable': is_disposable
    }
