"""Prompt enhancement utilities"""

class PromptEnhancer:
    """Enhance user prompts with quality keywords"""
    
    QUALITY_BOOSTERS = [
        "highly detailed", "professional", "8k", "sharp focus",
        "masterpiece", "best quality", "ultra detailed"
    ]
    
    STYLE_TEMPLATES = {
        "Photorealistic": "photorealistic, realistic lighting, detailed textures, high resolution",
        "Anime": "anime style, vibrant colors, cel shaded, manga art",
        "Oil Painting": "oil painting, brush strokes, artistic, classical art style",
        "Cyberpunk": "cyberpunk, neon lights, futuristic, sci-fi, dystopian",
        "Fantasy": "fantasy art, magical, ethereal, mystical atmosphere",
        "Watercolor": "watercolor painting, soft colors, artistic, flowing",
        "3D Render": "3d render, octane render, unreal engine, CGI",
        "Sketch": "pencil sketch, hand drawn, artistic sketch, line art"
    }
    
    NEGATIVE_DEFAULTS = [
        "blurry", "low quality", "distorted", "ugly", "bad anatomy",
        "worst quality", "low resolution", "watermark"
    ]
    
    @staticmethod
    def enhance_prompt(prompt: str, style: str = None, add_quality: bool = True) -> str:
        """Enhance a prompt with style and quality keywords"""
        enhanced = prompt.strip()
        
        # Add style if specified
        if style and style in PromptEnhancer.STYLE_TEMPLATES:
            enhanced = f"{enhanced}, {PromptEnhancer.STYLE_TEMPLATES[style]}"
        
        # Add quality boosters
        if add_quality:
            quality = ", ".join(PromptEnhancer.QUALITY_BOOSTERS[:3])
            enhanced = f"{enhanced}, {quality}"
        
        return enhanced
    
    @staticmethod
    def get_negative_prompt(custom_negatives: list = None) -> str:
        """Get default negative prompt"""
        negatives = PromptEnhancer.NEGATIVE_DEFAULTS.copy()
        if custom_negatives:
            negatives.extend(custom_negatives)
        return ", ".join(negatives)
