"""Shared helpers. Secrets are read from the environment or a local .env file and are never printed."""
import os, sys, json, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_env():
    """Load KEY=VALUE lines from <repo>/.env into os.environ (without overriding real env vars)."""
    p = os.path.join(ROOT, '.env')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def secret(name):
    load_env()
    v = os.environ.get(name, '')
    if not v:
        sys.exit(f'Missing {name}. Add it to .env (see .env.example) or choose a provider that needs no key.')
    return v

def jload(p, default=None):
    if not os.path.exists(p):
        return default
    return json.load(open(p, encoding='utf-8'))

def jdump(o, p):
    json.dump(o, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))

TAG = re.compile(r'\[[^\]]+\]\s*')
def strip_tags(text):
    """Remove ElevenLabs v3 emotion tags like [excited] for providers that would read them aloud."""
    return TAG.sub('', text).strip()
