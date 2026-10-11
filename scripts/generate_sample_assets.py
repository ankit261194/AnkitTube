import os
from PIL import Image, ImageDraw, ImageFont

def create_rounded_icon(output_path, bg_color, symbol_type="play", text="M"):
    size = (512, 512)
    # Create high-res image
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background
    corner_radius = 110
    draw.rounded_rectangle([20, 20, 492, 492], radius=corner_radius, fill=bg_color)

    # Accent inner border
    draw.rounded_rectangle([24, 24, 488, 488], radius=corner_radius - 4, outline=(255, 255, 255, 40), width=4)

    if symbol_type == "play":
        # Draw sleek Play Button Triangle
        # Center triangle points
        triangle_points = [
            (195, 140),
            (365, 256),
            (195, 372)
        ]
        draw.polygon(triangle_points, fill=(255, 255, 255, 255))
    elif symbol_type == "plugin":
        # Draw Plugin / Gear / Puzzle / Service icon
        # Central circle + cross/spokes
        draw.ellipse([156, 156, 356, 356], fill=(255, 255, 255, 255))
        draw.ellipse([196, 196, 316, 316], fill=bg_color)
        
        # 4 connector dots/gears
        dots = [
            (256, 120, 30),
            (256, 392, 30),
            (120, 256, 30),
            (392, 256, 30)
        ]
        for cx, cy, r in dots:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated icon: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    
    # App Icon: Vibrant Crimson / Deep Red Gradient Style
    create_rounded_icon(os.path.join(assets_dir, "app_icon.png"), (220, 20, 60), symbol_type="play")
    
    # Plugin Icon: Sleek Tech Blue / Indigo
    create_rounded_icon(os.path.join(assets_dir, "plugin_icon.png"), (30, 144, 255), symbol_type="plugin")
