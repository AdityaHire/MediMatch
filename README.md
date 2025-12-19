# MediMatch - Medicine Recommendation System

An intelligent medicine recommendation system that helps users find appropriate over-the-counter medications based on their symptoms using machine learning.

## Features

- 🤖 AI-powered medicine recommendations
- 🌐 Multi-language support (English & Hindi)
- 📊 Personalized recommendations based on age, gender, and medical history
- 📜 Query history tracking
- 🎨 Modern, responsive UI with Bootstrap 5

## Technologies Used

- **Backend:** Django 5.0
- **Machine Learning:** scikit-learn, pandas, numpy
- **Translation:** deep-translator
- **Frontend:** Bootstrap 5, Font Awesome
- **Database:** SQLite (development), PostgreSQL (production-ready)

## Installation

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AdityaHire/MediMatch.git
cd MediMatch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Compile translations:
```bash
python compile_translations.py
```

8. Collect static files:
```bash
python manage.py collectstatic --noinput
```

9. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## Deployment

### Heroku

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

4. Deploy:
```bash
git push heroku main
```

5. Run migrations:
```bash
heroku run python manage.py migrate
```

### Other Platforms

The project includes:
- `Procfile` for Heroku
- `runtime.txt` for Python version
- `requirements.txt` for dependencies
- WhiteNoise for static file serving

Compatible with: Heroku, Render, Railway, PythonAnywhere, and other PaaS platforms.

## Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Debug mode (False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Usage

1. Navigate to "Get Recommendation" page
2. Enter your symptoms
3. Provide age, gender, and medical history
4. Select language preference (English/Hindi)
5. Get personalized medicine recommendations
6. View recommendation history

## Project Structure

```
MediMatch/
├── medicine_project/      # Django project settings
├── recommendation/        # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Forms
│   ├── ml_model.py       # ML recommendation engine
│   └── urls.py           # URL routing
├── templates/            # HTML templates
├── static/              # Static files (CSS, images)
├── locale/              # Translation files
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment
└── runtime.txt         # Python version
```

## Important Notes

⚠️ **Medical Disclaimer:** This system is for informational purposes only and should not replace professional medical advice. Always consult with a healthcare provider before taking any medication.

## Developer

**Aditya Hire**

- 📧 Email: adityahire08@gmail.com
- 💼 LinkedIn: [linkedin.com/in/aditya-hire-2a0974357](https://www.linkedin.com/in/aditya-hire-2a0974357)
- 🐙 GitHub: [github.com/adityahire08](https://github.com/adityahire08)
- 🌐 Portfolio: [adityahire.github.io/myportfolio](https://adityahire.github.io/myportfolio/)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome!

## Support

If you like this project, please give it a ⭐️ on GitHub!
