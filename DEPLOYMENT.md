# AI LogoMaker Deployment Guide
## Created by Hiren Patel

### Quick Start (Development)

1. **Navigate to project directory:**
   ```bash
   cd logomaker
   ```

2. **Run setup script:**
   ```bash
   setup.bat
   ```

3. **Start the server:**
   ```bash
   run_server.bat
   ```

4. **Access the application:**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin (admin/admin123)

### Manual Setup

1. **Install basic dependencies:**
   ```bash
   pip install -r requirements_basic.txt
   ```

2. **Database setup:**
   ```bash
   py manage.py makemigrations
   py manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   py manage.py createsuperuser
   ```

4. **Setup demo data:**
   ```bash
   py manage.py setup_demo
   ```

5. **Run development server:**
   ```bash
   py manage.py runserver
   ```

### Production Deployment

1. **Install full dependencies:**
   ```bash
   pip install -r requirements_full.txt
   ```

2. **Environment variables:**
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   ```

3. **Database (PostgreSQL):**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'logomaker_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Static files:**
   ```bash
   py manage.py collectstatic
   ```

5. **Run with Gunicorn:**
   ```bash
   gunicorn logomaker.wsgi:application
   ```

### Features Available

✅ **Core Features:**
- AI Logo Generation (7 styles)
- User Authentication
- Mobile Responsive Design
- Admin Panel
- Logo Gallery
- Download System

✅ **AI Algorithms:**
- Modern Style Generator
- Vintage Style Generator
- Minimalist Style Generator
- Corporate Style Generator
- Creative Style Generator
- Tech Style Generator
- Elegant Style Generator

✅ **Mobile Features:**
- Touch-friendly interface
- Responsive design
- Mobile-optimized forms
- Progressive Web App ready

### File Structure

```
logomaker/
├── logomaker/              # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── logo_generator/         # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URLs
│   ├── admin.py           # Admin configuration
│   └── ai_generator.py    # AI logo generation
├── templates/              # HTML templates
│   ├── logo_generator/    # App templates
│   └── registration/      # Auth templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript
├── media/                  # Generated logos
├── requirements_basic.txt  # Basic dependencies
├── requirements_full.txt   # Full dependencies
├── setup.bat              # Setup script
├── run_server.bat         # Run script
└── README.md              # Documentation
```

### Default Credentials

- **Admin:** admin / admin123
- **Demo User:** demo / demo123

### API Endpoints

- `/` - Home page
- `/generate/` - Logo generation
- `/gallery/` - Logo gallery
- `/profile/` - User profile
- `/about/` - About page
- `/admin/` - Admin panel

### Troubleshooting

**Common Issues:**

1. **Module not found errors:**
   ```bash
   pip install -r requirements_basic.txt
   ```

2. **Database errors:**
   ```bash
   py manage.py migrate
   ```

3. **Static files not loading:**
   ```bash
   py manage.py collectstatic
   ```

4. **Permission errors:**
   - Check file permissions
   - Run as administrator if needed

### Performance Tips

1. **Enable caching in production**
2. **Use CDN for static files**
3. **Optimize database queries**
4. **Enable compression**
5. **Use Redis for sessions**

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Regular security updates
- [ ] Backup database regularly

### Support

For technical support:
- Check README.md for detailed information
- Review Django documentation
- Contact: Hiren Patel

---
**Created with ❤️ by Hiren Patel**