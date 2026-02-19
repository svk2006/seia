import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

class CropStressModel:
    def __init__(self):
        self.model = None
        self.crop_encoder = LabelEncoder()
        self.stage_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_names = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'crop_type_encoded', 'growth_stage_encoded']
        self.load_model()
        
    def train(self, data_path='training_data_expanded.csv'):
        """Train the ML model on historical data"""
        print("Loading training data...")
        df = pd.read_csv(data_path)
        
        # Encode categorical features
        df['crop_type_encoded'] = self.crop_encoder.fit_transform(df['crop_type'])
        df['growth_stage_encoded'] = self.stage_encoder.fit_transform(df['growth_stage'])
        
        # Prepare features and target
        X = df[['temperature', 'humidity', 'rainfall', 'wind_speed', 'crop_type_encoded', 'growth_stage_encoded']]
        y = df['stress_level']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Train model with improved hyperparameters
        print("Training Gradient Boosting model...")
        self.model = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.03,
            max_depth=6,
            subsample=0.85,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            verbose=0
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Train accuracy: {train_score:.2%}")
        print(f"Test accuracy: {test_score:.2%}")
        print(f"Trained on {len(df)} samples with {len(df['crop_type'].unique())} crops")
        
        # Save model
        self.save_model('model.pkl')
        
    def predict(self, temperature, humidity, rainfall, wind_speed, crop_type, growth_stage):
        """Make a prediction for crop stress level"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        try:
            crop_encoded = self.crop_encoder.transform([crop_type])[0]
            stage_encoded = self.stage_encoder.transform([growth_stage])[0]
        except:
            crop_encoded = 0
            stage_encoded = 0
        
        features = np.array([[temperature, humidity, rainfall, wind_speed, crop_encoded, stage_encoded]])
        
        # Scale features using the same scaler
        features_scaled = self.scaler.transform(features)
        
        # Predict
        stress_level = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        confidence = float(probabilities[int(stress_level)])
        
        return int(stress_level), float(confidence)
    
    def save_model(self, path='model.pkl'):
        """Save trained model and encoders to disk"""
        data = {
            'model': self.model,
            'crop_encoder': self.crop_encoder,
            'stage_encoder': self.stage_encoder,
            'scaler': self.scaler
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    def load_model(self, path='model.pkl'):
        """Load trained model and encoders from disk"""
        if not os.path.exists(path):
            print(f"Model not found. Training new model...")
            self.train()
            return
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.model = data['model']
        self.crop_encoder = data['crop_encoder']
        self.stage_encoder = data['stage_encoder']
        self.scaler = data['scaler']


# Crop-specific care recommendations & yield optimization
CROP_CARE = {
    'tomato': {
        'healthy': 'Your tomatoes are thriving! Keep soil consistently moist (2-3cm depth). Prune suckers weekly. Support with stakes as they grow.',
        'mild_stress': 'Tomatoes under mild stress. Increase watering to 5-6cm weekly. Apply mulch to retain moisture (5cm layer). Check for early blight on lower leaves.',
        'severe_stress': 'CRITICAL: Your tomatoes need immediate care! Deep water 8-10cm immediately. Apply fungicide for blight prevention. Remove affected leaves. Increase airflow.',
        'yield': 'Target: 20-30 tons/ha. Optimal temps: 21-27°C. Harvest when pink to extend ripeness. Use drip irrigation for 30% water savings.',
    },
    'lettuce': {
        'healthy': 'Lettuce growing well! Keep soil moist but not waterlogged. Provide afternoon shade in hot weather. Harvest outer leaves regularly.',
        'mild_stress': 'Lettuce stressed. Increase watering frequency (daily). Add shade cloth if temps >28°C. Check for aphids on new leaves.',
        'severe_stress': 'URGENT: Lettuce wilting! Water immediately and deeply. Provide 50% shade. Remove any bolting plants. Mist leaves in morning.',
        'yield': 'Target: 15-20 tons/ha. Optimal temps: 15-20°C. Bitter if temp >25°C. Succession plant every 2 weeks for continuous harvest.',
    },
    'cucumber': {
        'healthy': 'Cucumbers flourishing! Provide sturdy trellis support. Water 5cm weekly. Pinch main stem after 7-8 leaves to encourage lateral growth.',
        'mild_stress': 'Cucumber mildly stressed. Check for powdery mildew (white coating). Increase watering and airflow. Thin foliage if overcrowded.',
        'severe_stress': 'CRITICAL: Cucumbers drying! Water 10cm immediately. Spray with sulfur for mildew. Provide 50% shade cloth. Prune excess vines.',
        'yield': 'Target: 25-30 tons/ha. Optimal temps: 18-30°C. Pick every 2 days when 15-20cm (smaller = better quality). Daily picking increases yield.',
    },
    'basil': {
        'healthy': 'Basil is perfect! Pinch tops weekly to encourage bushiness. Keep soil consistently moist. Harvest before flowering for best flavor.',
        'mild_stress': 'Basil showing stress. Reduce watering (let topsoil dry between). Check for spider mites (fine webbing). Increase light exposure.',
        'severe_stress': 'URGENT: Basil dehydrating! Water immediately. Move to sunnier location (>6 hrs direct sun). Apply oil spray for mites.',
        'yield': 'Target: 3-4 harvests/season. Pinching increases yield by 40%. Optimal temps: 20-25°C. Freeze leaves in ice cubes for storage.',
    },
    'mint': {
        'healthy': 'Mint thriving! Very hardy - pinch regularly to control spread. Water moderately. Excellent for companion planting.',
        'mild_stress': 'Mint wilting slightly. Check soil drainage (mint prefers moist but well-drained). Reduce nitrogen fertilizer.',
        'severe_stress': 'CRITICAL: Mint dying! Water deeply. Check for root rot (musty smell). Improve drainage or repot. Trim dead foliage.',
        'yield': 'Target: 4-5 harvests/season. Very productive. Optimal temps: 15-25°C. Harvest before noon for maximum essential oil content.',
    },
    'pepper': {
        'healthy': 'Peppers doing great! Support with stakes. Water 5-6cm weekly. Blossom drop? Ensure consistent watering and 70F+ nights.',
        'mild_stress': 'Peppers under stress. Maintain consistent 70F+ night temps. Increase watering if soil dry >2cm. Check for spider mites.',
        'severe_stress': 'URGENT: Peppers failing! Water 8cm immediately. Protect from temps <55F (move inside/cover). Spray for pests.',
        'yield': 'Target: 8-12 tons/ha. Optimal temps: 25-30C day, 18-21C night. Harvest green or wait for color (15-20 days longer). Fruiting takes 60-90 days.',
    },
    'carrot': {
        'healthy': 'Carrots developing well! Thin seedlings to 5cm apart at 4-week mark. Keep soil loose and moist. Avoid splitting with consistent moisture.',
        'mild_stress': 'Carrots stressed. Loosen soil if compacted (check depth to 30cm). Water 5cm weekly. Avoid excess nitrogen (causes forked roots).',
        'severe_stress': 'CRITICAL: Carrots stunted! Aerate soil deeply. Water 8cm. Test soil pH (prefer 6.0-6.8). May need 2-3 months total recovery.',
        'yield': 'Target: 20-30 tons/ha. Optimal temps: 15-20C. Harvest at 2-3cm diameter for best sweetness. Store at 1C for 6+ weeks.',
    },
    'wheat': {
        'healthy': 'Wheat crop excellent! Monitor tiller formation (3-4 tillers optimal at tillering stage). Rainfall or irrigation: 500-750mm total.',
        'mild_stress': 'Wheat under stress. Check for diseases (leaf spot, rust). Ensure proper spacing for airflow. Fertilize if yellowing.',
        'severe_stress': 'URGENT: Wheat severely stressed! Apply fungicide if disease visible. Irrigate 5-6cm immediately. May need varieties replanting.',
        'yield': 'Target: 5-8 tons/ha. Optimal temps: 15-20C for growth, 10-15C for grain fill. Harvest when moisture <15%. 120-150 days to maturity.',
    },
    'maize': {
        'healthy': 'Maize thriving! Monitor V-stage (visible leaf stage) weekly. Ensure uniform plant heights. Support with adequate fertilizer.',
        'mild_stress': 'Maize showing stress. Check for nitrogen deficiency (bottom leaves yellowing). Increase irrigation 5-6cm weekly.',
        'severe_stress': 'CRITICAL: Maize failing! Deep irrigation 8-10cm immediately. Fertilize with nitrogen. Check for root diseases.',
        'yield': 'Target: 8-12 tons/ha. Optimal temps: 25-30C day, 15-20C night. Harvest at physiological maturity (black dot at kernel base). 110-140 days.',
    },
    'rice': {
        'healthy': 'Rice flooded and healthy! Maintain 5-7cm water depth. Watch for pest infestations (stemborers, leafhoppers). Optimal pH: 6.0-7.5.',
        'mild_stress': 'Rice under stress. Check water quality (maintain level). Watch for leaf spots or discoloration. Apply fungicide if needed.',
        'severe_stress': 'URGENT: Rice crop threatened! Drain and inspect roots (gray = root necrosis). Re-flood immediately. Apply pesticide if infested.',
        'yield': 'Target: 5-8 tons/ha (milled rice: 2.5-4 tons). Optimal temps: 25-30C. Harvest at 20% moisture. Store at <13% for longevity.',
    },
    'cotton': {
        'healthy': 'Cotton bolls filling nicely! Maintain 60cm spacing. Monitor for insects (aphids, bollworms). Boll development: 50-60 days from flowering.',
        'mild_stress': 'Cotton under stress. Check for whiteflies (sticky residue). Increase water 5-6cm weekly. Monitor boll development.',
        'severe_stress': 'CRITICAL: Cotton failing! Water 8-10cm immediately. Apply insecticide for boll damage. Check for root rot.',
        'yield': 'Target: 1.5-2.5 tons/hectare lint. Optimal temps: 26-35C day (avoid <15C). Lint quality best when temperatures stable. Harvest at 40% boll opening.',
    },
    'sugarcane': {
        'healthy': 'Sugarcane stalks excellent! Optimal height: 2-2.5m. Provide adequate spacing (1m between rows). Monitor NPK ratios.',
        'mild_stress': 'Sugarcane stressed. Check for smut (black powder on shoots) - remove stalks. Water 5-6cm weekly. Reduce nitrogen if pests increase.',
        'severe_stress': 'URGENT: Sugarcane failing! Water 8-10cm immediately. Apply smut fungicide if infected. May need to replant sections.',
        'yield': 'Target: 50-80 tons/ha fresh stalks, 12-16 tons sugar/ha. Optimal temps: 22-30C. Crush when brix >12. Ratoon for 4-5 seasons.',
    },
    'pulses': {
        'healthy': 'Pulse crops developing well! Monitor pod formation. Support with light staking. Nitrogen-fixing legumes - no extra N needed after inoculant.',
        'mild_stress': 'Pulses stressed. Check for wilting (overwatering). Reduce water frequency. Monitor for pod spot disease.',
        'severe_stress': 'CRITICAL: Pulses failing! Water 5-6cm if drought. Spray fungicide for disease. Thin crowded plants for airflow.',
        'yield': 'Target: 1.5-2.5 tons/ha. Optimal temps: 20-25C. Harvest when pods dry and rattle. Post-harvest: Store at <10% moisture.',
    }
}

def get_stress_recommendation(stress_level, crop_type='unknown'):
    """Get general farming recommendation based on stress level"""
    recommendations = {
        0: "✅ Your crop looks healthy! Continue regular maintenance and monitor soil moisture.",
        1: "⚠️ Mild stress detected. Increase irrigation by 15%. Check for pests. Monitor growth closely.",
        2: "🚨 SEVERE STRESS! Urgent action: Increase irrigation by 40%, apply treatments, monitor closely."
    }
    return recommendations.get(stress_level, "Unable to determine recommendation")

def get_crop_care(stress_level, crop_type):
    """Get crop-specific care recommendations"""
    crop_data = CROP_CARE.get(crop_type.lower(), {})
    
    if stress_level == 0:
        return crop_data.get('healthy', get_stress_recommendation(0, crop_type))
    elif stress_level == 1:
        return crop_data.get('mild_stress', get_stress_recommendation(1, crop_type))
    else:  # stress_level == 2
        return crop_data.get('severe_stress', get_stress_recommendation(2, crop_type))

def get_yield_info(crop_type):
    """Get yield optimization tips"""
    crop_data = CROP_CARE.get(crop_type.lower(), {})
    return crop_data.get('yield', 'No specific yield data available.')

def get_stress_label(stress_level):
    """Get human-readable stress label"""
    labels = {
        0: "Healthy",
        1: "Mild Stress",
        2: "Severe Stress"
    }
    return labels.get(stress_level, "Unknown")

def get_stress_color(stress_level):
    """Get color for stress level"""
    colors = {
        0: "#22c55e",  # Green
        1: "#eab308",  # Amber
        2: "#ef4444"   # Red
    }
    return colors.get(stress_level, "#6b7280")
def generate_observation_based_advice(crop_type, stress_level, observed_symptoms, temperature, humidity, growth_stage):
    """Generate detailed, symptom-specific advice for each observed issue"""
    
    # Symptom-specific remedies - universal treatments
    symptom_remedies = {
        'wilting': {
            'cause': 'Inadequate soil moisture or root stress',
            'immediate': '1. Water deeply (5-8cm) immediately to reach root zone. 2. Apply mulch (5cm) to reduce evaporation.',
            'treatment': '3. Check soil moisture daily. 4. Prune affected leaves to reduce water demand.',
            'urgent': stress_level == 2
        },
        'yellowing': {
            'cause': 'Nitrogen deficiency, waterlogging, or nutrient lockout',
            'immediate': '1. Apply nitrogen-rich fertilizer (urea or compost tea). 2. Check drainage - ensure no waterlogging.',
            'treatment': '3. Apply foliar spray (Neem oil or compost extract). 4. Improve soil aeration by reducing compaction.',
            'urgent': stress_level == 2
        },
        'spotting': {
            'cause': 'Fungal or bacterial disease',
            'immediate': '1. Remove and destroy affected leaves immediately. 2. Improve air circulation by pruning dense foliage.',
            'treatment': '3. Apply sulfur or copper fungicide every 7 days. 4. Avoid overhead watering - water at soil level only.',
            'urgent': stress_level == 2
        },
        'pests': {
            'cause': 'Insect infestation',
            'immediate': '1. Inspect both leaf surfaces for pest presence. 2. Spray with organic insecticide (neem oil, soap spray).',
            'treatment': '3. Apply spinosad or pyrethrin if organic fails. 4. Release beneficial insects (ladybugs, parasitic wasps).',
            'urgent': stress_level == 2
        },
        'disease': {
            'cause': 'Fungal, bacterial, or viral infection',
            'immediate': '1. Isolate affected plant if possible. 2. Remove all diseased parts (sanitize tools between cuts).',
            'treatment': '3. Apply appropriate fungicide or bactericide. 4. Improve sanitation - clean leaves with 70% alcohol.',
            'urgent': stress_level == 2
        },
        'dry': {
            'cause': 'Severe dehydration or high transpiration',
            'immediate': '1. Water deeply immediately (8-10cm). 2. Provide shade cloth (30-50%) to reduce heat stress.',
            'treatment': '3. Mist leaves early morning to reduce heat. 4. Add organic matter to soil to improve water retention.',
            'urgent': stress_level == 2
        },
        'stunting': {
            'cause': 'Nutrient deficiency, disease, or environmental stress',
            'immediate': '1. Apply balanced fertilizer (NPK 10-10-10). 2. Ensure proper lighting (6+ hours direct sun).',
            'treatment': '3. Check for root diseases (musty smell = root rot). 4. Optimize temperature for growth stage.',
            'urgent': stress_level == 2
        }
    }
    
    # Crop-specific adjustment factors
    crop_specific_factors = {
        'tomato': {'watering': 'drip irrigation', 'sensitivity': 'high to disease'},
        'lettuce': {'watering': 'frequent, light', 'sensitivity': 'bolts if hot'},
        'cucumber': {'watering': 'consistent moisture', 'sensitivity': 'powdery mildew'},
        'basil': {'watering': 'let topsoil dry', 'sensitivity': 'spider mites'},
        'mint': {'watering': 'moist not wet', 'sensitivity': 'root rot'},
        'pepper': {'watering': 'consistent', 'sensitivity': 'blossom drop'},
        'carrot': {'watering': 'moderate', 'sensitivity': 'root splitting'},
    }
    
    # Build personalized response
    advice_dict = {
        'observed_symptoms': observed_symptoms,
        'symptom_analysis': [],
        'combined_assessment': '',
        'action_priority': []
    }
    
    if not observed_symptoms:
        # No specific symptoms - use ML prediction only
        advice_dict['combined_assessment'] = f"Your {crop_type} shows {get_stress_label(stress_level).lower()} based on current conditions (Temp: {temperature}°C, Humidity: {humidity}%). {get_crop_care(stress_level, crop_type)}"
        return advice_dict
    
    # Process each observed symptom
    for symptom in observed_symptoms:
        remedy = symptom_remedies.get(symptom, {})
        if remedy:
            advice_dict['symptom_analysis'].append({
                'symptom': symptom,
                'cause': remedy.get('cause', 'Unknown cause'),
                'immediate_actions': remedy.get('immediate', ''),
                'follow_up': remedy.get('treatment', ''),
                'is_urgent': remedy.get('urgent', False)
            })
            if remedy.get('urgent'):
                advice_dict['action_priority'].append(symptom)
    
    # Combined assessment
    urgency_text = "URGENT ACTION NEEDED!" if stress_level == 2 and observed_symptoms else "Monitoring recommended" if stress_level == 1 else "Preventive care suggested"
    
    crop_factor = crop_specific_factors.get(crop_type.lower(), {})
    watering_method = crop_factor.get('watering', 'regular watering')
    
    advice_dict['combined_assessment'] = f"{urgency_text} - Your {crop_type} ({growth_stage}) has {len(observed_symptoms)} observed issue(s). Current conditions (Temp: {temperature}°C, Humidity: {humidity}%) combined with reported symptoms suggest {get_stress_label(stress_level).lower()}. Recommended approach: Use {watering_method} and closely monitor over next 48 hours."
    
    return advice_dict