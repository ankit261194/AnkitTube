import os
import sys
import json
import shutil
import urllib.request
import subprocess

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def download_file(url, target_path, label="file"):
    print(f"[*] Downloading {label} from {url}...")
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    # Using curl.exe for robust redirect handling and progress
    cmd = ["curl.exe", "-L", "-s", "-S", "-o", target_path, url]
    res = subprocess.run(cmd)
    if res.returncode == 0 and os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        print(f"[+] Downloaded {label} -> {target_path} ({os.path.getsize(target_path)} bytes)")
        return True
    else:
        # Fallback to urllib if curl fails
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print(f"[+] Downloaded {label} via urllib -> {target_path}")
            return True
        except Exception as e:
            print(f"[-] Failed to download {label}: {e}")
            return False

def get_latest_github_release_asset(repo, asset_filter):
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for asset in data.get('assets', []):
                name = asset.get('name', '')
                if asset_filter(name):
                    return asset.get('browser_download_url'), data.get('tag_name')
    except Exception as e:
        print(f"[-] Error fetching release from {repo}: {e}")
    return None, None

def run_build():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir, "config.json")
    cfg = load_config(config_file)

    app_name = cfg.get("app_name", "MeraTube")
    pkg_name = cfg.get("app_package_name", "com.meratube.android")
    plugin_name = cfg.get("plugin_app_name", "MeraTube Core Services")

    build_dir = os.path.join(base_dir, "build_cache")
    output_dir = os.path.join(base_dir, "output")
    keystore_dir = os.path.join(base_dir, "keystore")
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(keystore_dir, exist_ok=True)

    # 1. Generate Keystore if not exists
    keystore_path = os.path.join(keystore_dir, "release.keystore")
    if not os.path.exists(keystore_path):
        import generate_keystore
        generate_keystore.generate_keystore(keystore_path, cfg)

    # 2. Download / Check ReVanced CLI & Patches
    cli_path = os.path.join(build_dir, "revanced-cli.jar")
    patches_path = os.path.join(build_dir, "revanced-patches.jar")
    purged_patches_path = os.path.join(build_dir, "revanced-patches-purged.jar")
    gmscore_path = os.path.join(build_dir, "GmsCore.apk")

    print("[*] Checking latest ReVanced components from GitHub...")
    if not os.path.exists(cli_path):
        cli_url, _ = get_latest_github_release_asset("ReVanced/revanced-cli", lambda n: n.endswith(".jar"))
        if cli_url:
            download_file(cli_url, cli_path, "ReVanced CLI")
        else:
            print("[-] Could not download ReVanced CLI automatically. Place it manually in build_cache/revanced-cli.jar")
            return

    if not os.path.exists(patches_path):
        patches_url, _ = get_latest_github_release_asset("ReVanced/revanced-patches", lambda n: n.endswith(".jar") or n.endswith(".rvp") or n.endswith(".mpp"))
        if not patches_url:
            print("[*] ReVanced patches mirror: checking MorpheApp/morphe-patches...")
            patches_url, _ = get_latest_github_release_asset("MorpheApp/morphe-patches", lambda n: n.endswith(".mpp") or n.endswith(".jar"))
        if patches_url:
            download_file(patches_url, patches_path, "Patches Bundle")
        else:
            print("[-] Could not download Patches automatically. Place it manually in build_cache/revanced-patches.jar")
            return

    if not os.path.exists(gmscore_path):
        gmscore_url, _ = get_latest_github_release_asset("ReVanced/GmsCore", lambda n: n.endswith(".apk") and "arm64" not in n)
        if not gmscore_url:
            gmscore_url, _ = get_latest_github_release_asset("ReVanced/GmsCore", lambda n: n.endswith(".apk"))
        if gmscore_url:
            download_file(gmscore_url, gmscore_path, "GmsCore (MicroG)")

    # 3. Purge ReVanced Branding from Patches
    import purge_revanced
    purge_revanced.purge_patches_jar(patches_path, purged_patches_path, cfg)

    # 4. Rebrand MicroG / GmsCore as App Plugin
    if os.path.exists(gmscore_path):
        plugin_apk_out = os.path.join(output_dir, f"{app_name.replace(' ', '_')}-Core-Plugin.apk")
        import rebrand_microg
        rebrand_microg.rebrand_microg(gmscore_path, plugin_apk_out, config_file)

    # 5. Check YouTube Base APK
    yt_apk = os.path.join(base_dir, "youtube.apk")
    if not os.path.exists(yt_apk):
        print("\n" + "="*70)
        print(f"[!] ACTION REQUIRED: Please download a clean YouTube APK (nodpi recommended)")
        print(f"[!] and place it at: {yt_apk}")
        print("    You can download it safely from APKMirror (search YouTube).")
        print("="*70 + "\n")
        return

    # 6. Run ReVanced CLI to Build Branded YouTube APK
    app_icon_path = os.path.join(base_dir, "assets", "app_icon.png")
    final_app_apk = os.path.join(output_dir, f"{app_name.replace(' ', '_')}-Official.apk")
    
    cli_cmd = [
        "java", "-jar", cli_path,
        "patch",
        "--patches", purged_patches_path,
        "--out", final_app_apk,
        "--keystore", keystore_path,
        "--keystore-password", cfg.get("keystore_password", "customtube123"),
        "--keystore-entry-alias", "release_key",
        "--keystore-entry-password", cfg.get("keystore_password", "customtube123"),
        "--patch", "custom-branding",
        "-o", f"app-name={app_name}",
        "-o", f"icon-path={app_icon_path}",
        "--patch", "custom-package-name",
        "-o", f"package-name={pkg_name}",
        yt_apk
    ]

    print(f"\n[*] Building branded app '{app_name}' with package '{pkg_name}'...")
    print(f"[*] Command: {' '.join(cli_cmd)}")
    res = subprocess.run(cli_cmd)
    
    clean_name = app_name.replace(' ', '_')
    if res.returncode == 0:
        print("\n" + "="*70)
        print("[SUCCESS] YOUR BRANDED APP IS READY!")
        print(f"Main App: {final_app_apk}")
        print(f"Plugin:   {os.path.join(output_dir, f'{clean_name}-Core-Plugin.apk')}")
        print("="*70 + "\n")
    else:
        print(f"[-] Patching failed with exit code: {res.returncode}")

if __name__ == "__main__":
    run_build()
