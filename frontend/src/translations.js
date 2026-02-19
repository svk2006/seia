// Language translations for English and Tamil
const translations = {
  en: {
    // Header
    appTitle: "Crop Stress Advisory",
    appSubtitle: "AI-powered climate-smart crop health predictions for resilient farming",
    
    // Loading & Status
    loading: "Loading weather",
    analyzing: "Analyzing crop health",
    
    // Climate Action Messaging
    climateAction: "Building climate resilience",
    resilienceTitle: "Climate Resilience",
    adaptationTip: "Climate adaptation strategy",
    
    // Weather Card
    weatherTitle: "Weather at {location}",
    temperature: "Temperature",
    humidity: "Humidity",
    rainfall: "Rainfall",
    wind: "Wind",
    
    // Stress Level Card
    cropHealthy: "Crop is Healthy",
    mildStress: "Mild Stress Detected",
    severeStress: "Severe Stress Alert",
    confidence: "Confidence",
    recommendation: "Farming Recommendation",
    aiAnalysis: "AI Analysis (Mistral)",
    lastUpdated: "Last updated",
    
    // Report Form
    submitReport: "Submit Crop Report",
    cropType: "Crop Type",
    growthStage: "Growth Stage",
    observations: "Observations (Optional)",
    observationsPlaceholder: "Describe any visible symptoms, yellowing, wilting, or pest damage...",
    detected: "Detected",
    latitude: "Latitude",
    longitude: "Longitude",
    changeLocation: "Change Location (City/State)",
    searchLocation: "Search city or state (e.g., Mumbai, Bangalore, Pune)...",
    noLocations: "No locations found. Enter coordinates below.",
    manualCoordinates: "Manual Coordinates (Advanced)",
    submitAnalyze: "Submit & Analyze Report",
    
    // Map
    reportsMap: "Reports Map",
    yourLocation: "Your Location",
    status: "Status",
    growth: "Growth",
    
    // Reports Summary
    recentSubmissions: "Recent Submissions",
    noReports: "No reports yet. Submit one to get started!",
    
    // Error Messages
    geolocationError: "Using default location (Delhi). Enable location access for your actual location.",
    geolocationNotSupported: "Geolocation not supported. Using default location.",
    weatherError: "Could not fetch live weather. Using offline data.",
    submitError: "Failed:",
    error: "Error",
    
    // Footer
    footerText: "Built with ❤️ for farmers | ML + Ollama Mistral AI | Real-time Weather Data",
    copyright: "© 2026 AI Hackathon - Crop Stress Advisory System",
    
    // Growth Stages
    vegetative: "Vegetative",
    flowering: "Flowering",
    fruiting: "Fruiting",
    grain_fill: "Grain Fill",
    mature: "Mature",
    pod_fill: "Pod Fill",
    boll_formation: "Boll Formation",
    
    // Crops
    tomato: "Tomato",
    lettuce: "Lettuce",
    cucumber: "Cucumber",
    basil: "Basil",
    mint: "Mint",
    pepper: "Pepper",
    carrot: "Carrot",
    wheat: "Wheat",
    maize: "Maize",
    rice: "Rice",
    cotton: "Cotton",
    sugarcane: "Sugarcane",
    pulses: "Pulses",
    
    // Stress Labels
    healthy: "Healthy",
    
    // Language Switcher
    english: "English",
    tamil: "Tamil",
  },
  
  ta: {
    // Header
    appTitle: "பயிர் அழுத்த ஆலோசனை",
    appSubtitle: "விவசாயிகளுக்கான AI-இயக்கிய காலநிலை-புத்திமான் பயிர் சுகாதார முன்கணிப்புகள்",
    
    // Loading & Status
    loading: "வானிலை ஏற்றப்படுகிறது",
    analyzing: "பயிர் சுகாதாரம் பகுப்பாய்வு செய்யப்படுகிறது",
    
    // Climate Action Messaging
    climateAction: "காலநிலை நிலைத்தன்மை உருவாக்குதல்",
    resilienceTitle: "காலநிலை நிலைத்தன்மை",
    adaptationTip: "காலநிலை மানিய உபாய",
    
    // Weather Card
    weatherTitle: "வானிலை {location}",
    temperature: "வெப்பநிலை",
    humidity: "ஈரப்பதம்",
    rainfall: "மழைப்பொழிவு",
    wind: "காற்று",
    
    // Stress Level Card
    healthyStatus: "பயிர் ஆரோக்கியமாக உள்ளது",
    mildStressStatus: "லேசான அழுத்தம் கண்டறிந்தது",
    severeStressStatus: "கடுமையான அழுத்த எச்சரிக்கை",
    confidence: "நம்பிக்கை",
    farmingRecommendation: "விவசாய பரிந்துரை:",
    aiAnalysis: "AI பகுப்பாய்வு (Mistral):",
    lastUpdated: "கடைசியாக புதுப்பிக்கப்பட்டது:",
    
    // Report Form
    submitCropReport: "பயிர் அறிக்கை சமர்ப்பிக்கவும்",
    cropType: "பயிர் வகை",
    growthStage: "வளர்ச்சி நிலை",
    observations: "அவதானிப்புகள் (விரும்பினால்)",
    observationsPlaceholder: "இலைகளின் மஞ்சள் நிறம், முடக்கம், அல்லது பூச்சி சேதம் போன்ற எந்த கண்ணுக்குத் தெரியும் அறிகுறிகளையும் விவரிக்கவும்...",
    manualLocation: "கையேடு இடம் (விரும்பினால்)",
    latitude: "அட்சரேகை",
    longitude: "தீர்க்ஷமை",
    submitButton: "சமர்ப்பிக்கவும் & பகுப்பாய்வு செய்யவும்",
    
    // Map
    reportsMap: "அறிக்கைகள் வரைபடம்",
    yourLocation: "உங்கள் இடம்",
    
    // Reports Summary
    recentSubmissions: "சமீபத்திய சமர்ப்பணங்கள்",
    noReportsYet: "இன்னும் அறிக்கைகள் இல்லை. ஒன்றைச் சமர்ப்பிட்டு தொடங்கவும்!",
    
    // Error Messages
    geolocationError: "இயல்பான இடம் (டெல்லி) பயன்படுத்தப்படுகிறது. உங்கள் உண்மையான இடத்திற்கு இடம் அணுகலை இயக்கவும்.",
    geolocationNotSupported: "அட்சரேகை ஆதரிக்கப்படவில்லை. இயல்பான இடம் பயன்படுத்தப்படுகிறது.",
    couldNotFetchWeather: "நேரடி வானிலை பெற முடியவில்லை. অফলைன் தரவு பயன்படுத்தப்படுகிறது.",
    
    // Footer
    footer: "விவசாயிகளுக்கான உள்ளம் நிறைய கட்டப்பட்டது | ML + Ollama Mistral AI | நேரடி வானிலை தரவு",
    copyright: "2026 AI ஹ்যாக்கதான் - பயிர் அழுத்த ஆலோசனை அமைப்பு",
    
    // Growth Stages
    vegetative: "துளைக்கும் நிலை",
    flowering: "பூப்பிக்கும் நிலை",
    fruiting: "பலன் நிலை",
    grain_fill: "தானியம் நிரப்புதல்",
    mature: "முதிர்ந்த",
    pod_fill: "பாட் நிப்புதல்",
    boll_formation: "பருக்கை உருவாக்கம்",
    
    // Crops
    tomato: "தக்காளி",
    lettuce: "கீரை",
    cucumber: "வெள்ளரி",
    basil: "துளசி",
    mint: "புதினா",
    pepper: "மிளகாய்",
    carrot: "கேரட்",
    wheat: "கோதுமை",
    maize: "சோளம்",
    rice: "அரிசி",
    cotton: "பருத்தி",
    sugarcane: "கரும்பு",
    pulses: "பயறுவகைகள்",
    
    // Stress Labels
    healthy: "ஆரோக்கியமான",
    mild_stress: "லேசான அழுத்தம்",
    severe_stress: "கடுமையான அழுத்தம்",
  }
};

export default translations;
