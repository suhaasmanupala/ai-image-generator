"""Pre-made prompt templates library"""

PROMPT_LIBRARY = {
    "Landscapes": [
        "A serene mountain landscape at sunset with golden light",
        "Tropical beach with crystal clear water and palm trees",
        "Misty forest with rays of sunlight breaking through trees",
        "Northern lights over a snowy mountain range",
        "Desert landscape with sand dunes at golden hour"
    ],
    "Characters": [
        "Portrait of a wise old wizard with a long beard",
        "Futuristic cyberpunk character with neon accessories",
        "Elegant princess in a flowing gown in a castle",
        "Brave knight in shining armor holding a sword",
        "Mysterious hooded figure in a dark alley"
    ],
    "Fantasy": [
        "Majestic dragon flying over a medieval castle",
        "Enchanted forest with glowing mushrooms and fairies",
        "Ancient temple ruins covered in mystical vines",
        "Floating islands in the sky connected by bridges",
        "Crystal cave with magical glowing crystals"
    ],
    "Sci-Fi": [
        "Futuristic city with flying cars and neon signs",
        "Space station orbiting a distant planet",
        "Robot walking through a cyberpunk street",
        "Alien landscape with multiple moons in the sky",
        "High-tech laboratory with holographic displays"
    ],
    "Animals": [
        "Majestic lion with a flowing mane in golden light",
        "Colorful parrot perched on a tropical branch",
        "Wise owl sitting on a moonlit tree branch",
        "Playful dolphins jumping out of ocean waves",
        "Elegant white horse running through a field"
    ],
    "Abstract": [
        "Colorful geometric patterns with vibrant gradients",
        "Swirling cosmic energy with stars and nebulas",
        "Abstract representation of music with flowing colors",
        "Fractal patterns with infinite detail and symmetry",
        "Liquid metal flowing in artistic patterns"
    ]
}

def get_random_prompt(category: str = None) -> str:
    """Get a random prompt from library"""
    import random
    if category and category in PROMPT_LIBRARY:
        return random.choice(PROMPT_LIBRARY[category])
    
    all_prompts = []
    for prompts in PROMPT_LIBRARY.values():
        all_prompts.extend(prompts)
    return random.choice(all_prompts)
