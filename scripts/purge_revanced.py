import os
import sys
import json
import zipfile
import shutil
import re

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text_content(content, config):
    app_name = config.get("app_name", "MyTube")
    dev_name = config.get("developer_name", "App Developer")
    contact_no = config.get("contact_number", "")
    email = config.get("contact_email", "")
    website = config.get("website_or_social", "")
    plugin_name = config.get("plugin_app_name", f"{app_name} Core Services")
    about_desc = config.get("about_description", f"{app_name} - Ad-free Experience")

    # Order matters: more specific first
    replacements = [
        ("ReVanced Settings", f"{app_name} Settings"),
        ("revanced_settings", f"{app_name.lower()}_settings"),
        ("ReVanced GmsCore", plugin_name),
        ("ReVanced microG", plugin_name),
        ("GmsCore", plugin_name),
        ("microG", plugin_name),
        ("MicroG", plugin_name),
        ("https://revanced.app", website),
        ("https://github.com/ReVanced", website),
        ("github.com/ReVanced", website.replace("https://", "")),
        ("The ReVanced Team", dev_name),
        ("ReVanced Team", dev_name),
        ("ReVanced Contributors", dev_name),
        ("ReVanced", app_name),
        ("revanced.app", website.replace("https://", "") if website else "app.local"),
    ]

    # In case of specific about strings
    contact_badge = f"\n\nDeveloper: {dev_name}\nContact: {contact_no}\nSupport: {email}"
    
    modified = content
    for old, new in replacements:
        modified = modified.replace(old, new)
        
    return modified

def purge_patches_jar(input_jar, output_jar, config):
    print(f"[*] Purging ReVanced branding from {input_jar}...")
    temp_dir = os.path.join(os.path.dirname(output_jar), "_temp_patches_extract")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(input_jar, "r") as zf:
        zf.extractall(temp_dir)

    target_extensions = ('.xml', '.json', '.properties', '.txt', '.yaml', '.yml', '.smali')
    modified_count = 0

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Text based resource files
            if file.lower().endswith(target_extensions):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    new_content = clean_text_content(content, config)
                    
                    # Inject contact info into about screen / dialog if found
                    if "about" in file.lower() or "preference" in file.lower():
                        if config.get("contact_number") and config["contact_number"] not in new_content:
                            new_content = new_content.replace(
                                "</resources>",
                                f'    <string name="custom_contact_info">Support: {config.get("contact_number")}</string>\n</resources>'
                            )

                    if new_content != content:
                        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(new_content)
                        modified_count += 1
                except Exception as e:
                    pass

    # Re-zip into output jar
    with zipfile.ZipFile(output_jar, "w", compression=zipfile.ZIP_DEFLATED) as zf_out:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, temp_dir)
                zf_out.write(abs_path, rel_path)

    shutil.rmtree(temp_dir)
    print(f"[+] Purged successfully! Modified {modified_count} internal resource files.")
    print(f"[+] Output saved to: {output_jar}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python purge_revanced.py <input-patches.jar> <output-purged-patches.jar> [config.json]")
        sys.exit(1)

    in_jar = sys.argv[1]
    out_jar = sys.argv[2]
    cfg_file = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    
    cfg = load_config(cfg_file)
    purge_patches_jar(in_jar, out_jar, cfg)
