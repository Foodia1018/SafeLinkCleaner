# SafeLink Protection Cleaner - Dependencies List

## Core Dependencies

### Web Framework
- flask
- flask-sqlalchemy
- gunicorn
- werkzeug
- itsdangerous
- jinja2
- markupsafe
- blinker
- click

### Database
- psycopg2-binary
- sqlalchemy
- greenlet

### Data Processing
- pandas
- numpy
- python-dateutil
- pytz
- tzdata

### Email Validation & DNS
- dnspython
- email-validator
- idna

### File Processing
- openpyxl
- et-xmlfile

### Asynchronous Processing
- asyncio

### Environment & Configuration
- python-dotenv

## Development & Testing Dependencies

### Testing
- pytest (for testing)

### Type Checking
- typing-extensions

## Already Installed Dependencies

The following packages are already installed in our environment according to the output of `pip list`:

```
- asyncio==3.4.3
- blinker==1.9.0
- click==8.1.8
- dnspython==2.7.0
- email-validator==2.2.0
- et-xmlfile==2.0.0
- flask-sqlalchemy==3.1.1
- flask==3.1.0
- greenlet==3.2.1
- gunicorn==23.0.0
- idna==3.10
- itsdangerous==2.2.0
- jinja2==3.1.6
- markupsafe==3.0.2
- numpy==2.2.5
- openpyxl==3.1.5
- pandas==2.2.3
- psycopg2-binary==2.9.10
- python-dateutil==2.9.0.post0
- python-dotenv==1.1.0
- pytz==2025.2
- sqlalchemy==2.0.40
- typing-extensions==4.13.2
- tzdata==2025.2
- werkzeug==3.1.3
```

## Install Command

To install the required dependencies using pip:

```
pip install flask flask-sqlalchemy gunicorn psycopg2-binary pandas numpy dnspython email-validator asyncio openpyxl python-dotenv
```

Or using the Replit packager tool:

```python
packager_tool install python flask flask-sqlalchemy gunicorn psycopg2-binary pandas numpy dnspython email-validator asyncio openpyxl python-dotenv
```

## Notes

- The application's core functionality depends on database access, email validation, and CSV/Excel file processing.
- We use PostgreSQL as the database backend through psycopg2-binary.
- Flask and SQLAlchemy provide the web framework and ORM capabilities.
- Pandas and NumPy are used for data processing tasks related to email lists.
- DNSPython is crucial for DNS lookups during email domain validation.
