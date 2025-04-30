"""
Machine learning classifier for SafeLink Protection Cleaner.
Provides ML-enhanced pattern detection for security systems.
"""
import re
import logging
from collections import Counter

logger = logging.getLogger(__name__)

# Security system pattern storage with initial weights
security_patterns = {
    "microsoft_safelinks": {
        "patterns": [
            {"regex": r"safelinks\.protection\.outlook\.com", "weight": 0.9},
            {"regex": r"na\d+\.safelinks\.protection\.outlook\.com", "weight": 0.95}
        ],
        "mx_patterns": [
            {"regex": r".*\.protection\.outlook\.com", "weight": 0.8}
        ],
        "threshold": 0.7
    },
    "proofpoint": {
        "patterns": [
            {"regex": r"urldefense\.proofpoint\.com", "weight": 0.9},
            {"regex": r"urldefense\.com", "weight": 0.85}
        ],
        "mx_patterns": [
            {"regex": r".*\.pphosted\.com", "weight": 0.8},
            {"regex": r".*\.ppe-hosted\.com", "weight": 0.8}
        ],
        "threshold": 0.7
    }
    # Other security systems would be defined similarly
}

# Feature extraction for ML classification
def extract_features(domain, mx_records, txt_records):
    """
    Extract features from domain data for classification
    
    Args:
        domain (str): Email domain
        mx_records (list): List of MX records
        txt_records (list): List of TXT records
        
    Returns:
        dict: Features extracted from the domain data
    """
    features = {
        "domain_length": len(domain),
        "has_mx": len(mx_records) > 0,
        "mx_count": len(mx_records),
        "has_txt": len(txt_records) > 0,
        "txt_count": len(txt_records),
        "has_spf": any("v=spf1" in txt for txt in txt_records),
        "has_dkim": any("v=dkim1" in txt for txt in txt_records),
        "has_dmarc": any("v=dmarc1" in txt for txt in txt_records),
        "security_keywords": 0
    }
    
    # Count security keywords in records
    keywords = ["protection", "security", "secure", "defense", "scan", "filter", "gateway"]
    for record in mx_records + txt_records:
        for keyword in keywords:
            if keyword.lower() in record.lower():
                features["security_keywords"] += 1
    
    return features

def predict_security_system(features, domain, mx_records, txt_records):
    """
    Predict which security system is protecting the domain
    
    Args:
        features (dict): Domain features
        domain (str): Email domain
        mx_records (list): List of MX records
        txt_records (list): List of TXT records
        
    Returns:
        tuple: (security_system_name, confidence_score)
    """
    scores = {}
    
    # Calculate scores for each security system
    for system_id, system_info in security_patterns.items():
        score = 0
        total_weight = 0
        
        # Check domain patterns
        for pattern in system_info["patterns"]:
            regex = re.compile(pattern["regex"], re.IGNORECASE)
            weight = pattern["weight"]
            total_weight += weight
            
            if any(regex.search(record) for record in mx_records + txt_records + [domain]):
                score += weight
        
        # Calculate normalized score
        if total_weight > 0:
            normalized_score = score / total_weight
            scores[system_id] = normalized_score
    
    # Get the highest scoring system
    if scores:
        best_system = max(scores.items(), key=lambda x: x[1])
        system_id, confidence = best_system
        
        # Check if the confidence meets the threshold
        if confidence >= security_patterns[system_id]["threshold"]:
            return system_id, confidence
    
    return None, 0.0

def update_pattern_weights(training_data):
    """
    Update pattern weights based on training data
    
    Args:
        training_data (list): List of training examples with known labels
        
    Returns:
        bool: True if weights were updated successfully
    """
    # This would be implemented for a full ML system
    # For now, this is a placeholder
    logger.info("Pattern weights update called")
    return True

class SecuritySystemClassifier:
    """Machine learning classifier for security systems"""
    
    def __init__(self):
        """Initialize the classifier with default patterns"""
        self.patterns = security_patterns
    
    def predict(self, domain, mx_records, txt_records):
        """
        Predict security system for a domain
        
        Args:
            domain (str): Email domain
            mx_records (list): List of MX records
            txt_records (list): List of TXT records
            
        Returns:
            tuple: (security_system_name, confidence_score)
        """
        features = extract_features(domain, mx_records, txt_records)
        return predict_security_system(features, domain, mx_records, txt_records)
    
    def train(self, training_data):
        """
        Train the classifier with new data
        
        Args:
            training_data (list): List of training examples with known labels
            
        Returns:
            bool: True if training was successful
        """
        return update_pattern_weights(training_data)
