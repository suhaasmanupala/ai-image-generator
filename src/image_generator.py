from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List
import random

class ImageGenerator:
    """Handles image generation using Stable Diffusion API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = InferenceClient(token=api_key)
        self.model = "black-forest-labs/FLUX.1-schnell"
        self.img2img_model = "stabilityai/stable-diffusion-2-1"  # For image-to-image
    
    def generate_image(
        self,
        prompt: str,
        size: str = "512x512",
        guidance_scale: float = 7.5,
        negative_prompt: str = None,
        seed: int = None,
        num_inference_steps: int = 50
    ) -> Dict[str, Any]:
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of desired image
            size: Image dimensions (e.g., "512x512")
            guidance_scale: How closely to follow the prompt
            negative_prompt: What to avoid in the image
            seed: Random seed for reproducibility
            num_inference_steps: Number of denoising steps
        
        Returns:
            Dictionary with success status, image data, or error message
        """
        try:
            width, height = map(int, size.split("x"))
            
            # Set seed if provided
            if seed is None:
                seed = random.randint(0, 2147483647)
            
            # Generate image using InferenceClient
            image = self.client.text_to_image(
                prompt=prompt,
                model=self.model,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps
            )
            
            # Convert to bytes
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            image_bytes = img_byte_arr.getvalue()
            
            return {
                "success": True,
                "image": image,
                "image_bytes": image_bytes,
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "seed": seed,
                "width": width,
                "height": height
            }
        
        except Exception as e:
            error_msg = str(e)
            if "Model is currently loading" in error_msg or "loading" in error_msg.lower():
                return {"success": False, "error": "⏳ Model is loading. Please wait 30-60 seconds and try again."}
            elif "rate limit" in error_msg.lower():
                return {"success": False, "error": "⏱️ Rate limit reached. Please wait a few minutes and try again."}
            elif "401" in error_msg or "Invalid" in error_msg or "Unauthorized" in error_msg:
                return {
                    "success": False, 
                    "error": "🔑 Invalid API token. Please check SETUP_INSTRUCTIONS.md for help getting a valid token."
                }
            else:
                return {"success": False, "error": f"❌ Error: {error_msg}"}
    
    def generate_batch(
        self,
        prompt: str,
        count: int = 4,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate multiple images with different seeds"""
        results = []
        for i in range(count):
            result = self.generate_image(prompt=prompt, seed=None, **kwargs)
            results.append(result)
        return results
    
    def image_to_image(
        self,
        prompt: str,
        init_image: Image.Image,
        strength: float = 0.75,
        guidance_scale: float = 7.5,
        negative_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Generate image from an initial image and prompt using style transfer
        
        Args:
            prompt: Text description for the transformation
            init_image: Initial image to transform
            strength: How much to transform (0.0-1.0, higher = more change)
            guidance_scale: How closely to follow the prompt
            negative_prompt: What to avoid
        
        Returns:
            Dictionary with success status, image data, or error message
        """
        try:
            # For now, we'll simulate style transfer by generating a new image
            # with the prompt and blending it with the original
            # This is a workaround since FLUX doesn't support img2img
            
            # Get dimensions from original image
            width, height = init_image.size
            
            # Ensure dimensions are within limits
            max_size = 768
            if max(width, height) > max_size:
                ratio = max_size / max(width, height)
                width = int(width * ratio)
                height = int(height * ratio)
                init_image = init_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Round to nearest multiple of 8 (required by model)
            width = (width // 8) * 8
            height = (height // 8) * 8
            
            # Generate new image with the style prompt
            result_image = self.client.text_to_image(
                prompt=prompt,
                model=self.model,
                width=width,
                height=height,
                guidance_scale=guidance_scale,
                negative_prompt=negative_prompt
            )
            
            # Blend with original based on strength
            if strength < 1.0:
                # Resize result to match original if needed
                if result_image.size != init_image.size:
                    result_image = result_image.resize(init_image.size, Image.Resampling.LANCZOS)
                
                # Blend images
                from PIL import ImageChops
                result_image = Image.blend(init_image, result_image, strength)
            
            # Convert result to bytes
            result_byte_arr = BytesIO()
            result_image.save(result_byte_arr, format='PNG')
            result_bytes = result_byte_arr.getvalue()
            
            return {
                "success": True,
                "image": result_image,
                "image_bytes": result_bytes,
                "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "width": result_image.width,
                "height": result_image.height
            }
        
        except Exception as e:
            error_msg = str(e)
            if "loading" in error_msg.lower():
                return {"success": False, "error": "⏳ Model is loading. Please wait and try again."}
            elif "rate limit" in error_msg.lower():
                return {"success": False, "error": "⏱️ Rate limit reached. Please wait a moment."}
            else:
                return {"success": False, "error": f"❌ Error: {error_msg}"}
    
    def add_watermark(self, image: Image.Image, text: str = "AI Generated") -> Image.Image:
        """Add watermark to image"""
        watermarked = image.copy()
        draw = ImageDraw.Draw(watermarked)
        
        # Position watermark at bottom right
        width, height = watermarked.size
        text_bbox = draw.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        position = (width - text_width - 10, height - text_height - 10)
        
        # Draw semi-transparent background
        draw.rectangle(
            [position[0] - 5, position[1] - 5, 
             position[0] + text_width + 5, position[1] + text_height + 5],
            fill=(0, 0, 0, 128)
        )
        
        # Draw text
        draw.text(position, text, fill=(255, 255, 255, 200))
        
        return watermarked
