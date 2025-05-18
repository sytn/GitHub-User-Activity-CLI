import argparse
from datetime import datetime
import json
import os

def get_username():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Dosyayı aç ve veriyi yükle, yoksa boş dict oluştur
    if os.path.exists('search_history.json'):
        with open('search_history.json', "r", encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"searches": []}
    else:
        data = {"searches": []}

    parser = argparse.ArgumentParser(description="Get the User's username")
    parser.add_argument("-m", "--username", type=str, help="GitHub Username", required=False)

    args = parser.parse_args()

    if not args.username:
        args.username = input("Enter Your Username: ")
        
    url = f"https://api.github.com/users/{args.username}/events"

    new_user = {
        "username": args.username,
        "url": url,
        "searched_at": now
    }

    # Yeni kullanıcıyı data içine ekle
    data["searches"].append(new_user)

    # Dosyaya tekrar yaz
    with open('search_history.json', "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return url
