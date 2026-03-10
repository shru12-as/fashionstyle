# AI Style Recommendation System

A modern, full-stack AI-powered fashion assistant. Upload an image to receive personalized clothing, footwear, and jewelry recommendations based on your face shape, skin tone, and vibe. It also includes an AI chatbot for instant styling advice.

## Tech Stack
- **Frontend**: HTML5, TailwindCSS (CDN), Vanilla JavaScript
- **Backend**: Python 3, FastAPI, SQLAlchemy (SQLite)
- **AI Integration**: Groq API (`llama-3.2-90b-vision-preview` for images & `llama-3.3-70b-versatile` for chat)

---

## 🚀 Step-by-Step Setup Instructions

### 1. Backend Setup
1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. By default, a virtual environment (`venv`) should be created. If not, create activation:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows PowerShell**: `.\venv\Scripts\Activate.ps1`
   - **Windows CMD**: `.\venv\Scripts\activate.bat`
   - **Mac/Linux**: `source venv/bin/activate`
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: if requirements.txt isn't present, the dependencies are: `fastapi uvicorn groq python-multipart sqlalchemy pydantic opencv-python-headless python-dotenv`)*
5. **Configure the AI (CRITICAL)**:
   - Open the `backend/.env` file.
   - Replace `your_groq_api_key_here` with your actual Groq API key:
     ```env
     GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
     ```
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *The API will be available at `http://localhost:8000`*

### 2. Frontend Setup
1. In a separate terminal or simply using your file explorer, open the `frontend` folder.
2. Because the app uses webcam and API requests fetching from another origin, it is best to run it through a local web server (instead of double-clicking the HTML files directly). You can use Python's built-in server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## ✨ Usage Guide
- Click **Start Style Analysis** or **Try It Now** on the homepage.
- **Use Camera**: Grant browser permissions to capture a live photo of yourself.
- **Upload Photo**: Alternatively, upload a full-body or portrait photo from your device.
- Click **Analyze Style**. Enjoy the real-time AI breakdown of your profile.
- Checkout the curated **Outfit, Footwear, and Jewelry** suggestions, complete with external shop links!
- Need quick advice? Open the **Style Assistant** floating chat icon on the bottom right and ask questions like, *"What colors look best on warm skin tones?"*
