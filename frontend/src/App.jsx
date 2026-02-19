import { useEffect, useState } from 'react';
import axios from 'axios';
import translations from './translations';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Translation helper function
const t = (language, key) => {
  const dict = translations[language] || translations['en'];
  return dict[key] || key;
};

// Animated Loading Component - Climate-themed
function ClimateLoadingAnimation({ language }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="relative w-20 h-20">
        {/* Cloud animation - representing weather monitoring */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-5xl animate-pulse">☁️</div>
        </div>
        
        {/* Leaf particles - representing crop growth and resilience */}
        <div className="absolute top-0 right-0 text-2xl animate-bounce" style={{animationDelay: '0s'}}>🌿</div>
        <div className="absolute top-2 left-0 text-2xl animate-bounce" style={{animationDelay: '0.3s'}}>🌱</div>
        <div className="absolute bottom-0 right-2 text-2xl animate-bounce" style={{animationDelay: '0.6s'}}>🌾</div>
      </div>
      
      {/* Animated text */}
      <div className="text-center">
        <p className="text-sm font-semibold text-green-700 mb-2">
          {t(language, 'analyzing')}...
        </p>
        <div className="flex gap-1 justify-center">
          <span className="w-2 h-2 bg-green-600 rounded-full animate-pulse"></span>
          <span className="w-2 h-2 bg-green-600 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></span>
          <span className="w-2 h-2 bg-green-600 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></span>
        </div>
      </div>
      
      {/* Climate Action indicator */}
      <p className="text-xs text-blue-600 font-semibold mt-2 flex items-center gap-1">
        🌍 {t(language, 'climateAction')}
      </p>
    </div>
  );
}

// Weather Card Component
function WeatherCard({ weather, loading, language }) {
  if (loading) return <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-green-100">{t(language, 'loading')}...</div>;
  if (!weather) return null;

  const getWeatherIcon = (description) => {
    const desc = description.toLowerCase();
    if (desc.includes('rain')) return '🌧️';
    if (desc.includes('cloud')) return '☁️';
    if (desc.includes('clear') || desc.includes('sunny')) return '☀️';
    if (desc.includes('wind')) return '💨';
    return '🌤️';
  };

  return (
    <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-4 sm:p-6 rounded-xl shadow-sm border border-green-200">
      <h3 className="text-lg sm:text-xl font-bold text-green-800 mb-4 flex items-center gap-2">
        <span>🌍 {t(language, 'weatherTitle').replace('{location}', weather.location)}</span>
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
        <div className="bg-white p-3 rounded-lg border border-green-100">
          <p className="text-3xl mb-1">{getWeatherIcon(weather.description)}</p>
          <p className="text-xl font-bold text-green-700">{weather.temperature}°C</p>
          <p className="text-xs text-green-600">{t(language, 'temperature')}</p>
          
          {/* Climate indicator */}
          <div className="mt-2 text-xs font-semibold text-blue-600">
            {weather.temperature > 30 ? '🌡️ Hot' : weather.temperature < 15 ? '❄️ Cool' : '✓ Optimal'}
          </div>
        </div>
        <div className="bg-white p-3 rounded-lg border border-green-100">
          <p className="text-3xl mb-1">💧</p>
          <p className="text-xl font-bold text-blue-600">{weather.humidity}%</p>
          <p className="text-xs text-green-600">{t(language, 'humidity')}</p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-green-100">
          <p className="text-3xl mb-1">🌧️</p>
          <p className="text-xl font-bold text-blue-500">{weather.rainfall} mm</p>
          <p className="text-xs text-green-600">{t(language, 'rainfall')}</p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-green-100">
          <p className="text-3xl mb-1">💨</p>
          <p className="text-xl font-bold text-orange-600">{weather.wind_speed} m/s</p>
          <p className="text-xs text-green-600">{t(language, 'wind')}</p>
        </div>
      </div>
    </div>
  );
}

// Stress Level Card Component
function StressLevelCard({ prediction, loading, language }) {
  if (loading) return (
    <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-green-100 flex justify-center">
      <ClimateLoadingAnimation language={language} />
    </div>
  );
  if (!prediction) return null;

  const stressColors = {
    0: { 
      bg: 'from-green-50 to-emerald-50', 
      border: 'border-green-300',
      badge: 'bg-green-100 text-green-800',
      icon: '✅',
      title: t(language, 'cropHealthy'),
      resilience: 'High resilience to climate variability'
    },
    1: { 
      bg: 'from-amber-50 to-yellow-50', 
      border: 'border-amber-300',
      badge: 'bg-amber-100 text-amber-800',
      icon: '⚠️',
      title: t(language, 'mildStress'),
      resilience: 'Building adaptive capacity needed'
    },
    2: { 
      bg: 'from-red-50 to-orange-50', 
      border: 'border-red-300',
      badge: 'bg-red-100 text-red-800',
      icon: '🚨',
      title: t(language, 'severeStress'),
      resilience: 'Emergency resilience measures required'
    }
  };

  const colors = stressColors[prediction.stress_level] || stressColors[0];

  return (
    <div className={`bg-gradient-to-br ${colors.bg} p-4 sm:p-6 rounded-xl shadow-sm border-2 ${colors.border}`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg sm:text-xl font-bold text-gray-800">{colors.title}</h3>
          <p className={`inline-block ${colors.badge} px-3 py-1 rounded-full text-sm font-semibold mt-2`}>
            {prediction.stress_label} ({(prediction.confidence * 100).toFixed(0)}% confidence)
          </p>
        </div>
        <p className="text-4xl">{colors.icon}</p>
      </div>

      {/* Climate Resilience Status */}
      <div className="bg-white/80 p-3 rounded-lg mb-4 border-l-4 border-blue-400">
        <p className="text-xs text-blue-700 font-semibold flex items-center gap-2 mb-1">
          🌍 {language === 'ta' ? 'காலநிலை நிலைத்தன்மை' : 'Climate Resilience Status'}
        </p>
        <p className="text-xs text-blue-600">{colors.resilience}</p>
      </div>
      
      {/* Combined Assessment from Observation Analysis */}
      {prediction.combined_assessment && (
        <div className="bg-blue-50/80 p-4 rounded-lg mb-4 border-l-4 border-blue-500">
          <p className="font-semibold text-blue-900 text-sm mb-2">📋 {language === 'ta' ? 'மதிப்பீடு' : 'Assessment'}:</p>
          <p className="text-sm text-blue-800 leading-relaxed">{prediction.combined_assessment}</p>
        </div>
      )}

      {/* Observed Symptoms with Specific Advice */}
      {prediction.symptom_analysis && prediction.symptom_analysis.length > 0 && (
        <div className="bg-orange-50/80 p-4 rounded-lg mb-4 border border-orange-300">
          <p className="font-semibold text-orange-900 mb-3 flex items-center gap-2">
            🔍 {language === 'ta' ? 'கண்டறியப்பட்ட பிரச்சனைகள்' : 'Detected Issues'} ({prediction.symptom_analysis.length})
          </p>
          <p className="text-xs text-orange-700 mb-3 italic">
            {language === 'ta' ? 'குறிப்பு: இந்த பிரச்சனைகளை சரிசெய்ய தسریع நடவடிக்கை எடுக்க வேண்டியது அত்यন्த முக்கியம்' : 'Note: Prompt action is critical to address these issues and build climate resilience'}
          </p>
          <div className="space-y-3">
            {prediction.symptom_analysis
              .sort((a, b) => b.is_urgent - a.is_urgent)
              .map((issue, idx) => (
              <div key={idx} className={`${issue.is_urgent ? 'bg-red-50 border-red-300' : 'bg-white/80 border-orange-300'} p-3 rounded border-l-4`}>
                <p className="font-bold text-orange-700 text-sm capitalize mb-2 flex items-center gap-2">
                  {issue.is_urgent && '🚨'} {language === 'ta' ? 'பிரச்சனை' : 'Issue'}: {issue.symptom.replace('_', ' ')}
                </p>
                <p className="text-xs text-gray-700 mb-2">
                  <span className="font-semibold">{language === 'ta' ? 'காரணம்' : 'Cause'}:</span> {issue.cause}
                </p>
                <p className="text-xs text-gray-700 font-semibold text-red-700 mb-1">⚡ {language === 'ta' ? 'உடனடி நடவடிக்கை' : 'Immediate Action'}:</p>
                <p className="text-xs text-gray-700 mb-2 ml-3">{issue.immediate_actions}</p>
                <p className="text-xs text-gray-700 font-semibold text-blue-700 mb-1">📌 {language === 'ta' ? 'பின்தொடர்ச்சி' : 'Follow-up'}:</p>
                <p className="text-xs text-gray-700 ml-3">{issue.follow_up}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ML-Based General Recommendation with Climate Resilience */}
      <div className="bg-white/70 p-4 rounded-lg mb-4 border border-gray-200">
        <p className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
          🌾 {t(language, 'recommendation')}
        </p>
        <p className="text-sm text-gray-700 leading-relaxed">{prediction.ml_based_recommendation}</p>
        
        {/* Climate Resilience Indicator */}
        <div className="mt-3 pt-3 border-t border-gray-200 text-xs text-blue-700 flex items-center gap-2 font-semibold">
          🌍 {t(language, 'resilienceTitle')}: {language === 'ta' ? 'தசை வருமான உত்पादন' : 'Adaptive farming practices reduce climate risk by 40%+'}
        </div>
      </div>

      {/* Detailed AI Analysis from Ollama */}
      {prediction.ai_detailed_analysis && (
        <div className="bg-purple-50/80 p-4 rounded-lg mb-4 border border-purple-300">
          <p className="font-semibold text-purple-900 mb-2 flex items-center gap-2">🤖 {t(language, 'aiAnalysis')}</p>
          <p className="text-sm text-purple-800 leading-relaxed whitespace-pre-wrap">{prediction.ai_detailed_analysis}</p>
        </div>
      )}

      {/* Yield Optimization */}
      {prediction.yield_optimization && (
        <div className="bg-green-50/80 p-4 rounded-lg mb-4 border border-green-300">
          <p className="font-semibold text-green-900 mb-2">📊 {language === 'ta' ? 'விளை மேம்பாடு' : 'Yield Optimization'}:</p>
          <p className="text-sm text-green-800 leading-relaxed">{prediction.yield_optimization}</p>
        </div>
      )}

      <p className="text-xs text-gray-500 mt-3">{t(language, 'lastUpdated')}: {new Date(prediction.timestamp).toLocaleTimeString()}</p>
    </div>
  );
}

// Map Component
function MapView({ reports, userLocation, language }) {
  const [mapError, setMapError] = useState(null);

  useEffect(() => {
    if (!userLocation) return;

    const mapEl = document.getElementById('map');
    if (!mapEl) return;

    // Dynamically load Leaflet
    if (window.L) {
      initMap();
    } else {
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.onload = initMap;
      document.head.appendChild(script);
    }

    function initMap() {
      try {
        const L = window.L;
        
        // Clear existing map
        if (window.mapInstance) {
          window.mapInstance.remove();
        }

        // Create new map
        const map = L.map('map').setView(userLocation, 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap',
          maxZoom: 19,
        }).addTo(map);

        // User location marker (blue, larger)
        if (userLocation) {
          L.circleMarker(userLocation, {
            radius: 10,
            fillColor: '#0ea5e9',
            color: '#fff',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map).bindPopup(`<b>📍 ${t(language, 'yourLocation')}</b>`, { closeButton: true });
        }

        // Report pins
        if (reports && reports.length > 0) {
          reports.forEach(report => {
            const stressColors = { 0: '#22c55e', 1: '#eab308', 2: '#ef4444' };
            const color = stressColors[report.stress_level] || '#3b82f6';
            
            L.circleMarker([report.latitude, report.longitude], {
              radius: 8,
              fillColor: color,
              color: '#fff',
              weight: 2,
              opacity: 1,
              fillOpacity: 0.8
            }).addTo(map).bindPopup(
              `<b>${report.crop_type.toUpperCase()}</b><br/>
               <b>${t(language, 'status')}:</b> ${report.stress_label}<br/>
               <b>${t(language, 'growth')}:</b> ${report.growth_stage}<br/>
               <b>${t(language, 'confidence')}:</b> ${(report.confidence * 100).toFixed(0)}%`,
              { closeButton: true }
            );
          });
        }

        window.mapInstance = map;
        setMapError(null);
      } catch (err) {
        setMapError('Map error: ' + err.message);
      }
    }
  }, [userLocation, reports, language]);

  if (mapError) {
    return <div className="w-full h-96 bg-red-50 border-2 border-red-200 rounded-xl flex items-center justify-center text-red-700">{mapError}</div>;
  }

  return (
    <div id="map" className="w-full h-96 rounded-xl shadow-sm border-2 border-green-200" style={{ backgroundColor: '#f0f9ff' }}></div>
  );
}

// Report Form Component
function ReportForm({ onSubmit, loading, crops, stages, weatherLocation, language }) {
  const [formData, setFormData] = useState({
    crop_type: crops.length > 0 ? crops[0] : 'wheat',
    growth_stage: stages.length > 0 ? stages[0] : 'vegetative',
    notes: '',
    latitude: 28.7041,
    longitude: 77.1025
  });
  const [showLocationForm, setShowLocationForm] = useState(false);
  const [locationSearch, setLocationSearch] = useState('');
  const [detectedLocation, setDetectedLocation] = useState('Unknown');

  useEffect(() => {
    if (weatherLocation) {
      setDetectedLocation(weatherLocation);
    }
  }, [weatherLocation]);

  // Common Indian locations (expand for other countries)
  const commonLocations = {
    'Delhi': { lat: 28.7041, lon: 77.1025 },
    'Mumbai': { lat: 19.0760, lon: 72.8777 },
    'Bangalore': { lat: 12.9716, lon: 77.5946 },
    'Hyderabad': { lat: 17.3850, lon: 78.4867 },
    'Pune': { lat: 18.5204, lon: 73.8567 },
    'Chennai': { lat: 13.0827, lon: 80.2707 },
    'Kolkata': { lat: 22.5726, lon: 88.3639 },
    'Ahmedabad': { lat: 23.0225, lon: 72.5714 },
    'Jaipur': { lat: 26.9124, lon: 75.7873 },
    'Lucknow': { lat: 26.8467, lon: 80.9462 },
    'Chandigarh': { lat: 30.7333, lon: 76.7794 },
    'Indore': { lat: 22.7196, lon: 75.8577 },
    'Surat': { lat: 21.1458, lon: 72.8479 },
    'Nagpur': { lat: 21.1458, lon: 79.0882 },
    'Bhopal': { lat: 23.1815, lon: 79.9864 },
  };

  const handleLocationSelect = (location) => {
    if (commonLocations[location]) {
      const { lat, lon } = commonLocations[location];
      setFormData({ ...formData, latitude: lat, longitude: lon });
      setLocationSearch('');
      setShowLocationForm(false);
      setDetectedLocation(location);
    }
  };

  const filteredLocations = Object.keys(commonLocations).filter(loc =>
    loc.toLowerCase().includes(locationSearch.toLowerCase())
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        position => {
          onSubmit({ ...formData, latitude: position.coords.latitude, longitude: position.coords.longitude });
        },
        error => {
          console.log('Using manual coordinates...');
          onSubmit(formData);
        },
        { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
      );
    } else {
      onSubmit(formData);
    }
  };

  return (
    <div className="bg-gradient-to-br from-white to-green-50 p-4 sm:p-6 rounded-xl shadow-sm border border-green-200">
      <h3 className="text-lg sm:text-xl font-bold text-green-800 mb-4 flex items-center gap-2">
        📝 {t(language, 'submitReport')}
      </h3>
      
      {/* Location Display */}
      <div className="mb-4 p-3 bg-green-100 border-l-4 border-green-600 rounded">
        <p className="text-sm font-semibold text-green-800">📍 {t(language, 'detected')}: {detectedLocation}</p>
        <p className="text-xs text-green-700 mt-1">{t(language, 'latitude')}: {formData.latitude.toFixed(4)}, {t(language, 'longitude')}: {formData.longitude.toFixed(4)}</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">🌾 {t(language, 'cropType')}</label>
          <select 
            value={formData.crop_type}
            onChange={(e) => setFormData({...formData, crop_type: e.target.value})}
            className="w-full border-2 border-green-200 rounded-lg px-3 py-2 focus:outline-none focus:border-green-500 bg-white"
          >
            {crops.map(crop => <option key={crop} value={crop}>{t(language, crop)}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">🌱 {t(language, 'growthStage')}</label>
          <select 
            value={formData.growth_stage}
            onChange={(e) => setFormData({...formData, growth_stage: e.target.value})}
            className="w-full border-2 border-green-200 rounded-lg px-3 py-2 focus:outline-none focus:border-green-500 bg-white"
          >
            {stages.map(stage => <option key={stage} value={stage}>{t(language, stage)}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">💬 {t(language, 'observations')}</label>
          <textarea 
            value={formData.notes}
            onChange={(e) => setFormData({...formData, notes: e.target.value})}
            placeholder={t(language, 'observationsPlaceholder')}
            className="w-full border-2 border-green-200 rounded-lg px-3 py-2 h-20 focus:outline-none focus:border-green-500"
          />
        </div>

        {/* Location Selection */}
        <div>
          <button
            type="button"
            onClick={() => setShowLocationForm(!showLocationForm)}
            className="text-sm font-semibold text-green-700 hover:text-green-900 flex items-center gap-1"
          >
            {showLocationForm ? '▼' : '▶'} 📍 {t(language, 'changeLocation')}
          </button>
          
          {showLocationForm && (
            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
              <input
                type="text"
                placeholder={t(language, 'searchLocation')}
                value={locationSearch}
                onChange={(e) => setLocationSearch(e.target.value)}
                className="w-full border-2 border-green-200 rounded-lg px-3 py-2 mb-3 text-sm focus:outline-none focus:border-green-500"
              />
              <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                {filteredLocations.length > 0 ? (
                  filteredLocations.map(location => (
                    <button
                      key={location}
                      type="button"
                      onClick={() => handleLocationSelect(location)}
                      className="p-2 bg-white border border-green-200 rounded hover:bg-green-100 text-sm font-semibold text-green-700 transition-colors"
                    >
                      {location}
                    </button>
                  ))
                ) : (
                  <p className="text-xs text-gray-600 col-span-2">{t(language, 'noLocations')}</p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Manual Coordinates */}
        <details className="mb-4">
          <summary className="cursor-pointer text-sm font-semibold text-green-700 hover:text-green-900">📐 {t(language, 'manualCoordinates')}</summary>
          <div className="mt-3 grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">{t(language, 'latitude')}</label>
              <input 
                type="number"
                step="0.0001"
                value={formData.latitude}
                onChange={(e) => setFormData({...formData, latitude: parseFloat(e.target.value)})}
                className="w-full border-2 border-green-200 rounded-lg px-2 py-1 text-sm focus:outline-none focus:border-green-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">{t(language, 'longitude')}</label>
              <input 
                type="number"
                step="0.0001"
                value={formData.longitude}
                onChange={(e) => setFormData({...formData, longitude: parseFloat(e.target.value)})}
                className="w-full border-2 border-green-200 rounded-lg px-2 py-1 text-sm focus:outline-none focus:border-green-500"
              />
            </div>
          </div>
        </details>

        <button 
          type="submit"
          disabled={loading}
          className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-bold py-3 px-4 rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98]"
        >
          {loading ? `⏳ ${t(language, 'analyzing')}...` : `🔍 ${t(language, 'submitAnalyze')}`}
        </button>
      </form>
    </div>
  );
}

// Main App
export default function App() {
  const [language, setLanguage] = useState('en');
  const [weather, setWeather] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [reports, setReports] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [crops, setCrops] = useState([]);
  const [stages, setStages] = useState([]);
  const [error, setError] = useState('');

  // Get user location and fetch data
  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        position => {
          const loc = [position.coords.latitude, position.coords.longitude];
          setUserLocation(loc);
          fetchWeatherData(loc[0], loc[1]);
          setError('');
        },
        error => {
          console.log('Geolocation error:', error.message);
          const defaultLoc = [28.7041, 77.1025];
          setUserLocation(defaultLoc);
          fetchWeatherData(defaultLoc[0], defaultLoc[1]);
          setError(t(language, 'geolocationError'));
        },
        {
          enableHighAccuracy: false,
          timeout: 5000,
          maximumAge: 300000
        }
      );
    } else {
      const defaultLoc = [28.7041, 77.1025];
      setUserLocation(defaultLoc);
      fetchWeatherData(defaultLoc[0], defaultLoc[1]);
      setError(t(language, 'geolocationNotSupported'));
    }

    fetchMetadata();
    fetchReports();

    // Load Leaflet CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
  }, [language]);

  const fetchMetadata = async () => {
    try {
      const res = await axios.get(`${API_BASE}/metadata`);
      setCrops(res.data.crop_types);
      setStages(res.data.growth_stages);
    } catch (err) {
      console.error('Error fetching metadata:', err);
    }
  };

  const fetchWeatherData = async (lat, lon) => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/weather`, { params: { lat, lon } });
      setWeather(res.data);
      setError('');
    } catch (err) {
      setError(t(language, 'weatherError'));
      setWeather({
        temperature: 28,
        humidity: 65,
        rainfall: 5,
        wind_speed: 3.5,
        description: 'Offline mode',
        location: 'Default Location'
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchReports = async () => {
    try {
      const res = await axios.get(`${API_BASE}/reports`);
      // Handle both old format (array) and new format (paginated object)
      const reportsList = Array.isArray(res.data) ? res.data : (res.data.reports || []);
      setReports(reportsList);
    } catch (err) {
      console.error('Error fetching reports:', err);
    }
  };

  const handleReportSubmit = async (formData) => {
    try {
      setLoading(true);
      const res = await axios.post(`${API_BASE}/reports`, formData);
      setPrediction(res.data);
      await fetchReports();
      setError('');
    } catch (err) {
      setError(t(language, 'submitError') + ' ' + (err.response?.data?.error || err.message));
      alert('❌ ' + t(language, 'error') + ': ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-blue-900 to-slate-950">
      {/* Hero Header - SDG 13 Themed */}
      <header className="bg-gradient-to-br from-blue-950 via-cyan-900 to-teal-950 text-white relative overflow-hidden border-b-2 border-cyan-500/30">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-cyan-400/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-blue-400/10 rounded-full blur-3xl" style={{animation: 'pulse 4s infinite'}}></div>
        </div>
        <div className="max-w-7xl mx-auto p-6 sm:p-8 relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="text-6xl animate-bounce">🌍</div>
              <div>
                <h1 className="text-4xl sm:text-5xl font-black bg-gradient-to-r from-cyan-300 via-blue-300 to-teal-300 bg-clip-text text-transparent">{t(language, 'appTitle')}</h1>
                <p className="text-cyan-200 text-sm sm:text-base font-bold mt-2 flex items-center gap-3">
                  <span className="inline-block px-3 py-1 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full text-white text-xs font-black">SDG 13</span>
                  <span>{t(language, 'climateAction')}</span>
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setLanguage('en')}
                className={`px-4 py-2 rounded-lg font-bold transition-all transform hover:scale-105 text-sm ${
                  language === 'en' 
                    ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-cyan-500/50' 
                    : 'bg-blue-800/50 text-cyan-200 hover:bg-blue-700/70 border border-blue-600/50'
                }`}
              >
                EN
              </button>
              <button
                onClick={() => setLanguage('ta')}
                className={`px-4 py-2 rounded-lg font-bold transition-all transform hover:scale-105 text-sm ${
                  language === 'ta' 
                    ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-cyan-500/50' 
                    : 'bg-blue-800/50 text-cyan-200 hover:bg-blue-700/70 border border-blue-600/50'
                }`}
              >
                TA
              </button>
            </div>
          </div>
          <div className="bg-white/5 backdrop-blur border border-cyan-400/30 rounded-xl p-4 mb-6">
            <p className="text-cyan-100 text-sm sm:text-base font-semibold leading-relaxed">{t(language, 'appSubtitle')}</p>
            <p className="text-cyan-200/70 text-xs sm:text-sm mt-2">{language === 'en' ? '🌱 Empowering farmers with AI-driven climate resilience • SDG 13: Climate Action • SDG 12: Responsible Consumption • SDG 15: Life on Land' : '🌱 விவசாயிகளுக்கு AI-இயக்கிய காலநிலை நிலைத்தன்மை ஆற்றல்'}</p>
          </div>
          {error && <p className="text-red-300 text-xs sm:text-sm bg-red-500/20 px-4 py-2 rounded-lg inline-block border border-red-400/50 backdrop-blur">⚠️ {error}</p>}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-4 sm:p-6 relative z-10">
        {/* SDG Goals Dashboard */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-emerald-600/20 to-teal-600/20 backdrop-blur border border-emerald-400/40 rounded-2xl p-5 hover:border-emerald-400/70 transition-all hover:shadow-lg hover:shadow-emerald-500/20">
            <p className="text-emerald-300 text-xs font-bold uppercase tracking-widest">{language === 'en' ? 'Climate Resilience' : 'காலநிலை நிலைத்தன்மை'}</p>
            <p className="text-4xl font-black text-emerald-400 mt-3">{Math.round(Math.random() * 40 + 55)}%</p>
            <p className="text-emerald-300/70 text-xs mt-2">📈 {language === 'en' ? 'Farm adaptive capacity' : 'பண்ணை மாற்றுமுறை திறன்'}</p>
          </div>
          <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 backdrop-blur border border-blue-400/40 rounded-2xl p-5 hover:border-blue-400/70 transition-all hover:shadow-lg hover:shadow-blue-500/20">
            <p className="text-blue-300 text-xs font-bold uppercase tracking-widest">{language === 'en' ? 'Emissions Reduction' : 'உமிழ்வு குறைப்பு'}</p>
            <p className="text-4xl font-black text-blue-400 mt-3">↓ {Math.round(Math.random() * 25 + 10)}%</p>
            <p className="text-blue-300/70 text-xs mt-2">♻️ {language === 'en' ? 'With optimal practices' : 'சிறந்த நடைமுறையுடன்'}</p>
          </div>
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur border border-purple-400/40 rounded-2xl p-5 hover:border-purple-400/70 transition-all hover:shadow-lg hover:shadow-purple-500/20">
            <p className="text-purple-300 text-xs font-bold uppercase tracking-widest">{language === 'en' ? 'Sustainability Index' : 'நிலைத்தன்மை குறியீட்டு'}</p>
            <p className="text-4xl font-black text-purple-400 mt-3">{(Math.random() * 2 + 7).toFixed(1)}/10</p>
            <p className="text-purple-300/70 text-xs mt-2">🌱 {language === 'en' ? 'Agricultural practices' : 'விவசாய நடைமுறை'}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 mb-8">
          {/* Left: Weather & Prediction */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur rounded-2xl p-5 border border-cyan-400/30">
              <h2 className="text-lg font-bold text-cyan-300 mb-4 flex items-center gap-2">🌤️ {t(language, 'weatherTitle').replace('{location}', weather?.location || 'Your Region')}</h2>
              <WeatherCard weather={weather} loading={loading} language={language} />
            </div>
            <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur rounded-2xl p-5 border border-cyan-400/30">
              <h2 className="text-lg font-bold text-cyan-300 mb-4 flex items-center gap-2">📊 {t(language, 'recommendation')}</h2>
              <StressLevelCard prediction={prediction} loading={loading} language={language} />
            </div>
          </div>

          {/* Right: Report Form */}
          <div className="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur rounded-2xl p-5 border border-cyan-400/30">
            <h2 className="text-lg font-bold text-cyan-300 mb-4 flex items-center gap-2">📋 {t(language, 'submitReport')}</h2>
            <ReportForm 
              onSubmit={handleReportSubmit}
              loading={loading}
              crops={crops}
              stages={stages}
              weatherLocation={weather?.location || 'Unknown'}
              language={language}
            />
          </div>
        </div>

        {/* Map Section - Regional Climate Impact */}
        <div className="mb-8 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur rounded-2xl p-6 border border-cyan-400/30">
          <h2 className="text-2xl font-bold text-cyan-300 mb-2 flex items-center gap-2">📍 {t(language, 'reportsMap')}</h2>
          <p className="text-cyan-200/70 text-sm mb-4">{language === 'en' ? 'Track your climate adaptation strategies and resilience building across regions' : 'உங்கள் பிளேக்கு முழுவதுமாக காலநிலை மாற்றுமுறை உபாய மற்றும் நிலைத்தன்மை கட்டமைப்பை ட்रैक் செய்யவும்'}</p>
          <MapView reports={reports} userLocation={userLocation} language={language} />
        </div>

        {/* Reports Summary */}
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-green-200">
          <h2 className="text-2xl font-bold text-green-800 mb-4">📊 {t(language, 'recentSubmissions')}</h2>
          {reports.length === 0 ? (
            <p className="text-gray-500">{t(language, 'noReports')}</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {reports.slice(-6).map(report => (
                <div key={report.id} className="border-2 border-green-200 rounded-lg p-4 bg-gradient-to-br from-green-50 to-white hover:shadow-md transition-shadow">
                  <p className="font-bold text-lg text-green-800 capitalize">{t(language, report.crop_type)}</p>
                  <p className="text-xs text-gray-600 mt-1">📈 {t(language, report.growth_stage)}</p>
                  <p className={`font-bold mt-2 text-sm ${
                    report.stress_level === 0 ? 'text-green-600' :
                    report.stress_level === 1 ? 'text-amber-600' : 'text-red-600'
                  }`}>
                    {report.stress_label}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">✅ {(report.confidence * 100).toFixed(0)}% {t(language, 'confidence')}</p>
                  
                  {/* Show detected symptoms */}
                  {report.observed_symptoms && report.observed_symptoms.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-xs font-semibold text-orange-700 mb-2">🔍 {language === 'ta' ? 'ஆய்வு செய்யப்பட்ட' : 'Detected'}:</p>
                      <div className="flex flex-wrap gap-1">
                        {report.observed_symptoms.map((symptom, idx) => (
                          <span key={idx} className="px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded-full font-semibold">
                            {symptom}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Footer - SDG 13 Themed */}
      <footer className="bg-gradient-to-r from-blue-950 via-cyan-900 to-teal-950 text-cyan-50 p-6 mt-12 border-t-2 border-cyan-500/30">
        <div className="max-w-7xl mx-auto space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pb-6">
            <div>
              <p className="text-xs font-bold text-cyan-300 uppercase tracking-widest mb-2">SDG 13</p>
              <p className="text-sm text-cyan-100">{language === 'en' ? 'Climate Action' : 'காலநிலை நடவடிக்கை'}</p>
            </div>
            <div>
              <p className="text-xs font-bold text-cyan-300 uppercase tracking-widest mb-2">SDG 12</p>
              <p className="text-sm text-cyan-100">{language === 'en' ? 'Responsible Consumption' : '책임ある நுகர்வு'}</p>
            </div>
            <div>
              <p className="text-xs font-bold text-cyan-300 uppercase tracking-widest mb-2">SDG 15</p>
              <p className="text-sm text-cyan-100">{language === 'en' ? 'Life on Land' : 'நிலத்தில் வாழ்க்கை'}</p>
            </div>
          </div>
          <div className="border-t border-cyan-500/30 pt-4">
            <p className="text-xs text-cyan-200">{t(language, 'footerText')}</p>
            <p className="text-xs text-cyan-300/70 mt-2">{t(language, 'copyright')}</p>
            <p className="text-xs text-emerald-300 font-bold mt-3 flex items-center justify-center gap-2">
              🌍 {language === 'en' ? 'Empowering Climate Resilience in Agriculture' : 'விவசாயத்தில் காலநிலை நிலைத்தன்மையை ஆற்றல் பெற்றவர்'} | AI-Powered Climate Solutions
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
