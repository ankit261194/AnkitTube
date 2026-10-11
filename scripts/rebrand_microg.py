import os
import sys
import json
import shutil
import subprocess
import zipfile
from PIL import Image

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def resize_icon(src_icon, dest_path, size):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with Image.open(src_icon) as img:
        img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
        img_resized.save(dest_path, "PNG")

def rebrand_with_apktool(input_apk, output_apk, plugin_icon, config):
    print("[*] Rebranding MicroG/GmsCore using apktool...")
    temp_dir = "_temp_gmscore_decompiled"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    plugin_name = config.get("plugin_app_name", "App Core Services")
    dev_name = config.get("developer_name", "Dev")
    contact = config.get("contact_number", "")

    # Decompile
    cmd_decompile = ["apktool", "d", "-f", input_apk, "-o", temp_dir]
    res = subprocess.run(cmd_decompile, capture_output=True, text=True)
    if res.returncode != 0:
        print("[-] apktool decompile failed:", res.stderr)
        return False

    # 1. Update strings.xml in res/values/
    strings_path = os.path.join(temp_dir, "res", "values", "strings.xml")
    if os.path.exists(strings_path):
        with open(strings_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Replace app titles
        content = content.replace("microG Services", plugin_name)
        content = content.replace("GmsCore", plugin_name)
        content = content.replace("microG", plugin_name)

        # Update app_name string
        import re
        content = re.sub(r'<string name="app_name">.*?</string>', f'<string name="app_name">{plugin_name}</string>', content)

        with open(strings_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)
        print(f"[+] Replaced app title with: '{plugin_name}'")

    # 2. Replace launcher icons in all res/mipmap-* and res/drawable-*
    icon_sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
        "drawable-mdpi": 48,
        "drawable-hdpi": 72,
        "drawable-xhdpi": 96,
        "drawable-xxhdpi": 144,
        "drawable-xxxhdpi": 192,
    }

    res_dir = os.path.join(temp_dir, "res")
    if os.path.exists(res_dir):
        for root, dirs, files in os.walk(res_dir):
            for file in files:
                if ("ic_launcher" in file.lower() or "icon" in file.lower()) and file.endswith(".png"):
                    folder = os.path.basename(root)
                    size = icon_sizes.get(folder, 144)
                    full_dest = os.path.join(root, file)
                    resize_icon(plugin_icon, full_dest, size)

    # 3. Rebuild APK
    cmd_build = ["apktool", "b", temp_dir, "-o", output_apk]
    res_b = subprocess.run(cmd_build, capture_output=True, text=True)
    if res_b.returncode != 0:
        print("[-] apktool build failed:", res_b.stderr)
        return False

    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"[+] Plugin APK successfully rebranded and built: {output_apk}")
    return True

def rebrand_fallback_zip(input_apk, output_apk, plugin_icon, config):
    print("[!] apktool not found in PATH. Using direct asset overlay mode...")
    plugin_name = config.get("plugin_app_name", "App Core Services")
    temp_extract = "_temp_gmscore_zip"
    if os.path.exists(temp_extract):
        shutil.rmtree(temp_extract)
    os.makedirs(temp_extract, exist_ok=True)

    with zipfile.ZipFile(input_apk, "r") as zf:
        zf.extractall(temp_extract)

    # Replace icon files
    for root, dirs, files in os.walk(temp_extract):
        for file in files:
            if ("ic_launcher" in file.lower() or "icon" in file.lower()) and file.endswith(".png"):
                full_dest = os.path.join(root, file)
                resize_icon(plugin_icon, full_dest, 144)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_apk)), exist_ok=True)

    # Pack back
    with zipfile.ZipFile(output_apk, "w", compression=zipfile.ZIP_DEFLATED) as zf_out:
        for root, dirs, files in os.walk(temp_extract):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, temp_extract)
                zf_out.write(abs_path, rel_path)

    shutil.rmtree(temp_extract, ignore_errors=True)
    print(f"[+] Plugin icons updated in APK: {output_apk}")
    return True

def rebrand_microg(input_apk, output_apk, config_path):
    config = load_config(config_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugin_icon = os.path.join(base_dir, "assets", "plugin_icon.png")

    # Try apktool first for 100% full string and UI rebranding
    success = False
    try:
        shutil_which = shutil.which("apktool")
        if shutil_which:
            success = rebrand_with_apktool(input_apk, output_apk, plugin_icon, config)
    except Exception as e:
        print(f"Error checking apktool: {e}")

    if not success:
        rebrand_fallback_zip(input_apk, output_apk, plugin_icon, config)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python rebrand_microg.py <input_gmscore.apk> <output_plugin.apk> [config.json]")
        sys.exit(1)

    in_apk = sys.argv[1]
    out_apk = sys.argv[2]
    cfg = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

    rebrand_microg(in_apk, out_apk, cfg)
