# 🔐 OpenSesame SSO

> *"Open Sesame"* - The magical phrase that opens doors. A secure, enterprise-grade Single Sign-On (SSO) solution built with Django.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)
![Security](https://img.shields.io/badge/security-enterprise--grade-red.svg)

## 🎯 What's New

- ✨ **Passwordless Authentication (PLA)**: Login with just your email - no password needed!
- 📧 **Email Verification Codes**: Secure 6-digit one-time codes delivered via email
- 🎨 **Beautiful UI Templates**: Modern, animated login pages with smooth transitions
- 🛠️ **Management Commands**: Quick setup with CLI tools for service providers
- 📱 **Dual Authentication**: Choose between password-based or passwordless login

## ✨ Features

### 🛡️ **Security First**
- **Individual Service Secrets**: Each service provider gets a unique, encrypted secret key for JWT validation
- **Multi-Factor Authentication (MFA)**: TOTP-based 2FA support
- **Passwordless Authentication (PLA)**: Email-based one-time code authentication
- **Google reCAPTCHA Integration**: Bot protection on all authentication endpoints
- **Encrypted Secret Storage**: Service secrets encrypted at rest using AES encryption
- **JWT Security**: Short-lived access tokens with secure refresh mechanisms
- **Rate Limiting**: Protection against brute force attacks
- **CSRF Protection**: Built-in Django CSRF protection for all forms

### 🚀 **Enterprise Ready**
- **Multi-Service Support**: Unlimited service provider registrations
- **Custom Claims**: Define required user claims per service
- **Audit Logging**: Complete authentication and authorization logs
- **Admin Dashboard**: Django admin interface for service management
- **RESTful API**: Clean API endpoints for service integration
- **Scalable Architecture**: Built for high-traffic environments

### 👤 **User Experience**
- **Single Sign-On**: One login for all connected services
- **Multiple Authentication Methods**: Choose between password-based or passwordless login
- **Passwordless Login**: No password needed - just enter your email and verify with a code
- **User Profile Management**: Comprehensive user profiles with customizable fields
- **Email Verification**: Secure email verification workflow
- **Password Reset**: Secure password recovery with email tokens
- **Beautiful UI**: Modern, responsive templates with smooth animations
- **Mobile Responsive**: Works seamlessly across all devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web App A     │    │   Web App B     │    │   Web App C     │
│                 │    │                 │    │                 │
│ Secret Key: A   │    │ Secret Key: B   │    │ Secret Key: C   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     OpenSesame SSO        │
                    │                           │
                    │  🔐 Encrypted Secrets     │
                    │  🎯 JWT Generation        │
                    │  🤖 reCAPTCHA Protection  │
                    │  🔑 MFA Support           │
                    │  📧 Passwordless Auth     │
                    │                           │
                    └───────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Email Service        │
                    │  (OTP Code Delivery)    │
                    └─────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Django 5+
- PostgreSQL/MySQL (recommended for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Xeroxxhah/opensesame.git
   cd opensesame
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Create a test service provider**
   ```bash
   python manage.py create_test_service
   ```

8. **Link user to service**
   ```bash
   python manage.py add_user_to_service --email your-email@example.com
   ```

## 🛠️ Management Commands

### Create Test Service Provider
```bash
python manage.py create_test_service [--name "Service Name"] [--redirect-url "http://..."]
```
Creates a service provider for development/testing.

### Add User to Service
```bash
python manage.py add_user_to_service --email user@example.com [--service-id uuid]
```
Links a user account to a service provider.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-django-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/opensesame_db

# Email Configuration (Required for Passwordless Auth)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Google reCAPTCHA
ENABLE_RECAPTCHA=True
RECAPTCHA_SITE_KEY=your-recaptcha-site-key
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key

# JWT Settings
ACCESS_JWT_TIMEOUT=1440  # minutes
REFRESH_JWT_TIMEOUT=2880  # minutes

# Passwordless Authentication (PLA)
PLA_CODE_EXP=5  # Code expiration in minutes
PLA_MAX_ATTEMPTS=3  # Maximum verification attempts

# Encryption
ENCRYPTION_KEY=your-32-byte-encryption-key

# Company Info (for email templates)
COMP_CONF = {
    "name": "Your Company",
    "website": "https://yourwebsite.com",
    "linkedin": "https://linkedin.com/company/yourcompany"
}

```

### Google reCAPTCHA Setup

1. Visit [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
2. Create a new site
3. Choose reCAPTCHA v2 "I'm not a robot"
4. Add your domain
5. Copy the Site Key and Secret Key to your `.env` file

### Email Configuration for Passwordless Auth

OpenSesame supports multiple email providers for sending verification codes:

**Gmail**:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password
```

**Hostinger**:
```python
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

**SendGrid**:
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

**Custom Email Template**:
Edit `auth_provider/templates/email/otp_email.html` to customize the verification email design.

## 🔧 Service Provider Integration

### 1. Register Your Service

Access the Django admin panel at `/admin/` and create a new Service Provider:

- **Service Name**: Your application name
- **Redirect URL**: Where users return after authentication
- **Claims Required**: Define what user data you need

### 2. Get Your Secret Key

After saving, your unique secret key will be generated and displayed. **Keep this secure!**

### 3. Integration Example

```python
from flask import Flask, request, jsonify
import jwt
import json
app = Flask(__name__)

SECRET_KEY = "Service Provider Key"  # Same as used by SSO server
last_token = None  # Just for demo storage

@app.route("/sso/callback", methods=["POST", "GET"])
def sso_callback():
    global last_token

    if request.method == "POST":
        tokens = request.form.get("tokens")

        json_tokens = json.loads(tokens) 
        access_token = json_tokens.get('access')
        print(f"[POST] Received tokens: {tokens}")

        # Verify JWT
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            print("Decoded JWT payload:", payload)
        except jwt.PyJWTError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        return jsonify({"status": "ok", "message": "Token received"})

    else:  # GET request (browser redirect after server POST)
        if not last_token:
            return "No token received yet", 400

        return f"""
        <html>
          <body>
            <h2>SSO Complete</h2>
            <p>Token: {last_token}</p>
          </body>
        </html>
        """


if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

### 4. Authentication Flow

#### Password-Based Authentication
```
1. User visits your app → Redirect to OpenSesame login page
2. User enters email/password (+ MFA if enabled)
3. OpenSesame validates credentials (including CAPTCHA if needed)
4. OpenSesame generates JWT with your service's secret
5. User redirected back with JWT token via POST
6. Your app verifies JWT using your secret key
7. Grant access to authenticated user
```

#### Passwordless Authentication (PLA)
```
1. User visits your app → Redirect to OpenSesame PLA login page
2. User enters email address
3. OpenSesame sends 6-digit code via email
4. User enters verification code
5. OpenSesame validates code
6. OpenSesame generates JWT with your service's secret
7. User redirected back with JWT token via POST
8. Your app verifies JWT using your secret key
9. Grant access to authenticated user
```

## 🔒 Security Features

### JWT Security
- **Service-Specific Secrets**: Each service has its own secret key for JWT signing
- **Short-Lived Tokens**: Access tokens expire in 15 minutes by default
- **Refresh Token Rotation**: Secure token refresh mechanism
- **Algorithm Specification**: Uses HS256 algorithm for signing

### Data Protection
- **Encrypted Storage**: Service secrets encrypted at rest
- **Password Hashing**: PBKDF2 with SHA256 (Django default)
- **CSRF Protection**: All forms protected against CSRF attacks
- **SQL Injection Prevention**: Django ORM prevents SQL injection

### Authentication Security
- **Multi-Factor Authentication**: TOTP-based 2FA support
- **Passwordless Authentication**:
  - Time-limited verification codes (5 minutes default)
  - Maximum attempt limiting (3 attempts default)
  - One-time use codes
  - SHA-256 hashed code storage
- **reCAPTCHA Integration**: Prevents automated attacks
- **Rate Limiting**: Protection against brute force attempts
- **Email Verification**: Ensures email ownership
- **Account Lockout**: Temporary lockout after failed attempts

## 📊 API Documentation

### Authentication Endpoints

#### Standard Login (Password-Based)
```http
POST /api/v1/auth/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword",
  "mfa_token": "123456",  // Optional: Required if MFA is enabled
  "g-recaptcha-response": "recaptcha-token",  // Optional: If reCAPTCHA is enabled
  "service_id": "uuid-of-requesting-service"
}

Response:
Returns HTML page that auto-submits to service provider callback URL with JWT tokens
```

#### Check MFA Status
```http
POST /api/v1/mfa-status/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "securepassword",
  "service_id": "uuid-of-requesting-service"
}

Response:
{
  "mfa_required": true/false
}
```

#### Passwordless Login - Send Code
```http
POST /api/v1/pla/send-code/
Content-Type: application/json

{
  "username": "user@example.com",
  "service_id": "uuid-of-requesting-service",
  "g-recaptcha-response": "recaptcha-token"  // Optional: If reCAPTCHA is enabled
}

Response:
{
  "success": true,
  "message": "Verification code sent to your email"
}
```

#### Passwordless Login - Verify Code
```http
POST /api/v1/pla/auth/
Content-Type: application/json

{
  "username": "user@example.com",
  "code": "123456",
  "service_id": "uuid-of-requesting-service"
}

Response:
Returns HTML page that auto-submits to service provider callback URL with JWT tokens
```

#### Token Refresh
```http
POST /api/v1/refresh-token/
Content-Type: application/json

{
  "refresh_token": "your-refresh-token",
  "service_id": "uuid-of-requesting-service"
}

Response:
{
  "access": "new-access-token",
  "refresh": "new-refresh-token"
}
```

### Web Login Pages

#### Standard Login Page
```
GET /web.sso/login/?service_id={your-service-id}
```
- Username/password authentication
- Optional MFA support
- Link to passwordless login
- reCAPTCHA integration

#### Passwordless Login Page
```
GET /web.sso/pla-login/?service_id={your-service-id}
```
- Email-based authentication
- Two-step verification process
- Code resend functionality
- Link to password-based login

## 🧪 Testing

### Testing Passwordless Authentication

1. **Start the test service provider**:
   ```bash
   python test_service_provider.py
   ```
   This starts a Flask app on port 5000 that receives SSO callbacks.

2. **Get your service ID**:
   ```bash
   python manage.py create_test_service
   ```
   Note the Service ID from the output.

3. **Link your user**:
   ```bash
   python manage.py add_user_to_service --email your-email@example.com
   ```

4. **Test the flow**:
   - Visit: `http://127.0.0.1:8000/web.sso/pla-login/?service_id={YOUR-SERVICE-ID}`
   - Enter your email
   - Check your email for the 6-digit code
   - Enter the code
   - You'll be redirected to the Flask app with JWT tokens!

### Run the test suite:

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "opensesame.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure secure database (PostgreSQL recommended)
- [ ] Set up Redis for caching
- [ ] Configure email backend
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up monitoring and logging
- [ ] Regular database backups
- [ ] Security headers configuration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### Commercial Licensing

For commercial use without GPL restrictions, commercial licenses are available. Contact us for more information.

## 🆘 Support

- **Documentation**: [Full Documentation](https://opensesame-sso.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/Xeroxxhah/opensesame/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Xeroxxhah/opensesame/discussions)
- **Security**: Report security issues to security@yourdomain.com

## 🙏 Acknowledgments

- Django team for the amazing framework
- PyJWT for JWT implementation
- Google for reCAPTCHA service
- The open source community

---

**Made with ❤️ for a more secure web**

*OpenSesame - One key to unlock all doors, securely.*
