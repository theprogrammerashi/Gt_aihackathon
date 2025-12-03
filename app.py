import streamlit as st
import time
from PIL import Image
from streamlit_option_menu import option_menu
from services import CreativeEngine

# CONFIG
st.set_page_config(page_title="GT Creative Studio", layout="wide", page_icon="📸")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- ICONS ---
class Icons:
    brain = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00CC96" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M3 9a2 2 0 0 1 2-2h.93a2 2 0 0 0 1.664-.89l.812-1.22A2 2 0 0 1 10.07 4h3.86a2 2 0 0 1 1.664.89l.812 1.22A2 2 0 0 0 18.07 7H19a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9z"/></svg>"""
    layers = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>"""

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        {Icons.brain}
        <h2 style="margin:0; font-size: 1.1rem; color: #fff;">GT Studio</h2>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Studio", "Asset Library"],
        icons=["palette", "folder"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "14px"},
            "nav-link-selected": {"background-color": "#00CC96", "color": "#000"}
        }
    )
    
    st.markdown("---")
    st.success("System Online v2.2")

# --- PAGE 1: STUDIO ---
if selected == "Studio":
    st.title("Auto-Creative Engine")
    
    # INPUT PANEL
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 2])
    
    with c1:
        st.caption("1. BRAND LOGO")
        logo_file = st.file_uploader("Upload Logo", type=['png', 'jpg'], key="logo")
    with c2:
        st.caption("2. PRODUCT SHOT")
        prod_file = st.file_uploader("Upload Product", type=['png', 'jpg', 'jpeg'], key="prod")
    with c3:
        st.caption("3. CONTEXT")
        brand_name = st.text_input("Brand Name", "Lumina")
        user_context = st.text_input("Additional Context", placeholder="AI will analyze image...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("🚀 GENERATE CAMPAIGNS", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # OUTPUT SECTION
    if generate:
        engine = CreativeEngine()
        status_box = st.empty()
        
        # 1. Vision
        visual_context = ""
        if prod_file:
            status_box.info("Analyzing Product Visuals")
            img = Image.open(prod_file)
            visual_context = engine.analyze_product_visuals(img)
        else:
            visual_context = user_context or "Generic product"

        # 2. Generation
        status_box.info("Generating High-Fidelity Variations & Saving to Library...")
        campaigns = engine.generate_campaigns(brand_name, visual_context, logo_present=bool(logo_file))
        
        
        if engine.is_mock:
            st.warning(" API Quota Exceeded or Error. Displaying Backup/Demo Data.")
        else:
            status_box.success("Generation Complete & Assets Saved!")
            
        st.session_state['results'] = campaigns
    # GALLERY
    if 'results' in st.session_state:
        campaigns = st.session_state['results']
        
        st.subheader(f"Generated Assets ({len(campaigns)})")
        
        # Grid 
        cols = st.columns(2)
        for i, item in enumerate(campaigns):
            col = cols[i % 2] 
            with col:
                st.markdown(f"""
                <div class="variation-card">
                    <div class="card-image-container">
                        <img src="{item['image_url']}" style="width:100%; height:100%; object-fit: cover;">
                        <div class="theme-badge">{item['theme']}</div>
                    </div>
                    <div class="card-content">
                        <h4 style="color:{item['hex_accent']}; margin:0 0 8px 0;">{item['headline']}</h4>
                        <p style="font-size:0.9rem; margin:0; opacity: 0.8;">{item['caption']}</p>
                    </div>
                </div>
                <div style="margin-bottom: 20px;"></div>
                """, unsafe_allow_html=True)

        # DOWNLOAD
        st.markdown("---")
        c_dl, _ = st.columns([1, 3])
        with c_dl:
            engine = CreativeEngine()
            zip_bytes = engine.package_assets(campaigns)
            st.download_button(
                "DOWNLOAD ALL ASSETS (.ZIP)",
                data=zip_bytes,
                file_name=f"{brand_name}_Assets.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )

#  PAGE 2
elif selected == "Asset Library":
    st.title("Digital Asset Management")
    st.markdown("Repository of all AI-generated creative assets.")
    
    engine = CreativeEngine()
    assets = engine.get_library_assets()
    
    if assets:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for i, file_path in enumerate(assets):
            col = cols[i % 4]
            with col:
                st.image(file_path, use_container_width=True)
                st.caption(file_path.split(os.sep)[-1])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No assets generated yet. Go to Studio to create some!")