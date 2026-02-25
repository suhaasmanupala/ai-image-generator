# 🎨 AI Image Generator Pro

A production-ready, feature-rich Text-to-Image web application built with Python and Streamlit, powered by Stable Diffusion AI.

## ✨ Features

### 🖼️ Core Generation
- **Text-to-Image**: Generate high-quality images from text prompts
- **Batch Generation**: Create multiple variations with different seeds
- **Style Transfer**: Transform uploaded images with AI
- **Multiple Sizes**: 512x512, 768x768, 1024x1024, and custom aspect ratios

### 🎨 Advanced Controls
- **Guidance Scale**: Fine-tune how closely AI follows your prompt (1.0-20.0)
- **Inference Steps**: Control generation quality (20-100 steps)
- **Seed Control**: Reproducible results with specific seeds
- **Negative Prompts**: Specify what to avoid in images

### 📚 Smart Prompts
- **Prompt Library**: 30+ pre-made prompts across 6 categories
- **Prompt Enhancement**: Auto-improve prompts with quality keywords
- **Style Presets**: 8 artistic styles (Photorealistic, Anime, Oil Painting, etc.)
- **Random Prompts**: Get instant inspiration

### 🖼️ Session Features
- **Generation History**: View all images created in current session
- **Analytics Dashboard**: Track success rate and generation stats
- **Download Options**: Save images with or without watermarks
- **Settings Tracking**: Review parameters used for each generation

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Key

1. Visit [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a free account
3. Generate an access token with "Read" permission

### 3. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API key
HUGGINGFACE_API_KEY=hf_your_token_here
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Usage Guide

### Single Image Generation
1. Navigate to "Generate" → "Single Image" tab
2. Enter your prompt or use a random one
3. Optionally select a style preset
4. Adjust advanced settings if needed
5. Click "Generate Image"
6. Download your creation

### Batch Generation
1. Go to "Batch Generate" tab
2. Enter your prompt
3. Select number of variations (2-6)
4. Generate multiple images at once
5. Download individual variations

### Style Transfer
1. Go to "Style Transfer" tab
2. Upload an image
3. Choose a style preset or write custom prompt
4. Adjust transformation strength
5. See before/after comparison
6. Download transformed image

### Prompt Library
1. Navigate to "Prompt Library"
2. Browse categories (Landscapes, Characters, Fantasy, etc.)
3. Click "Use" on any prompt
4. Return to Generate page to create

### Analytics
1. Go to "Analytics" page
2. View total generations and success rate
3. Review recent activity
4. Track your creative progress

## 🎯 Project Structure

```
.
├── app.py                 # Main application
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── image_generator.py # Image generation logic
│   ├── prompt_library.py  # Pre-made prompts
│   ├── prompt_enhancer.py # Prompt enhancement
│   ├── history_manager.py # Session history
│   └── utils.py           # Utility functions
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

## 🔧 Configuration

### Environment Variables

- `HUGGINGFACE_API_KEY` (required): Your Hugging Face API token

### Advanced Settings

All configurable in the UI:
- Image dimensions
- Guidance scale
- Inference steps
- Random seed
- Negative prompts
- Transformation strength

## 🌐 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Add secrets in dashboard:
   ```toml
   HUGGINGFACE_API_KEY = "your_token_here"
   ```
5. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t ai-image-gen .
docker run -p 8501:8501 -e HUGGINGFACE_API_KEY=your_key ai-image-gen
```

## 🎨 Style Presets

- **Photorealistic**: Realistic lighting and detailed textures
- **Anime**: Vibrant colors and manga art style
- **Oil Painting**: Brush strokes and classical art
- **Cyberpunk**: Neon lights and futuristic sci-fi
- **Fantasy**: Magical and ethereal atmosphere
- **Watercolor**: Soft colors and flowing artistic style
- **3D Render**: CGI and Unreal Engine quality
- **Sketch**: Hand-drawn pencil sketch style

## 📊 Features Comparison

| Feature | This App | Basic Generators |
|---------|----------|------------------|
| Text-to-Image | ✅ | ✅ |
| Batch Generation | ✅ | ❌ |
| Style Transfer | ✅ | ❌ |
| Prompt Library | ✅ | ❌ |
| Prompt Enhancement | ✅ | ❌ |
| Style Presets | ✅ | ❌ |
| Session History | ✅ | ❌ |
| Analytics | ✅ | ❌ |
| Negative Prompts | ✅ | ❌ |
| Seed Control | ✅ | ❌ |
| Watermarks | ✅ | ❌ |

## 🛡️ Security

- ✅ API keys in environment variables
- ✅ No hardcoded credentials
- ✅ .env excluded from version control
- ✅ Input validation
- ✅ Error handling

## 🐛 Troubleshooting

### "Invalid token" error
- Ensure you copied the complete token including `hf_` prefix
- Check token has "Read" permission
- Verify token is active at https://huggingface.co/settings/tokens

### "Model is loading" error
- This is normal for first request
- Wait 30-60 seconds and try again
- Model needs to warm up

### "Rate limit" error
- Free tier has rate limits
- Wait a few minutes before retrying
- Consider upgrading for higher limits

## 📝 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Inference API
- [Streamlit](https://streamlit.io/) for the web framework
- [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) for the AI model

## 📧 Support

For issues or questions:
- Check [Hugging Face Status](https://status.huggingface.co/)
- Review this documentation
- Open an issue on GitHub

---

Made with ❤️ using Python, Streamlit, and AI
