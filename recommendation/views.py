# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SymptomForm
from .models import PatientQuery
from .ml_model import get_recommender
import json
from deep_translator import GoogleTranslator


def translate_hindi_symptoms(symptoms):
    """Translate Hindi symptoms to English for ML model using Google Translate"""
    try:
        # Detect if symptoms contain Hindi characters
        if any('\u0900' <= char <= '\u097F' for char in symptoms):
            translator = GoogleTranslator(source='hi', target='en')
            translated = translator.translate(symptoms)
            return translated
        else:
            # Already in English or other language
            return symptoms
    except Exception as e:
        print(f"Symptom translation error: {e}")
        # If translation fails, return original
        return symptoms


def translate_medicine_to_hindi(recommendations, language_code):
    """Translate medicine recommendations to Hindi using Google Translate"""
    if language_code != 'hi':
        return recommendations
    
    translated_recommendations = []
    translator = GoogleTranslator(source='en', target='hi')
    
    for med in recommendations:
        translated_med = med.copy()
        
        try:
            # Translate each text field
            for field in ['description', 'usage', 'side_effects', 'precautions']:
                if field in translated_med and translated_med[field]:
                    # Translate the text
                    translated_text = translator.translate(translated_med[field])
                    translated_med[field] = translated_text
            
            # Keep medicine name in English or provide transliteration
            # Category can be translated
            if 'category' in translated_med:
                translated_med['category'] = translator.translate(translated_med['category'])
                
        except Exception as e:
            # If translation fails, keep original text
            print(f"Translation error: {e}")
            pass
        
        translated_recommendations.append(translated_med)
    
    return translated_recommendations


def home(request):
    """Home page view"""
    return render(request, 'recommendation/home.html')


def about(request):
    """About page view"""
    return render(request, 'recommendation/about.html')


def recommend(request):
    """Medicine recommendation view"""
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            # Get form data
            symptoms = form.cleaned_data['symptoms']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            medical_history = form.cleaned_data['medical_history']
            
            # Translate Hindi symptoms to English for ML model
            translated_symptoms = translate_hindi_symptoms(symptoms)
            
            # Get ML recommendations
            recommender = get_recommender()
            recommendations = recommender.recommend_medicines(
                symptoms=translated_symptoms,
                age=age,
                gender=gender,
                top_n=5
            )
            
            # Save query to database
            query = form.save(commit=False)
            query.recommended_medicines = json.dumps(recommendations)
            query.save()
            
            # Store in session for results page
            request.session['recommendations'] = recommendations
            request.session['patient_info'] = {
                'symptoms': symptoms,
                'age': age,
                'gender': gender,
                'medical_history': medical_history
            }
            
            return redirect('results')
    else:
        form = SymptomForm()
    
    return render(request, 'recommendation/recommend.html', {'form': form})


def results(request):
    """Display recommendation results"""
    recommendations = request.session.get('recommendations', [])
    patient_info = request.session.get('patient_info', {})
    
    if not recommendations:
        messages.warning(request, 'No recommendations found. Please submit your symptoms first.')
        return redirect('recommend')
    
    # Get current language and translate recommendations if Hindi
    from django.utils.translation import get_language
    current_language = get_language()
    translated_recommendations = translate_medicine_to_hindi(recommendations, current_language)
    
    context = {
        'recommendations': translated_recommendations,
        'patient_info': patient_info
    }
    
    return render(request, 'recommendation/results.html', context)


def history(request):
    """View past queries"""
    queries = PatientQuery.objects.all()[:10]  # Last 10 queries
    
    # Parse JSON recommendations for each query
    for query in queries:
        try:
            query.recommendations = json.loads(query.recommended_medicines)
        except:
            query.recommendations = []
    
    return render(request, 'recommendation/history.html', {'queries': queries})
