import streamlit as st
from dotenv import load_dotenv
from src.image_generator import ImageGenerator
from src.config import Config
from src.utils import setup_page, display_error
from src.prompt_library import PROMPT_LIBRARY, get_random_prompt
from src.prompt_enhancer import PromptEnhancer
from src.history_manager import HistoryManager
from PIL import Image
import random

# Load environment variables
load_dotenv()

def main():
    setup_page()
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'history_manager' not in st.session_state:
        st.session_state.history_manager = HistoryManager()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        page = st.radio(
            "Navigation",
            ["🎨 Generate", "📚 Prompt Library", "📊 Analytics", "🖼️ History"]
        )
        
        st.divider()
        st.markdown("### About")
        st.markdown("AI Image Generator with advanced features")
    
    # Main content based on page selection
    if page == "🎨 Generate":
        show_generate_page()
    elif page == "📚 Prompt Library":
        show_prompt_library()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "🖼️ History":
        show_history()

def show_generate_page():
    st.title("🎨 AI Image Generator Pro")
    st.markdown("Generate stunning images with advanced controls")
    
    # Initialize generator
    try:
        config = Config()
        generator = ImageGenerator(config.api_key)
    except ValueError as e:
        display_error(str(e))
        st.stop()
    
    # Tabs for different generation modes
    tab1, tab2, tab3 = st.tabs(["✨ Single Image", "🎲 Batch Generate", "🎭 Style Transfer"])
    
    with tab1:
        show_single_generation(generator)
    
    with tab2:
        show_batch_generation(generator)
    
    with tab3:
        show_style_transfer()

def show_single_generation(generator):
    """Single image generation with all features"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prompt input
        prompt = st.text_area(
            "Enter your prompt",
            placeholder="A serene landscape with mountains at sunset...",
            height=100,
            key="single_prompt"
        )
        
        # Quick actions
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🎲 Random Prompt"):
                st.session_state.random_prompt = get_random_prompt()
                st.rerun()
        with col_b:
            if st.button("✨ Enhance Prompt"):
                if prompt:
                    st.session_state.enhanced_prompt = PromptEnhancer.enhance_prompt(prompt)
                    st.rerun()
        with col_c:
            if st.button("🔄 Clear"):
                st.session_state.pop('random_prompt', None)
                st.session_state.pop('enhanced_prompt', None)
                st.rerun()
        
        # Show random or enhanced prompt
        if 'random_prompt' in st.session_state:
            st.info(f"🎲 Random: {st.session_state.random_prompt}")
            prompt = st.session_state.random_prompt
        if 'enhanced_prompt' in st.session_state:
            st.success(f"✨ Enhanced: {st.session_state.enhanced_prompt}")
            prompt = st.session_state.enhanced_prompt
    
    with col2:
        # Style presets
        st.markdown("### 🎨 Style Presets")
        style = st.selectbox(
            "Choose a style",
            ["None"] + list(PromptEnhancer.STYLE_TEMPLATES.keys()),
            key="style_preset"
        )
    
    # Advanced settings in expander
    with st.expander("⚙️ Advanced Settings"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            size = st.selectbox(
                "Image Size",
                ["512x512", "768x768", "1024x1024", "512x768", "768x512"],
                index=0,
                key="adv_size"
            )
            
            guidance_scale = st.slider(
                "Guidance Scale",
                min_value=1.0,
                max_value=20.0,
                value=7.5,
                step=0.5,
                key="adv_guidance"
            )
        
        with col2:
            num_steps = st.slider(
                "Inference Steps",
                min_value=20,
                max_value=100,
                value=50,
                step=10,
                key="adv_steps"
            )
            
            use_seed = st.checkbox("Use specific seed", key="adv_use_seed")
            seed = None
            if use_seed:
                seed = st.number_input("Seed", min_value=0, max_value=2147483647, value=42, key="adv_seed")
        
        with col3:
            use_negative = st.checkbox("Use negative prompt", value=True, key="adv_negative")
            negative_prompt = None
            if use_negative:
                negative_prompt = st.text_area(
                    "Negative Prompt",
                    value=PromptEnhancer.get_negative_prompt(),
                    height=100,
                    key="adv_negative_prompt"
                )
            
            add_watermark = st.checkbox("Add watermark", key="adv_watermark")
    
    # Generate button
    if st.button("🎨 Generate Image", type="primary", use_container_width=True):
        if not prompt or not prompt.strip():
            st.warning("Please enter a prompt")
            return
        
        # Apply style if selected
        final_prompt = prompt
        if style != "None":
            final_prompt = PromptEnhancer.enhance_prompt(prompt, style=style)
        
        with st.spinner("Generating your masterpiece..."):
            result = generator.generate_image(
                prompt=final_prompt,
                size=size,
                guidance_scale=guidance_scale,
                negative_prompt=negative_prompt,
                seed=seed,
                num_inference_steps=num_steps
            )
        
        if result["success"]:
            # Add to history
            st.session_state.history.append({
                "image": result["image"],
                "prompt": final_prompt,
                "settings": {
                    "size": size,
                    "guidance": guidance_scale,
                    "steps": num_steps,
                    "seed": result.get("seed")
                }
            })
            
            st.session_state.history_manager.add_generation(
                prompt=final_prompt,
                settings={"size": size, "guidance": guidance_scale},
                success=True
            )
            
            st.success("✅ Image generated successfully!")
            
            # Display image
            st.image(result["image"], caption=final_prompt, use_column_width=True)
            
            # Image info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Size", f"{result['width']}x{result['height']}")
            with col2:
                st.metric("Seed", result.get('seed', 'N/A'))
            with col3:
                st.metric("Steps", num_steps)
            
            # Download options
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Image",
                    data=result["image_bytes"],
                    file_name=f"generated_{result['timestamp']}.png",
                    mime="image/png"
                )
            with col2:
                if add_watermark:
                    watermarked = generator.add_watermark(result["image"])
                    from io import BytesIO
                    buf = BytesIO()
                    watermarked.save(buf, format='PNG')
                    st.download_button(
                        label="📥 Download with Watermark",
                        data=buf.getvalue(),
                        file_name=f"watermarked_{result['timestamp']}.png",
                        mime="image/png"
                    )
        else:
            display_error(result["error"])
            st.session_state.history_manager.add_generation(
                prompt=final_prompt,
                settings={"size": size},
                success=False
            )

def show_batch_generation(generator):
    """Batch generation mode"""
    st.markdown("### 🎲 Generate Multiple Variations")
    st.info("Generate multiple images with different random seeds")
    
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="A beautiful landscape...",
        height=100,
        key="batch_prompt"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        batch_count = st.slider("Number of images", 2, 6, 4, key="batch_count")
        size = st.selectbox("Size", ["512x512", "768x768"], key="batch_size")
    with col2:
        guidance = st.slider("Guidance", 1.0, 20.0, 7.5, key="batch_guidance")
    
    if st.button("🎲 Generate Batch", type="primary"):
        if not prompt or not prompt.strip():
            st.warning("Please enter a prompt")
            return
        
        with st.spinner(f"Generating {batch_count} variations..."):
            results = generator.generate_batch(
                prompt=prompt,
                count=batch_count,
                size=size,
                guidance_scale=guidance
            )
        
        # Display in grid
        cols = st.columns(2)
        for idx, result in enumerate(results):
            with cols[idx % 2]:
                if result["success"]:
                    st.image(result["image"], caption=f"Variation {idx+1} (Seed: {result.get('seed', 'N/A')})")
                    st.download_button(
                        label=f"📥 Download #{idx+1}",
                        data=result["image_bytes"],
                        file_name=f"batch_{idx+1}_{result['timestamp']}.png",
                        mime="image/png",
                        key=f"download_batch_{idx}"
                    )

def show_style_transfer():
    """Style transfer with image-to-image"""
    st.markdown("### 🎭 Style Transfer & Image Transformation")
    st.info("Upload an image and transform it with AI! The app generates a new image based on your prompt and blends it with the original.")
    
    # Initialize generator
    try:
        config = Config()
        generator = ImageGenerator(config.api_key)
    except ValueError as e:
        display_error(str(e))
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Upload Image")
        uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'], key="style_upload")
        
        if uploaded_file:
            from PIL import Image
            init_image = Image.open(uploaded_file)
            st.image(init_image, caption="Original Image", use_column_width=True)
    
    with col2:
        st.markdown("#### ✨ Transformation Settings")
        
        # Style presets for image-to-image
        style_options = {
            "Custom": "",
            "Oil Painting": "oil painting, artistic, brush strokes, classical art",
            "Anime Style": "anime style, vibrant colors, manga art",
            "Watercolor": "watercolor painting, soft colors, artistic",
            "Cyberpunk": "cyberpunk, neon lights, futuristic, sci-fi",
            "Fantasy Art": "fantasy art, magical, ethereal, mystical",
            "Sketch": "pencil sketch, hand drawn, artistic sketch",
            "3D Render": "3d render, octane render, CGI, unreal engine",
            "Pop Art": "pop art, bold colors, comic book style",
            "Impressionist": "impressionist painting, soft brush strokes",
            "Dark Fantasy": "dark fantasy, gothic, dramatic lighting"
        }
        
        selected_style = st.selectbox("Choose Style", list(style_options.keys()), key="style_select")
        
        if selected_style == "Custom":
            transformation_prompt = st.text_area(
                "Describe the transformation",
                placeholder="Turn this into a beautiful sunset scene...",
                height=100,
                key="style_custom_prompt"
            )
        else:
            transformation_prompt = st.text_area(
                "Transformation prompt",
                value=style_options[selected_style],
                height=100,
                key="style_preset_prompt"
            )
        
        strength = st.slider(
            "Transformation Strength",
            min_value=0.1,
            max_value=1.0,
            value=0.75,
            step=0.05,
            help="Higher = more change from original",
            key="style_strength"
        )
        
        guidance = st.slider(
            "Guidance Scale",
            min_value=1.0,
            max_value=20.0,
            value=7.5,
            step=0.5,
            key="style_guidance"
        )
        
        use_negative = st.checkbox("Use negative prompt", value=True, key="style_negative")
        negative_prompt = None
        if use_negative:
            negative_prompt = st.text_input(
                "Negative prompt",
                value="blurry, low quality, distorted",
                key="style_negative_prompt"
            )
    
    # Transform button
    if uploaded_file and st.button("🎨 Transform Image", type="primary", use_container_width=True):
        if not transformation_prompt or not transformation_prompt.strip():
            st.warning("Please enter a transformation prompt")
            return
        
        with st.spinner("Transforming your image..."):
            result = generator.image_to_image(
                prompt=transformation_prompt,
                init_image=init_image,
                strength=strength,
                guidance_scale=guidance,
                negative_prompt=negative_prompt
            )
        
        if result["success"]:
            st.success("✅ Image transformed successfully!")
            
            # Show before/after comparison
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Before")
                st.image(init_image, use_column_width=True)
            with col2:
                st.markdown("#### After")
                st.image(result["image"], use_column_width=True)
            
            # Download button
            st.download_button(
                label="📥 Download Transformed Image",
                data=result["image_bytes"],
                file_name=f"transformed_{result['timestamp']}.png",
                mime="image/png"
            )
            
            # Settings used
            with st.expander("⚙️ Settings Used"):
                st.json({
                    "prompt": transformation_prompt,
                    "strength": strength,
                    "guidance_scale": guidance,
                    "negative_prompt": negative_prompt,
                    "size": f"{result['width']}x{result['height']}"
                })
        else:
            display_error(result["error"])

def show_prompt_library():
    """Prompt library page"""
    st.title("📚 Prompt Library")
    st.markdown("Browse and use pre-made prompts")
    
    # Category selection
    category = st.selectbox("Select Category", list(PROMPT_LIBRARY.keys()), key="prompt_category")
    
    st.markdown(f"### {category}")
    
    # Display prompts
    for idx, prompt in enumerate(PROMPT_LIBRARY[category]):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(prompt)
        with col2:
            if st.button("Use", key=f"use_prompt_{category}_{idx}"):
                st.session_state.selected_prompt = prompt
                st.success("Prompt copied! Go to Generate page.")

def show_analytics():
    """Analytics dashboard"""
    st.title("📊 Analytics Dashboard")
    
    stats = st.session_state.history_manager.get_stats()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Generations", stats["total_generations"])
    with col2:
        st.metric("Successful", stats["successful"])
    with col3:
        st.metric("Failed", stats["failed"])
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    
    st.divider()
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    recent = st.session_state.history_manager.get_recent(10)
    
    if recent:
        for entry in recent:
            with st.expander(f"🎨 {entry['prompt'][:50]}... - {entry['timestamp'][:10]}"):
                st.json(entry)
    else:
        st.info("No generation history yet. Start creating!")

def show_history():
    """Session history gallery"""
    st.title("🖼️ Generation History")
    st.markdown("View all images generated in this session")
    
    if not st.session_state.history:
        st.info("No images generated yet. Go to Generate page to create some!")
        return
    
    # Display in grid
    cols_per_row = 3
    for idx in range(0, len(st.session_state.history), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            img_idx = idx + col_idx
            if img_idx < len(st.session_state.history):
                item = st.session_state.history[img_idx]
                with col:
                    st.image(item["image"], use_column_width=True)
                    st.caption(item["prompt"][:50] + "...")
                    with st.expander("Details"):
                        st.json(item["settings"])
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    main()
