GT Creative Studio: The Auto-Creative Engine

Tagline: An enterprise-grade multimodal pipeline that ingests raw brand assets and autonomously synthesizes high-fidelity ad campaigns (Copy + Imagery) in under 60 seconds.

1. The Problem (Real World Scenario)

Context: In the AdTech ecosystem, "Creative Fatigue" is the #1 killer of campaign performance. Marketing teams spend 80% of their time manually resizing images and tweaking copy for A/B tests, leaving little room for strategy.

The Pain Point: The feedback loop between "Strategy" and "Asset Generation" is broken. It takes days to produce 10 variations of an ad. By the time they are live, the market trends have shifted.

My Solution: I built GT Creative Studio, a "Creative-as-a-Service" engine. It uses Gemini 2.0 Flash Vision to "see" a product and Stable Diffusion to "re-imagine" it, delivering production-ready assets instantly.

2. Expected End Result

For the User:

Input: Upload a raw Product Image (e.g., a sneaker) and a Brand Logo.

Action: Click "Generate Variations".

Output:

A live dashboard displaying 4 distinct strategic angles (e.g., "Luxury", "High Energy").

A Downloadable ZIP File containing high-resolution images and a text manifest, ready for immediate upload to Google/Meta Ads Manager.

3. Technical Approach

I architected this as a Multimodal RAG (Retrieval-Augmented Generation) system, moving beyond simple text prompts to a vision-first workflow.

System Architecture:

Visual Ingestion (The Eye):

Instead of relying on user text input, I passed the uploaded image stream directly to Google Gemini 2.0 Flash Vision.

The model extracts visual embeddings (materials, lighting, aesthetics) to ensure the generated ads actually look like the real product.

Strategic Synthesis (The Brain):

I engineered a "Chain of Thought" prompt that forces the LLM to output strictly formatted JSON.

This ensures the application can parse the response programmatically into "Headline", "Body", and "Image Prompt" without parsing errors.

Latent Diffusion (The Painter):

The system dynamically constructs prompts for Stable Diffusion (via Pollinations API) by combining the brand's visual identity with the generated thematic context.

Asset Orchestration (The Delivery):

I implemented an In-Memory Zip Generator using Python's zipfile and io.BytesIO. This avoids writing temporary files to the disk (Stateless Architecture), making the app faster and more secure for cloud deployment.

4. Tech Stack

Language: Python 3.10+

Multimodal AI: Google Gemini 2.0 Flash (Vision & Text reasoning)

Image Synthesis: Latent Diffusion Models (via Pollinations API)

Frontend: Streamlit (Custom CSS Design System)

Data Structure: JSON (Strict Schema Enforcement)

Asset Handling: Pillow (Image Processing) & Requests (Async Fetching)

5. Challenges & Learnings

Building a multimodal pipeline presented unique architectural challenges. Here is how I solved them:

Challenge 1: Visual Hallucinations

Issue: Early versions generated generic images that didn't resemble the uploaded product.

Solution: I implemented a "Vision-First" Seeding Step. Before generating ideas, the AI must first analyze the uploaded image and output a "Visual Descriptor String". This string is then injected into every subsequent image generation prompt, acting as a visual anchor.

Challenge 2: JSON Instability

Issue: The LLM would sometimes return markdown text instead of pure JSON, breaking the UI.

Solution: I implemented a Robust Sanitization Layer. The service layer automatically strips markdown formatting (```json) and uses a try/except fallback mechanism to switch to cached "Safe Data" if parsing fails, ensuring the demo never crashes.

6. Visual Proof

(added in screenhots folder, Please see there )

Input Interface

Generated Campaign Gallery


7. How to Run

# 1. Clone Repository
git clone https://github.com/theprogrammerashi/Gt_aihackathon

# 2. Setup Virtual Environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Configure Environment
# Create a .env file and add your key:
# GOOGLE_API_KEY="your_gemini_key_here"

# 5. Launch Application
streamlit run app.py
