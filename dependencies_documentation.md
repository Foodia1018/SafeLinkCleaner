# SafeLink Protection Cleaner - Dependencies Documentation

## Core Dependencies

### Web Framework Components

#### Flask & Extensions
- **flask**: Web application framework
  - Used for routing, templating, and request handling
  - Key imports: `Flask`, `render_template`, `request`, `jsonify`, `redirect`, `url_for`, `flash`
- **flask-sqlalchemy**: Flask extension for SQLAlchemy
  - Provides integration between Flask and SQLAlchemy ORM
  - Key imports: `SQLAlchemy`
- **werkzeug**: WSGI utility library for web applications
  - Used for security features and utilities
  - Key imports: `secure_filename`
- **jinja2**: Template engine
  - Used for rendering HTML templates
- **itsdangerous**: Cryptographic signing tools
  - Used for securely signing data like session cookies

#### Database
- **sqlalchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
  - Used for database models and queries
  - Key imports: `DeclarativeBase`
- **psycopg2-binary**: PostgreSQL adapter for Python
  - Enables connection to PostgreSQL databases
- **greenlet**: Lightweight coroutines for in-process concurrent programming
  - Required by SQLAlchemy for async features

### Data Processing
- **pandas**: Data manipulation and analysis library
  - Used for processing CSV and Excel files
  - Key imports: `pd.read_csv`, `pd.read_excel`, `DataFrame`
- **numpy**: Numerical computing library
  - Used for efficient array operations
  - Often imported as `np`
- **openpyxl**: Excel file manipulation
  - Used for reading/writing Excel files
  - Required by pandas for Excel support

### Email & Domain Validation
- **dnspython**: DNS toolkit
  - Used for MX record validation of email domains
  - Key imports: `dns.resolver`
- **email-validator**: Email validation library
  - Used for email syntax checking

### Asynchronous Processing
- **asyncio**: Asynchronous I/O framework
  - Used for concurrent processing of email lists
  - Key imports: `asyncio.to_thread`, `asyncio.gather`

### Server Deployment
- **gunicorn**: WSGI HTTP server
  - Used to serve the Flask application
  - The application is configured to run with Gunicorn

### Configuration
- **python-dotenv**: Environment variable management
  - Used to load configuration from .env files

## Implementation Notes

### Database Models
- The application uses SQLAlchemy models for data persistence
- Main models: `EmailList`, `Email`, `SecurityStats`, `ProcessingJob`
- PostgreSQL is used as the database backend

### Asynchronous Processing
- Email processing is done asynchronously using Python's asyncio
- This allows for concurrent handling of DNS lookups and validations

### Security System Detection
- The application detects email protection systems through DNS analysis
- Uses pattern matching to identify security gateways

### File Handling
- Supports CSV, TXT, and XLSX file formats for email lists
- Uses pandas for efficient data extraction

## Environment Dependencies
- Python 3.11
- PostgreSQL database
