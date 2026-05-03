# GymFlow

Smart gym management software for 2-branch fitness centers.

## Tech Stack
- **Backend**: Django 5.x
- **Database**: Neon Postgres (free)
- **Hosting**: Railway (free)
- **Files**: Cloudinary (free)
- **Static**: WhiteNoise

---

## Local Setup

### 1. Clone and create virtual environment
```bash
git clone <your-repo>
cd gymflow
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your Neon and Cloudinary credentials
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (owner account)
```bash
python manage.py createsuperuser
```

### 6. Set up branches via admin
```bash
python manage.py runserver
# Go to /admin → Branches → Add your 2 branches
# Go to /admin → Users → Set your user role to 'owner'
```

### 7. Run the app
```bash
python manage.py runserver
# Visit http://localhost:8000
```

---

## Railway Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial GymFlow setup"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. Connect to Railway
- Go to [railway.app](https://railway.app)
- New Project → Deploy from GitHub repo
- Add environment variables from `.env.example`

### 3. Run migrations on Railway
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### 4. Cron job (auto archive)
Railway automatically picks up the cron job from `railway.toml`.
It runs every night at midnight IST:
```
python manage.py archive_members
```

To test manually:
```bash
python manage.py archive_members
```

---

## Neon Setup
1. Go to [neon.tech](https://neon.tech) → New Project
2. Copy the connection string
3. Fill in `DB_*` values in `.env`

## Cloudinary Setup
1. Go to [cloudinary.com](https://cloudinary.com) → Dashboard
2. Copy Cloud Name, API Key, API Secret
3. Fill in `CLOUDINARY_*` values in `.env`

---

## Project Structure
```
gymflow/
├── accounts/        # Auth, user roles (Owner/Manager/Staff/Trainer)
├── branches/        # Branch model (Branch 1, Branch 2)
├── members/         # Member CRUD, bulk upload, auto archive
│   └── management/commands/archive_members.py
├── enquiries/       # Lead capture → convert to member
├── plans/           # Membership plan management
├── payments/        # Payments, invoices, PDF generation
├── reports/         # Revenue, expiry, pending reports + Excel export
├── templates/       # All HTML templates
├── static/          # CSS, JS
├── railway.toml     # Railway deployment + cron config
├── Procfile         # Gunicorn start command
└── requirements.txt
```

---

## Adding WhatsApp (Future)
When ready to add Interakt:
1. `mkdir notifications && python manage.py startapp notifications`
2. Add to `INSTALLED_APPS`
3. Add Interakt API key to `.env`
4. Create webhook endpoint in `notifications/views.py`
5. Trigger messages from `members/views.py` on payment/expiry events
