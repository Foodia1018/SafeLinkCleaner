"""
Email validation module for SafeLink Protection Cleaner.
Provides functions for validating email addresses and domains.
"""
import re
import dns.resolver
import socket
from config import EMAIL_REGEX, DNS_TIMEOUT

def is_valid_email(email):
    """
    Check if an email has valid format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email has valid format, False otherwise
    """
    if not isinstance(email, str):
        return False
    
    pattern = re.compile(EMAIL_REGEX)
    return bool(pattern.match(email))

def is_valid_domain(domain):
    """
    Check if a domain is valid
    
    Args:
        domain (str): Domain to validate
        
    Returns:
        bool: True if domain is valid, False otherwise
    """
    try:
        # First check basic domain format
        if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
            return False
        
        # Try to resolve the domain's A record
        socket.setdefaulttimeout(DNS_TIMEOUT)
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        # Try to resolve MX records as a fallback
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    except Exception:
        return False

def check_mx_record(domain):
    """
    Check if a domain has valid MX records
    
    Args:
        domain (str): Domain to check
        
    Returns:
        bool: True if domain has valid MX records, False otherwise
    """
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return False
    except Exception:
        return False

def verify_email_smtp(email):
    """
    Perform a light SMTP verification of an email address 
    (doesn't actually send an email, just checks if the mailbox exists)
    
    Note: This can trigger spam filters if used excessively.
    Use with caution and implement rate limiting.
    
    Args:
        email (str): Email address to verify
        
    Returns:
        bool: True if email appears to be valid, False otherwise
    """
    # This functionality is disabled by default to avoid spam triggers
    # Implement if needed with proper rate limiting and error handling
    return True  # Default to True as a placeholder
