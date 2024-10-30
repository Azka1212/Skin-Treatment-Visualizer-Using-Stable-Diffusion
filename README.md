# Skin Treatment Visualizer Using Stable Diffusion

A web-based application designed to simulate and visualize aesthetic skin treatments on uploaded images using the Stable Diffusion model. This tool allows users to apply various cosmetic procedures (such as Botox, fillers, and contouring) and adjust the intensity of each treatment to visualize potential outcomes realistically.

## Features

- **Realistic Treatment Visualizations**: Generate an "after-treatment" image based on user-selected aesthetic treatments and intensity.
- **Customizable Treatment Options**: Choose from a range of treatments, including cheek fillers, Botox, contouring, and more.
- **Intensity Control**: Each treatment includes a customizable intensity slider (1-10) to control the degree of enhancement.
- **Image Download**: Download the generated "after-treatment" image for further use.

## How It Works

1. **Upload a 'Before Treatment' Image**: Start by uploading an image in `.jpg`, `.jpeg`, or `.png` format.
2. **Select Treatments**: Choose from a list of aesthetic treatments.
3. **Adjust Intensity**: Use sliders to set the intensity level of each selected treatment.
4. **Generate Image**: Click the "Generate After-Treatment Image" button to see the visualized results.
5. **Download Image**: Save the generated image to your device.

## Technical Overview

This application leverages the `StableDiffusionImg2ImgPipeline` from the `diffusers` library and is built on **Streamlit** for an interactive user experience.

### Model Details

- **Stable Diffusion**: Utilizes `Stable Diffusion v1.5` via the `diffusers` library for high-quality image-to-image transformations.
- **GPU Acceleration**: Offloaded to GPU for faster processing and includes CPU offloading for memory optimization.
- **Customized Prompts**: Predefined prompt modifications for each treatment to ensure realistic and consistent results.

### Treatment Options

Each treatment includes a unique description and intensity adjustment for precise control:
- **Full Face Contouring**
- **Lip Filler**
- **Facial Botox**
- **Cheek Filler**
- **Filler Under Eyes**
- **Smile Line Filler**
- **Temple Filler**
- **Nose Filler**
- **Forehead Botox**

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/Skin-Treatment-Visualizer.git
cd Skin-Treatment-Visualizer
pip install -r requirements.txt


##Usage
Run the Streamlit app with:
```bash
streamlit run app.py

Visit http://localhost:8501 in your browser to interact with the application.
[Video Project 1.zip](https://github.com/user-attachments/files/17576560/Video.Project.1.zip)

