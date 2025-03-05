# --- 1. Definir algunos user-agents reales para distintos sistemas (Chrome 133) ---
# --- 1. Definir User-Agents comunes ---
USER_AGENTS = {
    "Windows": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "MacOS": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.6099.199 Safari/537.36"
    ),
    "Linux": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.6099.199 Safari/537.36"
    ),
    "Android": (
        "Mozilla/5.0 (Linux; Android 13; SM-S918U) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.6167.85 Mobile Safari/537.36"
    ),
    "iPhone": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "iPad": (
        "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Firefox_Windows": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "
        "Gecko/20100101 Firefox/120.0"
    ),
    "Edge_Windows": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.6099.199 Safari/537.36 Edg/120.0.0.0"
    ),
    "IE_11": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) "
        "like Gecko"
    ),
}

# --- 2. Definir perfiles de navegador predefinidos ---
profiles = {
    "perfil_windows_EEUU": {
        "user_agent": USER_AGENTS["Windows"],
        "timezone": "America/New_York",
        "geolocation": {"lat": 40.7128, "lon": -74.0060},  # Nueva York, EE. UU.
        "languages": "en-US,en",
        "fonts": ["Arial", "Calibri", "Times New Roman"],
        "proxy": True
    },
    "perfil_linux_ES": {
        "user_agent": USER_AGENTS["Linux"],
        "timezone": "Europe/Madrid",
        "geolocation": {"lat": 41.3888, "lon": 2.1590},  # Barcelona, España
        "languages": "es-ES,es",
        "fonts": ["DejaVu Sans", "Liberation Serif", "Arial"],
        "proxy": None
    },
    "perfil_macOS_FR": {
        "user_agent": USER_AGENTS["MacOS"],
        "timezone": "Europe/Paris",
        "geolocation": {"lat": 48.8566, "lon": 2.3522},  # París, Francia
        "languages": "fr-FR,fr",
        "fonts": ["Helvetica", "Arial", "Courier"],
        "proxy": None
    },
    "perfil_android_MX": {
        "user_agent": USER_AGENTS["Android"],
        "timezone": "America/Mexico_City",
        "geolocation": {"lat": 19.4326, "lon": -99.1332},  # Ciudad de México
        "languages": "es-MX,es",
        "fonts": ["Roboto", "Noto Sans", "Arial"],
        "proxy": None
    },
    "perfil_iphone_UK": {
        "user_agent": USER_AGENTS["iPhone"],
        "timezone": "Europe/London",
        "geolocation": {"lat": 51.5074, "lon": -0.1278},  # Londres, Reino Unido
        "languages": "en-GB,en",
        "fonts": ["San Francisco", "Helvetica", "Arial"],
        "proxy": None
    },
    "perfil_firefox_windows_CA": {
        "user_agent": USER_AGENTS["Firefox_Windows"],
        "timezone": "America/Toronto",
        "geolocation": {"lat": 43.65107, "lon": -79.347015},  # Toronto, Canadá
        "languages": "en-CA,en",
        "fonts": ["Verdana", "Times New Roman", "Tahoma"],
        "proxy": None
    },
    "perfil_edge_windows_AUS": {
        "user_agent": USER_AGENTS["Edge_Windows"],
        "timezone": "Australia/Sydney",
        "geolocation": {"lat": -33.8688, "lon": 151.2093},  # Sídney, Australia
        "languages": "en-AU,en",
        "fonts": ["Segoe UI", "Arial", "Tahoma"],
        "proxy": None
    },
    "perfil_ipad_IT": {
        "user_agent": USER_AGENTS["iPad"],
        "timezone": "Europe/Rome",
        "geolocation": {"lat": 41.9028, "lon": 12.4964},  # Roma, Italia
        "languages": "it-IT,it",
        "fonts": ["San Francisco", "Arial", "Courier"],
        "proxy": None
    },
    "perfil_IE11_windows_BR": {
        "user_agent": USER_AGENTS["IE_11"],
        "timezone": "America/Sao_Paulo",
        "geolocation": {"lat": -23.5505, "lon": -46.6333},  # São Paulo, Brasil
        "languages": "pt-BR,pt",
        "fonts": ["Times New Roman", "Arial", "Verdana"],
        "proxy": None
    },
}

# Puede agregar más perfiles según las necesidades


# --- 3. Script de inyección JavaScript para modificar WebGL, Canvas, Audio, etc. ---
# Este script se ejecutará en cada nueva página antes de cualquier script de la web (Page.addScriptToEvaluateOnNewDocument).
stealth_script = r"""
// Función de ayuda para sobreeescribir propiedades de solo-lectura de navigator
function overrideNavigatorProp(prop, value) {
    try {
        Object.defineProperty(navigator, prop, {
            get: () => value,
            configurable: true
        });
    } catch(e) {
        console.warn("No se pudo sobreescribir navigator." + prop, e);
    }
}

// 1. Spoof de Canvas: alterar ligeramente huella del canvas
const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function(...args) {
    // Opcional: modificar pixeles antes de obtener dataURL para cambiar fingerprint.
    // (Por simplicidad, aquí devolvemos el canvas sin cambios reales)
    return origToDataURL.apply(this, args);
};
const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
    // Opcional: introducir leves variaciones en los píxeles del canvas
    // (Ejemplo: cambiar el valor de un píxel de cada 100 para ruido imperceptible)
    let imageData = origGetImageData.call(this, x, y, w, h);
    // Aquí podría modificar imageData.data para alterar la imagen mínimamente.
    return imageData;
};

// 2. Spoof de WebGL: ocultar GPU real (vendor/renderer) en WebGL
const origGetParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(param) {
    // Constantes WebGL para vendor/renderer sin máscara (WebGL debug extension)
    const UNMASKED_VENDOR = 0x9245;
    const UNMASKED_RENDERER = 0x9246;
    if (param === UNMASKED_VENDOR) {
        return "Intel Inc.";    // Valor ficticio de fabricante GPU
    }
    if (param === UNMASKED_RENDERER) {
        return "Intel Iris Xe Graphics";  // Valor ficticio de modelo GPU
    }
    return origGetParameter.call(this, param);
};

// 3. Spoof de Audio: homogenizar huella de AudioContext
if (window.AudioContext || window.webkitAudioContext) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const origGain = AudioCtx.prototype.createGain;
    AudioCtx.prototype.createGain = function() {
        const gainNode = origGain.call(this);
        // Sobrescribir método que se usa en fingerprint de audio (DynamicsCompressor)
        const origComp = gainNode.context.createDynamicsCompressor;
        gainNode.context.createDynamicsCompressor = function() {
            const comp = origComp.call(this);
            // Sobrescribir método getFloatFrequencyData del AnalyserNode
            const origGetFloatData = AnalyserNode.prototype.getFloatFrequencyData;
            AnalyserNode.prototype.getFloatFrequencyData = function(array) {
                // Rellenar array con valores constantes o ligeramente aleatorios
                // para camuflar la firma de audio. Aquí simplemente añadimos un offset fijo.
                origGetFloatData.call(this, array);
                for (let i = 0; i < array.length; i++) {
                    array[i] += 0.1;  // pequeño desplazamiento
                }
            };
            return comp;
        };
        return gainNode;
    };
}

// 4. Otras propiedades de navigator a modificar para coherencia
// (Ejemplos: idioma, plataforma, zona horaria si no se usan métodos CDP, hardwareConcurrency)
overrideNavigatorProp('languages', ['es-ES', 'es']);  // Idiomas preferidos (ejemplo)
overrideNavigatorProp('platform', 'Win32');           // Plataforma (ej: Win32, Linux x86_64, MacIntel según perfil)
overrideNavigatorProp('webdriver', undefined);        // Eliminar bandera webdriver (automatización)
"""
# Nota: El script anterior realiza modificaciones sencillas. En un caso real se puede
# ajustar para que los valores ficticios concuerden exactamente con el perfil deseado
# (por ejemplo, vendor GPU acorde al SO simulado, idiomas acorde a locale, etc.).
