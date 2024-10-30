import streamlit as st
from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image
import matplotlib.pyplot as plt
import io

# Initialize the model
@st.cache_resource
def load_model():
    pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    ).to("cuda")
    
    pipeline.enable_model_cpu_offload()  # Optional: CPU offloading for memory optimization
    # Disable NSFW safety checker
    pipeline.safety_checker = None
    return pipeline

pipeline = load_model()


# Function to modify the intensity of the prompt
def modify_prompt_intensity(prompt, intensity):
    # Improved intensity descriptions with clear instructions
    intensity_descriptions = {
    1: "barely noticeable, no change to tone, texture, or lighting",
    2: "subtle, natural, keep tone, texture, and lighting",
    3: "mild enhancement, preserve tone, texture, and lighting",
    4: "visible, natural, maintain tone and texture",
    5: "balanced, noticeable, no change to tone or texture",
    6: "clear enhancement, defined, keep realism",
    7: "strong, defined, tone and texture unchanged",
    8: "bold, transformative, tone and texture consistent",
    9: "dramatic, noticeable, tone and texture unchanged",
    10: "intense, pronounced, tone, posture, lighting unchanged"
    }

    # Get the intensity description based on user input
    intensity_description = intensity_descriptions.get(intensity, "subtle, natural enhancement, soft and understated")
    
    # Replace the placeholder in the prompt
    return prompt.replace("{intensity_description}", intensity_description)


# Function to generate the combined prompt based on user-selected treatments
def generate_treatment_prompt(treatments, intensities):
    # Dictionary of treatment prompts with clear instructions to avoid unwanted changes
    treatment_prompts = {
        "full_face_contouring": "Apply a {intensity_description} full-face contouring, enhancing facial structure. Maintain natural skin tone, texture, and lighting. Intensities 1-3, subtle contour, 4-6, balanced enhancement, 7-10, more improved look. No changes to image color or other facial features.",
        
        "lip_filler": "Apply a {intensity_description} lip filler, enhance volume and shape. Maintain natural lip texture and tone. Intensities 1-3, subtle boost, 4-6, noticeable volume, 7-10, fuller lips. No changes to image color, lighting, or other facial features. Image must be giving clean look, don't blurr the surface",
        
        "facial_botox": "Apply a {intensity_description} facial Botox to smooth wrinkles on the forehead and around the eyes. Maintain natural skin texture, tone, and lighting. Intensities 1-3, light smoothing, 4-6, wrinkle reduction, 7-10, dramatic smoothing. No changes to image color or other facial features.",
        
        "cheek_filler": "Apply a {intensity_description} cheek filler, lift and define cheekbones. Maintain natural skin tone, texture, and lighting. Intensities 1-3, subtle lift, 4-6, defined cheeks, 7-10, sculpted look. No changes to image color or other facial features. image must look like that there are some changes, and cheeks are filled",
        
        "filler_under_eyes": "Apply a {intensity_description} under-eye filler to reduce hollows and dark circles. Maintain natural skin texture and tone. Intensities 1-3, slight refresh, 4-6, noticeable smoothing, 7-10, fully rejuvenated. No changes to image color or other facial features.",
        
        "smile_line_filler": "Apply a {intensity_description} smile line filler to reduce nasolabial folds. Maintain natural skin tone and texture. Intensities 1-3, gentle softening, 4-6, balanced reduction, 7-10, significant smoothing. No changes to image color or other facial features.",
        
        "temple_filler": "Apply a {intensity_description} temple filler, restore volume and smooth hollows. Maintain natural skin tone and lighting. Intensities 1-3, subtle fill, 4-6, noticeable volume, 7-10, dramatic restoration. No changes to image color or other facial features.",
        
        "nose_filler": "Apply a {intensity_description} nose filler to smooth and refine the nasal bridge. Maintain natural proportions and skin tone. Intensities 1-3, minor smoothing, 4-6, visible refinement, 7-10, significant reshaping. No changes to image color or other facial features.",
        
        "forhead_botox": "Apply a {intensity_description} forhead, remove forhead wrinkles, maintain, (clean), skin, overall. Maintain, natural, skin, texture, tone. Intensities 1-3, light softening, 4-6, noticeable, smoothing, 7-10, fully smooth, forehead area."
    }
    
    # Generate the combined prompt by applying intensity to each selected treatment
    combined_prompt = []
    for treatment, intensity in zip(treatments, intensities):
        if treatment in treatment_prompts:
            # Modify the prompt based on the intensity and append it to the list
            combined_prompt.append(modify_prompt_intensity(treatment_prompts[treatment], intensity))
    
    # Join all prompts into one
    return " ".join(combined_prompt)

# Streamlit App
st.title("Aesthetic Treatment Image Generator")

# Upload image
uploaded_file = st.file_uploader("Upload your 'before-treatment' image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    before_image = Image.open(uploaded_file).convert("RGB")
    st.image(before_image, caption="Before Treatment", use_column_width=True)

    # Select treatments
    treatments = st.multiselect(
        "Select treatments:",
        ["full_face_contouring", "lip_filler", "facial_botox", "cheek_filler", 
         "filler_under_eyes", "smile_line_filler", "temple_filler", "nose_filler","forhead_botox"],
        default=["cheek_filler"]
    )

    # Set intensities for each treatment
    intensities = []
    for treatment in treatments:
        intensity = st.slider(f"Intensity for {treatment.replace('_', ' ').title()}:", 1, 10, 5)
        intensities.append(intensity)

    # Generate treatment prompt
    if st.button("Generate After-Treatment Image"):
        prompt = generate_treatment_prompt(treatments, intensities)

        # Generate the after-treatment image using the Stable Diffusion pipeline
        output_image = pipeline(
            prompt=prompt,
            image=before_image,
            strength=0.2  # Adjust transformation strength
            #generator=torch.manual_seed(100)  # You can change the seed value
        ).images[0]

        # Display the after-treatment image
        st.image(output_image, caption="After Treatment", use_column_width=True)

        # Option to save the image
        img_bytes = io.BytesIO()
        output_image.save(img_bytes, format='PNG')
        st.download_button(label="Download After-Treatment Image", data=img_bytes, file_name="after_treatment.png", mime="image/png")
