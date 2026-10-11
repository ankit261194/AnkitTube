import os
import sys
import json
import subprocess

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_keystore(keystore_path, config):
    if os.path.exists(keystore_path):
        print(f"[!] Keystore already exists at: {keystore_path}")
        return True

    app_name = config.get("app_name", "MyTube")
    dev_name = config.get("developer_name", "Developer")

    # Ensure parent dir exists
    os.makedirs(os.path.dirname(os.path.abspath(keystore_path)), exist_ok=True)

    dname = f"CN={dev_name}, OU={app_name}, O={app_name} Org, L=New Delhi, ST=Delhi, C=IN"
    password = config.get("keystore_password", "customtube123")

    cmd = [
        "keytool",
        "-genkeypair",
        "-v",
        "-keystore", keystore_path,
        "-alias", "release_key",
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", "10000",
        "-storepass", password,
        "-keypass", password,
        "-dname", dname
    ]

    print(f"[*] Generating custom developer keystore for '{dev_name}'...")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[+] Keystore created successfully at: {keystore_path}")
            return True
        else:
            print("[-] Keytool error:", res.stderr)
            return False
    except Exception as e:
        print(f"[-] Failed to execute keytool: {e}")
        return False

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg_file = os.path.join(base_dir, "config.json")
    k_path = os.path.join(base_dir, "keystore", "release.keystore")
    
    cfg = load_config(cfg_file)
    generate_keystore(k_path, cfg)
