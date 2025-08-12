# 🔐 OpenSesame SSO

> *"Open Sesame"* - The magical phrase that opens doors. A secure, enterprise-grade Single Sign-On (SSO) solution built with Django.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)
![Security](https://img.shields.io/badge/security-enterprise--grade-red.svg)

## ✨ Features

### 🛡️ **Security First**
- **Individual Service Secrets**: Each service provider gets a unique, encrypted secret key for JWT validation
- **Multi-Factor Authentication (MFA)**: TOTP-based 2FA support
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
- **User Profile Management**: Comprehensive user profiles with customizable fields
- **Email Verification**: Secure email verification workflow
- **Password Reset**: Secure password recovery with email tokens
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
                    │                           │
                    └───────────────────────────┘
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

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google reCAPTCHA
ENABLE_CAPTCHA = True
RECAPTCHA_PUBLIC_KEY=your-recaptcha-site-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-secret-key

# JWT Settings
ACCESS_JWT_TIMEOUT=1440
REFRESH_JWT_TIMEOUT=2880

# Encryption
ENCRYPTION_KEY=your-32-byte-encryption-key

```

### Google reCAPTCHA Setup

1. Visit [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
2. Create a new site
3. Choose reCAPTCHA v2 "I'm not a robot"
4. Add your domain
5. Copy the Site Key and Secret Key to your `.env` file

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

```
1. User visits your app → Redirect to OpenSesame
2. User authenticates → OpenSesame validates (including CAPTCHA if needed)
3. OpenSesame generates JWT with your service's secret
4. User redirected back with JWT token
5. Your app verifies JWT using your secret key
6. Grant access to authenticated user
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
- **reCAPTCHA Integration**: Prevents automated attacks
- **Rate Limiting**: Protection against brute force attempts
- **Email Verification**: Ensures email ownership
- **Account Lockout**: Temporary lockout after failed attempts

## 📊 API Documentation

### Authentication Endpoints

#### Login
```http
POST /api/v1/auth/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "captcha_token": "recaptcha-response-token if enabled and set",
  "service_id": "uuid-of-requesting-service"
  "mfa-code": "MFA code if it is enabled and set"

}
```

#### Token Verification
```http
POST /api/v1/refresh-token/
Authorization: Bearer your-jwt-token

{
  "refresh_token": "refresh token",
  "service_id": "uuid-of-requesting-service"
}
```

## 🧪 Testing

Run the test suite:

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
