// --- Elements ---
const btnCamera = document.getElementById('btn-camera');
const fileUpload = document.getElementById('file-upload');
const cameraFeed = document.getElementById('camera-feed');
const cameraCanvas = document.getElementById('camera-canvas');
const uploadUI = document.getElementById('upload-ui');
const cameraControls = document.getElementById('camera-controls');
const btnCapture = document.getElementById('btn-capture');
const btnCancelCamera = document.getElementById('btn-cancel-camera');
const previewUI = document.getElementById('preview-ui');
const imagePreview = document.getElementById('image-preview');
const btnRetake = document.getElementById('btn-retake');
const btnAnalyze = document.getElementById('btn-analyze');

const uploadSection = document.getElementById('upload-section');
const loadingState = document.getElementById('loading-state');
const resultsSection = document.getElementById('results-section');

const tabWomen = document.getElementById('tab-women');
const tabMen = document.getElementById('tab-men');
const galleryWomen = document.getElementById('gallery-women');
const galleryMen = document.getElementById('gallery-men');
const galleryImages = document.querySelectorAll('.gallery-img');

// --- Global state ---
let stream = null;
let currentFile = null;

// --- Config ---
const API_BASE = 'http://127.0.0.1:8000/api';

// --- Tab Logic ---
tabWomen.addEventListener('click', () => {
    tabWomen.classList.add('bg-white/20', 'text-white');
    tabWomen.classList.remove('text-gray-400');
    tabMen.classList.remove('bg-white/20', 'text-white');
    tabMen.classList.add('text-gray-400');
    galleryWomen.classList.remove('hidden');
    galleryMen.classList.add('hidden');
});

tabMen.addEventListener('click', () => {
    tabMen.classList.add('bg-white/20', 'text-white');
    tabMen.classList.remove('text-gray-400');
    tabWomen.classList.remove('bg-white/20', 'text-white');
    tabWomen.classList.add('text-gray-400');
    galleryMen.classList.remove('hidden');
    galleryWomen.classList.add('hidden');
});

// --- Gallery Logic ---
galleryImages.forEach(img => {
    img.addEventListener('click', async () => {
        try {
            // Fetch the image as a Blob
            const response = await fetch(img.src);
            const blob = await response.blob();
            currentFile = new File([blob], "gallery_image.jpg", { type: blob.type });
            showPreview(URL.createObjectURL(blob));
        } catch (err) {
            console.error("Failed to load image from gallery", err);
            alert('Failed to process the selected outfit.');
        }
    });
});

// --- Camera Logic ---
btnCamera.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraFeed.srcObject = stream;
        cameraFeed.classList.remove('hidden');
        uploadUI.classList.add('hidden');
        cameraControls.classList.remove('hidden');
        cameraFeed.play();
    } catch (err) {
        alert('Unable to access camera. Please use upload option.');
        console.error(err);
    }
});

btnCancelCamera.addEventListener('click', stopCamera);

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    cameraFeed.classList.add('hidden');
    cameraControls.classList.add('hidden');
    uploadUI.classList.remove('hidden');
}

btnCapture.addEventListener('click', () => {
    cameraCanvas.width = cameraFeed.videoWidth;
    cameraCanvas.height = cameraFeed.videoHeight;
    const ctx = cameraCanvas.getContext('2d');
    ctx.drawImage(cameraFeed, 0, 0);
    
    // Convert to blob
    cameraCanvas.toBlob((blob) => {
        currentFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
        showPreview(URL.createObjectURL(blob));
        stopCamera();
    }, 'image/jpeg', 0.9);
});

// --- Upload Logic ---
fileUpload.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
        currentFile = e.target.files[0];
        showPreview(URL.createObjectURL(currentFile));
    }
});

function showPreview(url) {
    imagePreview.src = url;
    uploadUI.classList.add('hidden');
    previewUI.classList.remove('hidden');
}

btnRetake.addEventListener('click', () => {
    currentFile = null;
    imagePreview.src = '';
    previewUI.classList.add('hidden');
    uploadUI.classList.remove('hidden');
});

// --- API Logic ---
btnAnalyze.addEventListener('click', async () => {
    if (!currentFile) return;
    
    // UI transitioning
    previewUI.classList.add('hidden');
    loadingState.classList.remove('hidden');
    
    const formData = new FormData();
    formData.append('image', currentFile);
    
    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('API Request Failed');
        
        const data = await response.json();
        renderResults(data.analysis);
        
    } catch (err) {
        console.error(err);
        alert('Failed to analyze image. Ensure backend is running.');
        loadingState.classList.add('hidden');
        uploadUI.classList.remove('hidden');
    }
});

function renderResults(analysis) {
    loadingState.classList.add('hidden');
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    
    // Populate profile summary
    document.getElementById('res-face').innerText = analysis.face_shape || 'Unknown';
    document.getElementById('res-skin').innerText = analysis.skin_tone || 'Unknown';
    document.getElementById('res-gender').innerText = analysis.gender || 'Unknown';
    document.getElementById('res-vibe').innerText = analysis.style_vibe || 'Unknown';
    
    // Populate new AI Insights
    document.getElementById('res-color').innerText = analysis.color_advice || 'No specific color advice provided.';
    document.getElementById('res-occasion').innerText = analysis.occasion_suggestions || 'No specific occasion provided.';
    
    // Populate cards
    const container = document.getElementById('recommendation-cards');
    container.innerHTML = '';
    
    const recs = analysis.recommendations || {};
    const types = ['outfit', 'footwear', 'accessories'];
    
    types.forEach(type => {
        const item = recs[type];
        if(!item) return;
        
        // Use generic placeholders mapping since we don't have e-commerce API
        const placeHolderMap = {
            'outfit': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&auto=format&fit=crop&q=60',
            'footwear': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=60',
            'accessories': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500&auto=format&fit=crop&q=60'
        };
        
        const cardHTML = `
            <div class="glass-panel rounded-2xl overflow-hidden flex flex-col hover:scale-105 transition-transform duration-300">
                <img src="${placeHolderMap[type]}" alt="${type}" class="w-full h-48 object-cover">
                <div class="p-6 flex flex-col flex-grow">
                    <span class="text-xs font-semibold uppercase tracking-wider text-primary mb-2">${type}</span>
                    <h3 class="text-lg font-bold mb-2 flex-grow">${item.name}</h3>
                    <p class="text-xl font-medium text-gray-300 mb-4">${item.price}</p>
                    <a href="https://www.amazon.in/s?k=${encodeURIComponent(item.search_query)}" target="_blank" class="w-full text-center bg-white text-dark hover:bg-gray-200 transition font-bold py-3 rounded-xl">Shop Now</a>
                </div>
            </div>
        `;
        container.innerHTML += cardHTML;
    });
}

// --- Chatbot Logic ---
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotWindow = document.getElementById('chatbot-window');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatbotToggle.addEventListener('click', () => {
    chatbotWindow.classList.remove('hidden');
    // slight delay to allow display flex to apply before transforming
    setTimeout(() => chatbotWindow.classList.add('visible'), 10);
    chatbotToggle.classList.add('scale-0');
});

chatbotClose.addEventListener('click', () => {
    chatbotWindow.classList.remove('visible');
    setTimeout(() => chatbotWindow.classList.add('hidden'), 300);
    chatbotToggle.classList.remove('scale-0');
});

function addMessage(text, isUser = false) {
    const div = document.createElement('div');
    if (isUser) {
        div.className = 'bg-primary text-white text-sm p-3 rounded-xl rounded-tr-sm self-end max-w-[80%]';
    } else {
        div.className = 'bg-white/10 text-sm p-3 rounded-xl rounded-tl-sm self-start max-w-[80%]';
    }
    div.innerText = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if(!msg) return;
    
    addMessage(msg, true);
    chatInput.value = '';
    
    // Add loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'bg-white/10 text-sm p-3 rounded-xl rounded-tl-sm self-start flex gap-1 items-center';
    loadingDiv.innerHTML = '<div class="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div><div class="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style="animation-delay: 0.2s"></div><div class="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style="animation-delay: 0.4s"></div>';
    loadingDiv.id = 'chat-loading';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        
        document.getElementById('chat-loading')?.remove();
        
        if(response.ok) {
            const data = await response.json();
            addMessage(data.reply);
        } else {
            addMessage("Sorry, I'm having trouble connecting to the server.");
        }
    } catch(err) {
        document.getElementById('chat-loading')?.remove();
        console.error(err);
        addMessage("Sorry, network error occurred.");
    }
});
