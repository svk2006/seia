import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_openai_analysis(symptoms, crop_data):
    """Get analysis from OpenAI API"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Warning: OPENAI_API_KEY not set")
            return None
        
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are an agricultural expert specializing in crop stress management. Analyze this crop stress situation and provide practical recommendations:

Crop: {crop_data.get('crop_type', 'Unknown')}
Growth Stage: {crop_data.get('growth_stage', 'Unknown')}
Observed Symptoms: {symptoms}

Provide your response in the following format:
1. Root Cause (1-2 sentences identifying the primary cause)
2. Immediate Actions (3-4 actionable steps the farmer should take today)
3. Prevention Tips (2-3 preventive measures for future)

Keep the response concise, practical, and specific to the crop and symptoms."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert agricultural advisor with deep knowledge of crop stress management, disease identification, and sustainable farming practices."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        return None


def get_huggingface_analysis(symptoms, crop_data):
    """Get analysis from Hugging Face Inference API"""
    try:
        from huggingface_hub import InferenceClient
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("Warning: HUGGINGFACE_API_KEY not set")
            return None
        
        client = InferenceClient(api_key=api_key)
        
        prompt = f"""Agricultural Expert Analysis:
Crop: {crop_data.get('crop_type')}
Symptoms: {symptoms}

Provide 3 immediate actions and preventive measures."""
        
        response = client.text_generation(prompt, max_new_tokens=300)
        return response
    except Exception as e:
        print(f"HuggingFace Error: {str(e)}")
        return None


def get_ollama_analysis(symptoms, crop_data):
    """Get analysis from local Ollama (if available - fallback option)"""
    try:
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
        
        prompt = f"Agricultural analysis for {crop_data.get('crop_type')}: {symptoms}. Provide immediate actions."
        
        response = requests.post(
            ollama_url,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '')
    except Exception as e:
        print(f"Ollama Error: {str(e)}")
    
    return None


def get_ai_analysis(symptoms, crop_data):
    """
    Get AI analysis using configured provider.
    Tries providers in order: Configured > Ollama local > None
    Falls back gracefully if providers are not available.
    """
    provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    print(f"[LLM] Using provider: {provider}")
    
    # Try primary provider
    if provider == 'openai':
        result = get_openai_analysis(symptoms, crop_data)
        if result:
            print("[LLM] OpenAI analysis successful")
            return result
        print("[LLM] OpenAI failed, trying fallbacks...")
            
    elif provider == 'huggingface':
        result = get_huggingface_analysis(symptoms, crop_data)
        if result:
            print("[LLM] HuggingFace analysis successful")
            return result
        print("[LLM] HuggingFace failed, trying fallbacks...")
    
    # Try local Ollama as fallback
    result = get_ollama_analysis(symptoms, crop_data)
    if result:
        print("[LLM] Using local Ollama fallback")
        return result
    
    print("[LLM] No AI provider available, will use observation-based analysis only")
    # If all else fails, return None and let app use observation-based analysis
    return None
