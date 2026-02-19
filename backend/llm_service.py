import os
from openai import OpenAI

def get_ai_analysis(symptoms, crop_data):
    """Get analysis from OpenAI instead of Ollama"""
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Analyze this crop stress situation and provide actionable recommendations:
    
    Crop: {crop_data['crop_type']}
    Growth Stage: {crop_data['growth_stage']}
    Observed Symptoms: {symptoms}
    
    Provide:
    1. Root cause identification
    2. 3-4 immediate actions
    3. Prevention measures
    4. Expected recovery time
    
    Keep response concise and practical.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agricultural expert specialized in crop stress management."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def get_ollama_analysis(symptoms, crop_data):
    """Fallback to local Ollama if available"""
    import requests
    import json
    
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
    
    try:
        prompt = f"Analyze: {crop_data['crop_type']} with {symptoms}"
        response = requests.post(
            ollama_url,
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('response', '')
    except:
        pass
    
    return None  # Fall back to default recommendations