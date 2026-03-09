import streamlit as st
from PIL import Image
import utils.gemini_service as gs

# Configure page layout and aesthetics
st.set_page_config(
    page_title="StyleMinds: AI Fashion Stylist",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a premium look
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f0f6fc;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .main-title {
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #ff6b6b, #c0392b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #bb86fc 0%, #3700b3 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(187, 134, 252, 0.4);
        color: white;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #21262d;
        border: 1px solid #30363d;
        color: white;
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
    .stTextArea>div>div>textarea {
        background-color: #21262d;
        border: 1px solid #30363d;
        color: white;
        border-radius: 6px;
    }

    /* Cards/Containers */
    .st-emotion-cache-1cvow4s, .st-emotion-cache-1wf38xo {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* File Uploader tweaks */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #30363d;
        background-color: #0d1117;
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border-color: #30363d;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "api_configured" not in st.session_state:
        # Initialize Gemini API
        st.session_state.api_configured = gs.configure_gemini()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'trends' not in st.session_state:
        if st.session_state.api_configured:
             with st.spinner("Fetching latest fashion trends..."):
                st.session_state.trends = gs.get_current_trends()
        else:
             st.session_state.trends = "Trends unavailable due to missing API key."

def render_sidebar():
    """Render the application sidebar navigation."""
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Explore your personalized AI stylist.")
    
    page = st.sidebar.radio(
        "Choose a feature:",
        ["Home & Trends", "Visual Outfit Builder", "Personal Stylist Consult"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Powered by Google Gemini ✦")
    return page

def render_home_page():
    """Render the landing page with trends."""
    st.markdown("<h1 class='main-title'>StyleMinds AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8b949e; margin-bottom: 2rem;'>Your Personal Generative Fashion Director</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Welcome to the Future of Styling")
        st.write("""
        Discover outfits that actually fit your aesthetic, lifestyle, and wardrobe.
        StyleMinds uses advanced vision and generative AI to understand your unique
        look and propose intelligent, trend-aware recommendations.
        """)
        st.info("👈 Use the sidebar to try our features: upload a clothing item to build an outfit around it, or chat with your virtual stylist.")

    with col2:
         st.markdown("### 🔥 Current Global Trends")
         if 'trends' in st.session_state:
             st.info(st.session_state.trends)
         else:
             st.write("Loading trends...")


def render_visual_builder_page():
    """Render the image upload and analysis page."""
    st.markdown("## 📸 Visual Outfit Builder")
    st.write("Upload a photo of a clothing item (e.g., a jacket, a pair of sneakers) and I will build 3 complete cohesive outfits around it.")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        uploaded_file = st.file_uploader("Upload an item picture...", type=["jpg", "jpeg", "png"])
        context = st.text_input("Any specific occasion/style? (Optional)", placeholder="e.g., 'For a casual office day', or 'Streetwear vibe'")
        
        analyze_btn = False
        if uploaded_file is not None:
             image = Image.open(uploaded_file)
             st.image(image, caption="Your Item", use_container_width=True)
             
             analyze_btn = st.button("Generate Outfits ✨", use_container_width=True)
             
    with col2:
        if uploaded_file is not None and analyze_btn:
             if not st.session_state.api_configured:
                  st.error("API Key not found or invalid. Please check `.streamlit/secrets.toml`.")
             else:
                  with st.spinner("Analyzing style and crafting looks..."):
                       # Pass the PIL Image directly to our helper
                       recommendation = gs.get_outfit_recommendation_from_image(image, context)
                       st.success("Analysis Complete!")
                       st.markdown(recommendation)
        elif uploaded_file is None:
             st.info("Upload a photo to see AI-generated outfits.")


def render_personal_stylist_page():
    """Render the personalized advice consultation page."""
    st.markdown("## 💬 Personal Style Consultation")
    st.write("Tell your AI stylist what you're looking for, your body type, color preferences, or an upcoming event.")

    with st.form("styling_form"):
         occasion = st.text_input("What is the occasion?", placeholder="e.g., 'Summer wedding guest', 'Tech conference'")
         preferences = st.text_area("Describe your style preferences, constraints, or what you need:", 
                                   placeholder="e.g., 'I want a smart-casual look. I prefer dark colors, mostly navy and black, and I want it to be comfortable but edgy.'",
                                   height=150)
         
         submit_button = st.form_submit_button("Get Styling Advice ✦")
         
    if submit_button:
         if not preferences:
              st.warning("Please describe what you're looking for.")
         elif not st.session_state.api_configured:
              st.error("API Key not found or invalid. Please check `.streamlit/secrets.toml`.")
         else:
              with st.spinner("Consulting stylist..."):
                  advice = gs.get_styling_advice(preferences, occasion)
                  st.markdown("### 👔 Stylist Recommendation")
                  st.success(advice)


def main():
    init_session_state()
    selected_page = render_sidebar()
    
    if selected_page == "Home & Trends":
        render_home_page()
    elif selected_page == "Visual Outfit Builder":
        render_visual_builder_page()
    elif selected_page == "Personal Stylist Consult":
        render_personal_stylist_page()

if __name__ == "__main__":
    main()
