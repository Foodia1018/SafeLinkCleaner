"""
Security pattern detection for various email security gateways.
This module contains regex patterns and detection algorithms for identifying
emails protected by security systems like Microsoft Safe Links, Proofpoint, etc.
"""
import re
import dns.resolver
from config import SECURITY_SYSTEMS

# Compiled regex patterns for efficiency
PATTERN_CACHE = {}

def get_pattern(pattern_str):
    """Get or create compiled regex pattern"""
    if pattern_str not in PATTERN_CACHE:
        PATTERN_CACHE[pattern_str] = re.compile(pattern_str, re.IGNORECASE)
    return PATTERN_CACHE[pattern_str]

def detect_security_system_from_mx(domain):
    """
    Detect security systems based on MX records
    
    Args:
        domain (str): The email domain to check
        
    Returns:
        str or None: The detected security system name or None
    """
    try:
        # Query MX records
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = [str(rdata.exchange).rstrip('.').lower() for rdata in answers]
        
        # Check for security system patterns in MX records
        for system_id, system_info in SECURITY_SYSTEMS.items():
            for pattern in system_info.get('mx_patterns', []):
                for mx_record in mx_records:
                    if pattern.lower() in mx_record:
                        return system_info['name']
        
        return None
    
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return None
    except Exception as e:
        print(f"Error checking MX records for {domain}: {str(e)}")
        return None

def detect_security_system_from_txt(domain):
    """
    Detect security systems based on TXT records
    
    Args:
        domain (str): The email domain to check
        
    Returns:
        str or None: The detected security system name or None
    """
    try:
        # Query TXT records
        answers = dns.resolver.resolve(domain, 'TXT')
        txt_records = [str(rdata).lower() for rdata in answers]
        
        # Check for security system patterns in TXT records
        for system_id, system_info in SECURITY_SYSTEMS.items():
            for pattern in system_info.get('patterns', []):
                pattern_regex = get_pattern(pattern)
                for txt_record in txt_records:
                    if pattern_regex.search(txt_record):
                        return system_info['name']
        
        # Check for SPF records which might indicate protection services
        for txt_record in txt_records:
            if 'v=spf1' in txt_record:
                # Check for specific security services in SPF record
                for system_id, system_info in SECURITY_SYSTEMS.items():
                    for pattern in system_info.get('patterns', []):
                        pattern_regex = get_pattern(pattern)
                        if pattern_regex.search(txt_record):
                            return system_info['name']
        
        return None
    
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        return None
    except Exception as e:
        print(f"Error checking TXT records for {domain}: {str(e)}")
        return None

def is_protected_by_security_system(domain):
    """
    Check if a domain is protected by any known security system
    
    Args:
        domain (str): The email domain to check
        
    Returns:
        tuple: (is_protected, security_system_name)
    """
    # Check MX records first
    security_system = detect_security_system_from_mx(domain)
    if security_system:
        return True, security_system
    
    # Check TXT records next
    security_system = detect_security_system_from_txt(domain)
    if security_system:
        return True, security_system
    
    return False, None

def get_security_pattern_list():
    """Get a flattened list of all security patterns"""
    all_patterns = []
    for system_id, system_info in SECURITY_SYSTEMS.items():
        all_patterns.extend([
            {'pattern': pattern, 'system': system_info['name']} 
            for pattern in system_info.get('patterns', [])
        ])
    return all_patterns
