# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from decouple import config
from .forms import SymptomForm
from .models import PatientQuery
from .ml_model import get_recommender
import json
from deep_translator import GoogleTranslator
from openai import OpenAI


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


def translate_medicine_to_regional_language(recommendations, language_code):
    """Translate medicine recommendations to Hindi or Marathi using Google Translate"""
    if language_code not in ['hi', 'mr']:
        return recommendations
    
    translated_recommendations = []
    translator = GoogleTranslator(source='en', target=language_code)
    
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


@login_required
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
            query.user = request.user
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


@login_required
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
    translated_recommendations = translate_medicine_to_regional_language(recommendations, current_language)
    
    context = {
        'recommendations': translated_recommendations,
        'patient_info': patient_info
    }
    
    return render(request, 'recommendation/results.html', context)


@login_required
def history(request):
    """View past queries"""
    queries = PatientQuery.objects.filter(user=request.user).order_by('-created_at')[:10]  # Last 10 queries for current user
    
    # Parse JSON recommendations for each query
    for query in queries:
        try:
            query.recommendations = json.loads(query.recommended_medicines)
        except:
            query.recommendations = []
    
    return render(request, 'recommendation/history.html', {'queries': queries})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'recommendation/login.html', {'form': form})


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'recommendation/register.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


CHATBOT_SYSTEM_PROMPT = (
    "You are MediBot, a friendly AI health assistant embedded in the MediMatch web app. "
    "Provide general, educational information about common health topics, symptoms, "
    "over-the-counter medicines, wellness, and when to see a doctor. "
    "Be concise (use short paragraphs or bullet points). "
    "Never diagnose conditions, prescribe prescription medication, or replace a medical "
    "professional. Always include a brief disclaimer to consult a qualified doctor for "
    "personal medical advice. Respond in the same language the user wrote in."
)


@require_POST
def chatbot_api(request):
    """Endpoint for the floating Groq-powered chatbot widget."""
    api_key = config('GROQ_API_KEY', default='')
    if not api_key:
        return JsonResponse(
            {'error': 'Chatbot is not configured. Please set GROQ_API_KEY in the environment.'},
            status=503,
        )

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request payload.'}, status=400)

    history = payload.get('history') or []
    user_message = (payload.get('message') or '').strip()
    if not user_message:
        return JsonResponse({'error': 'Empty message.'}, status=400)

    model_name = config('GROQ_MODEL', default='openai/gpt-oss-20b')

    input_lines = []
    for turn in history[-20:]:
        role = turn.get('role')
        text = (turn.get('text') or '').strip()
        if not text:
            continue
        if role == 'user':
            input_lines.append({'role': 'user', 'content': text})
        elif role == 'assistant':
            input_lines.append({'role': 'assistant', 'content': text})
    input_lines.append({'role': 'user', 'content': user_message})

    try:
        client = OpenAI(api_key=api_key, base_url='https://api.groq.com/openai/v1')
        response = client.responses.create(
            model=model_name,
            instructions=CHATBOT_SYSTEM_PROMPT,
            input=input_lines,
            temperature=0.5,
        )
        reply = (getattr(response, 'output_text', '') or '').strip() or "I'm sorry, I couldn't generate a response. Please try again."
        return JsonResponse({'reply': reply})
    except Exception as e:
        return JsonResponse(
            {'error': f'Chatbot error: {e}'},
            status=500,
        )
