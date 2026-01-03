# Quick Setup Guide

## Step-by-Step Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup

**For SQLite (Default - Recommended for testing):**
- No additional setup needed. Just proceed to migrations.

**For MariaDB/MySQL:**
1. Install MariaDB/MySQL server
2. Create database:
   ```sql
   CREATE DATABASE ecommerce_db;
   ```
3. Edit `ecommerce_project/settings.py`:
   - Comment out SQLite database config
   - Uncomment and configure MySQL/MariaDB config with your credentials
4. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
This allows you to access the Django admin panel at `/admin/`

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Access the Application
- Open browser: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Testing the Application

### As a Vendor:
1. Go to Register → As Vendor
2. Create an account
3. Log in
4. Create a store
5. Add products to your store

### As a Buyer:
1. Go to Register → As Buyer
2. Create an account
3. Log in
4. Browse products
5. Add items to cart
6. Checkout (invoice will be sent to email - check console in development)

## Email Configuration

### Development (Default):
Emails are printed to the console. Check your terminal when:
- Password reset is requested
- Order is placed (invoice email)

### Production:
Edit `ecommerce_project/settings.py` and configure SMTP settings:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## Troubleshooting

### Database Errors:
- Make sure migrations are run: `python manage.py migrate`
- For MySQL/MariaDB: Ensure database exists and credentials are correct

### Import Errors:
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Template Errors:
- Ensure `templates` directory exists in project root
- Check that `TEMPLATES` setting in `settings.py` includes the templates directory

### Permission Errors:
- Make sure you're logged in with the correct role (vendor/buyer)
- Check that you own the resource you're trying to edit/delete

## Next Steps

1. Review the planning documents in `Planning/` folder
2. Test all functionality as both vendor and buyer
3. Configure email for production use
4. Set up proper database for production
5. Change SECRET_KEY and set DEBUG=False for production


