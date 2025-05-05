#!/usr/bin/env python3
"""
YouTube Spam Comment Remover

Cara penggunaan:
1. Jalankan skrip:
   python ytspam.py
2. Saat diminta, masukkan URL atau ID video YouTube (bisa banyak, pisah spasi/koma).
3. Masukkan pola spam (pisah koma atau titik-koma).
4. Ikuti OAuth flow (copy-paste URL & kode) jika diminta.

Komentar yang terhapus dicatat di `deleted_comments.txt`.
"""

import re
import unicodedata
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow, argparser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Konfigurasi OAuth & API
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
LOG_FILE = 'deleted_comments.txt'


def normalize(text: str) -> str:
    """Normalize teks Unicode (compat-font, aksen)."""
    return unicodedata.normalize('NFKC', text)


def extract_video_id(token: str) -> str:
    """Ekstrak ID video 11 karakter dari URL atau kembalikan token."""
    m = re.search(r"(?:[?&]v=|youtu\.be/|/live/)([\w-]{11})", token)
    return m.group(1) if m else token.strip()


def get_authenticated_service():
    """Autentikasi OAuth2 dengan no local webserver, simpan token di oauth2.json."""
    storage = Storage('oauth2.json')
    creds = storage.get()
    if not creds or creds.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)
        flags = argparser.parse_args(args=['--noauth_local_webserver'])
        creds = run_flow(flow, storage, flags)
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def prompt_video_ids() -> list[str]:
    """Minta input URL/ID video, kembalikan daftar ID valid."""
    raw = input('Masukkan URL atau ID video YouTube (pisah spasi/koma):\n> ')
    tokens = re.split(r'[\s,]+', raw.strip())
    ids = []
    for tok in tokens:
        if not tok:
            continue
        vid = extract_video_id(tok)
        if len(vid) == 11:
            ids.append(vid)
        else:
            print(f'⚠️ Lewatkan token non-ID: {tok}')
    return ids


def prompt_spam_patterns() -> list[str]:
    """Minta input pola spam, pisah koma/titik-koma."""
    raw = input('Masukkan pola spam (pisah koma atau titik-koma):\n> ')
    parts = re.split(r'\s*[,;]\s*', raw.strip())
    patterns = []
    for p in parts:
        if not p:
            continue
        pn = normalize(p)
        try:
            re.compile(pn)
            patterns.append(pn)
        except re.error:
            patterns.append(re.escape(pn))
    return patterns


def is_spam(text: str, patterns: list[str]) -> bool:
    """Return True jika text cocok salah satu pattern."""
    nt = normalize(text.lower())
    return any(re.search(p, nt) for p in patterns)


def delete_spam_comments(youtube, video_id: str, patterns: list[str]) -> None:
    """Hapus komentar spam pada video tertentu dan catat log."""
    next_token = None
    count = 0
    with open(LOG_FILE, 'a', encoding='utf-8') as logf:
        logf.write(f"\n=== Video {video_id} ===\nPatterns: {patterns}\n")
        while True:
            try:
                resp = youtube.commentThreads().list(
                    part='snippet', videoId=video_id,
                    maxResults=100, pageToken=next_token
                ).execute()
            except HttpError as e:
                print(f'Gagal fetch komentar: {e}')
                break

            for item in resp.get('items', []):
                c = item['snippet']['topLevelComment']
                cid = c['id']
                txt = c['snippet']['textDisplay']
                auth = c['snippet']['authorDisplayName']
                if is_spam(txt, patterns):
                    try:
                        youtube.comments().setModerationStatus(
                            id=cid, moderationStatus='rejected'
                        ).execute()
                        snippet = normalize(txt)[:50].replace('\n', ' ')
                        print(f'🗑️ Dihapus: [{auth}] {snippet}…')
                        logf.write(f'[{cid}] {auth}: {snippet}…\n')
                        count += 1
                    except HttpError as e:
                        print(f'Error hapus {cid}: {e}')

            next_token = resp.get('nextPageToken')
            if not next_token:
                break

        print(f'Video {video_id}: total dihapus {count} komentar spam')
        logf.write(f'Total deleted: {count}\n')

def get_video_title(youtube, video_id: str) -> str:
    """Mengambil judul video dari video ID."""
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        items = response.get('items', [])
        if not items:
            return '[Video tidak ditemukan]'
        return items[0]['snippet']['title']
    except HttpError as e:
        return f'[Gagal mengambil judul: {e}]'
def main():
    print('=== YouTube Spam Comment Remover ===')
    video_ids = prompt_video_ids()
    if not video_ids:
        print('Tidak ada Video ID valid. Keluar.')
        return
    patterns = prompt_spam_patterns()
    print('\n🔥 Pola Spam:')
    for p in patterns:
        print(' -', p)

    youtube = get_authenticated_service()
    for vid in video_ids:
        title = get_video_title(youtube, vid)
        print(f'\n🎥 Video: {title} (ID: {vid})')
        delete_spam_comments(youtube, vid, patterns)

if __name__ == '__main__':
    main()