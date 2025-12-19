# Medicine Recommendation System

An AI-powered medicine recommendation system built with Django, Machine Learning, HTML, CSS, and Bootstrap.

## Features

- **AI-Powered Recommendations**: Uses TF-IDF and Cosine Similarity for accurate medicine suggestions
- **User-Friendly Interface**: Clean and responsive design with Bootstrap 5
- **Comprehensive Information**: Detailed medicine info including usage, side effects, and precautions
- **Query History**: Track past recommendations
- **Responsive Design**: Works seamlessly on all devices

## Technology Stack

### Backend
- Django 5.0
- Python 3.x
- scikit-learn (Machine Learning)
- pandas & numpy (Data Processing)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Font Awesome Icons

## Installation Guide

### Step 1: Clone or Navigate to the Project
```bash
cd c:\Users\adity\OneDrive\Desktop\hggg
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional - for Admin Panel)
```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```

### Step 8: Access the Application
Open your browser and visit:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Project Structure

```
hggg/
├── manage.py
├── requirements.txt
├── README.md
├── medicine_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── recommendation/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── ml_model.py
├── templates/
│   ├── base.html
│   └── recommendation/
│       ├── home.html
│       ├── recommend.html
│       ├── results.html
│       ├── about.html
│       └── history.html
└── static/
    └── css/
        └── style.css
```

## How It Works

1. **User Input**: Patient enters symptoms, age, gender, and medical history
2. **Text Processing**: System processes the input using NLP techniques
3. **ML Analysis**: TF-IDF vectorization and cosine similarity matching
4. **Recommendations**: Top matching medicines with detailed information
5. **Results Display**: Comprehensive medicine information with usage instructions

## Machine Learning Model

The system uses:
- **TF-IDF Vectorization**: Converts symptoms into numerical vectors
- **Cosine Similarity**: Measures similarity between symptoms and medicine profiles
- **Content-Based Filtering**: Recommends medicines based on symptom matching

## Features Explained

### 1. Home Page
- Introduction to the system
- Feature highlights
- Call-to-action buttons

### 2. Recommendation Page
- Symptom input form
- Patient information collection
- Form validation

### 3. Results Page
- Top medicine recommendations
- Similarity scores
- Detailed medicine information
- Usage instructions and precautions

### 4. History Page
- Past query records
- Previous recommendations
- Query timestamps

### 5. About Page
- System information
- Technology stack details
- ML model explanation

## Important Notes

⚠️ **Medical Disclaimer**: This system is for educational and informational purposes only. Always consult a qualified healthcare professional before taking any medication.

## Customization

### Adding More Medicines
Edit the `_load_medicine_data()` method in `recommendation/ml_model.py` to add more medicines to the database.

### Modifying Styles
Edit `static/css/style.css` to customize the appearance.

### Changing ML Model
You can enhance the ML model in `recommendation/ml_model.py` by:
- Adding more sophisticated algorithms
- Implementing deep learning models
- Integrating external medical APIs

## Troubleshooting

### Issue: Module not found
**Solution**: Make sure you've activated the virtual environment and installed all requirements.

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and ensure `DEBUG = True` in development.

### Issue: Database errors
**Solution**: Delete `db.sqlite3` and run migrations again.

## Future Enhancements

- User authentication system
- Export recommendations as PDF
- Integration with pharmacy APIs
- Multi-language support
- Advanced ML models (Neural Networks)
- Drug interaction warnings
- Dosage calculator

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is for educational purposes.

## Contact

For questions or feedback, please reach out through the application's contact form.

---

**Built with ❤️ using Django and Machine Learning**
