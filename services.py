import os
import requests
import zipfile
import io
import time
import random
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class CreativeEngine:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-1.5-flash"
        self.model = None
        self.library_path = "asset_library"
        self.is_mock = False
        
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"Auth Error: {e}")
                self.is_mock = True
        else:
            self.is_mock = True

    def _generate_with_retry(self, inputs, retries=3):
        for attempt in range(retries):
            try:
                return self.model.generate_content(inputs)
            except Exception as e:
                print(f"API Error: {e}")
                time.sleep(2)
        self.is_mock = True
        return None

    def analyze_product_visuals(self, image: Image.Image):
        if self.is_mock or not self.model: return "Modern high-quality product"
        prompt = "Analyze this image. Describe colors, materials, and vibe in 1 sentence."
        response = self._generate_with_retry([prompt, image])
        return response.text if response else "Premium product"

    def generate_campaigns(self, brand: str, visual_context: str, logo_present: bool = False):
        if self.is_mock or not self.model: return self._mock_data()

        prompt = f"""
        Role: Creative Director for {brand}. Product Visuals: "{visual_context}".
        Task: Create 4 ad variations (Themes: Minimalist, Lifestyle, Luxury, High Energy).
        Return RAW JSON Array:
        [
            {{
                "theme": "Theme Name",
                "headline": "Headline (Max 7 words)",
                "caption": "Social copy",
                "image_prompt": "Stable Diffusion prompt. Include '{brand} logo' if logo_present.",
                "hex_accent": "#00CC96"
            }}
        ]
        """
        
        response = self._generate_with_retry(prompt)
        
        if response:
            try:
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                campaigns = json.loads(clean_json)
                
                for i, camp in enumerate(campaigns):
                    branding = f"branded with {brand} logo" if logo_present else ""
                    final_prompt = f"{camp['image_prompt']}, {branding}, {visual_context}, 8k photography"
                    
                    seed = random.randint(100, 99999)
                    encoded = final_prompt.replace(" ", "%20")
                    camp['image_url'] = f"https://pollinations.ai/p/{encoded}?seed={seed}&width=1080&height=1080&nologo=true"
                    
                    
                    self.save_to_library(camp['image_url'], f"{brand}_{camp['theme']}")
                    
                return campaigns
            except:
                return self._mock_data()
        return self._mock_data()

    def save_to_library(self, url, filename):
        try:
            
            img_data = requests.get(url, timeout=30).content
            if len(img_data) > 1024:
                safe_name = "".join([c for c in filename if c.isalnum() or c=='_'])
                path = os.path.join(self.library_path, f"{safe_name}.jpg")
                with open(path, "wb") as f:
                    f.write(img_data)
        except Exception as e:
            print(f"Save failed: {e}")

    def get_library_assets(self):
        if not os.path.exists(self.library_path): return []
        files = [os.path.join(self.library_path, f) for f in os.listdir(self.library_path) if f.endswith('.jpg')]
        files.sort(key=os.path.getmtime, reverse=True)
        return files

    def package_assets(self, campaigns):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            manifest = "CAMPAIGN ASSETS\n===============\n\n"
            for i, camp in enumerate(campaigns):
                fname = f"Var_{i+1}_{camp['theme'].split()[0]}.jpg"
                manifest += f"[{camp['theme']}]\nHEADLINE: {camp['headline']}\nFILE: {fname}\n\n"
                try:
                    img_bytes = requests.get(camp['image_url'], timeout=30).content
                    zf.writestr(fname, img_bytes)
                except: pass
            zf.writestr("campaign_manifest.txt", manifest)
        return zip_buffer.getvalue()

    def _mock_data(self):
        return [
            {"theme": "Neon Future", "headline": "Light Up The Night.", "caption": "Next gen tech.", "image_prompt": "neon cyberpunk product", "image_url": "https://pollinations.ai/p/neon?seed=1", "hex_accent": "#00CC96"},
            {"theme": "Pure Zen", "headline": "Simplicity Redefined.", "caption": "Find your balance.", "image_prompt": "minimalist white product", "image_url": "https://pollinations.ai/p/white?seed=2", "hex_accent": "#AAAAAA"},
            {"theme": "Urban Flow", "headline": "Move With The City.", "caption": "Never stop.", "image_prompt": "urban street style product", "image_url": "https://pollinations.ai/p/urban?seed=3", "hex_accent": "#FF4B4B"},
            {"theme": "Luxury Gold", "headline": "Standard of Excellence.", "caption": "Pure luxury.", "image_prompt": "gold luxury product", "image_url": "https://pollinations.ai/p/gold?seed=4", "hex_accent": "#FFD700"}
        ]