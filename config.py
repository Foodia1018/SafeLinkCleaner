"""
Configuration settings for the SafeLink Protection Cleaner application
"""

# Email security systems to detect
SECURITY_SYSTEMS = {
    "microsoft_safelinks": {
        "name": "Microsoft Safe Links",
        "patterns": ["safelinks.protection.outlook.com"],
        "mx_patterns": ["protection.outlook.com"]
    },
    "proofpoint": {
        "name": "Proofpoint URL Defense",
        "patterns": ["urldefense.proofpoint.com", "urldefense.com"],
        "mx_patterns": ["pphosted.com", "ppe-hosted.com"]
    },
    "barracuda": {
        "name": "Barracuda Sentinel",
        "patterns": ["linkprotect.cudasvc.com"],
        "mx_patterns": ["barracudanetworks.com", "cudamail.com"]
    },
    "mimecast": {
        "name": "Mimecast",
        "patterns": ["protect-us.mimecast.com", "mimecast.com"],
        "mx_patterns": ["mimecast.com", "mimecast-offshore.com"]
    },
    "cisco_ironport": {
        "name": "Cisco IronPort",
        "patterns": ["cisco.com", "ironport.com"],
        "mx_patterns": ["ironport.com", "esa.com"]
    },
    "mcafee": {
        "name": "McAfee",
        "patterns": ["mcafee.com", "scl.secure.mcafee"],
        "mx_patterns": ["mcafeesaas.com"]
    },
    "symantec": {
        "name": "Symantec",
        "patterns": ["symantec", "messagelabs"],
        "mx_patterns": ["messagelabs.com", "symanteccloud.com"]
    },
    "sophos": {
        "name": "Sophos",
        "patterns": ["sophos", "sophosxl"],
        "mx_patterns": ["sophos.com", "reflexion.net"]
    },
    "trend_micro": {
        "name": "Trend Micro",
        "patterns": ["trendmicro", "emea.trendmicro"],
        "mx_patterns": ["trendmicro.com", "trendmicro.eu"]
    },
    "fireeye": {
        "name": "FireEye",
        "patterns": ["fireeye"],
        "mx_patterns": ["fireeyecloud.com", "fireeye.com"]
    },
    "forcepoint": {
        "name": "Forcepoint",
        "patterns": ["forcepoint", "websense"],
        "mx_patterns": ["forcepoint.com", "websense.com"]
    },
    "sonicwall": {
        "name": "SonicWall",
        "patterns": ["sonicwall"],
        "mx_patterns": ["sonicwall.com", "sonicwallcloud.com"]
    },
    "eop": {
        "name": "Exchange Online Protection",
        "patterns": ["protection.outlook.com"],
        "mx_patterns": ["protection.outlook.com", "mail.protection.outlook.com"]
    },
    "cloudmark": {
        "name": "Cloudmark",
        "patterns": ["cloudmark"],
        "mx_patterns": ["cloudmark.com", "cloudmarkhosted.com"]
    },
    "perception_point": {
        "name": "Perception Point",
        "patterns": ["perception-point"],
        "mx_patterns": ["perception-point.io"]
    },
    "avanan": {
        "name": "Avanan Security",
        "patterns": ["avanan"],
        "mx_patterns": ["avanan.net", "avanan.com"]
    }
}

# Disposable email domains to filter
DISPOSABLE_EMAIL_DOMAINS = [
    "mailinator.com", "yopmail.com", "tempmail.com", "10minutemail.com", 
    "guerrillamail.com", "sharklasers.com", "getairmail.com", "trashmail.com",
    "temp-mail.org", "throwawaymail.com", "fakeinbox.com", "dispostable.com"
]

# Batch size for processing
BATCH_SIZE = 100

# Maximum threads for concurrent processing
MAX_THREADS = 10

# DNS Timeout in seconds
DNS_TIMEOUT = 5

# API rate limits
API_RATE_LIMIT = 100  # requests per minute

# File size limits
MAX_FILE_SIZE_MB = 10

# Supported file formats
SUPPORTED_FORMATS = ["csv", "txt", "xlsx", "json"]

# Export formats
EXPORT_FORMATS = ["csv", "json", "xlsx"]

# Cache settings
CACHE_TIMEOUT = 3600  # seconds

# Valid email regex pattern
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
