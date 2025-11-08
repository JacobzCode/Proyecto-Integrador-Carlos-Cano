"""
Script to generate sample data with extended fields for testing.
Creates realistic entries with mood, sleep_hours, appetite, and concentration.
"""
import requests
import random
import time
from datetime import datetime, timedelta

API_BASE = 'http://127.0.0.1:8001/api'

# Sample users
USERS = [
    {'handle': 'carlos', 'email': 'carlos@example.com', 'secret': 'password123'},
    {'handle': 'maria', 'email': 'maria@example.com', 'secret': 'password123'},
    {'handle': 'juan', 'email': 'juan@example.com', 'secret': 'password123'},
]

# Sample comments
COMMENTS = {
    'high': ['¡Me siento genial!', 'Excelente día', 'Todo va muy bien', 'Estoy feliz'],
    'medium': ['Un día normal', 'Me siento ok', 'Estoy bien', 'Tranquilo'],
    'low': ['Me siento triste', 'No estoy bien', 'Día difícil', 'Me siento mal', 'Necesito ayuda']
}

def create_account(user):
    """Create a user account if it doesn't exist."""
    try:
        res = requests.post(f'{API_BASE}/accounts', json=user)
        if res.status_code == 201:
            print(f"✅ Cuenta creada: {user['handle']}")
            return True
        elif res.status_code == 400 and 'already exists' in res.text:
            print(f"ℹ️  Cuenta ya existe: {user['handle']}")
            return True
        else:
            print(f"❌ Error creando cuenta {user['handle']}: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al crear cuenta {user['handle']}: {e}")
        return False

def login(user):
    """Login and get JWT token."""
    try:
        res = requests.post(f'{API_BASE}/sessions', json={
            'handle': user['handle'],
            'secret': user['secret']
        })
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Login exitoso: {user['handle']}")
            return data['access_token']
        else:
            print(f"❌ Error login {user['handle']}: {res.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción al hacer login {user['handle']}: {e}")
        return None

def generate_entry(mood_category='medium'):
    """Generate a realistic entry with extended fields."""
    if mood_category == 'high':
        mood = random.randint(7, 10)
        sleep_hours = random.uniform(7, 9)
        appetite = random.randint(7, 10)
        concentration = random.randint(7, 10)
        comment = random.choice(COMMENTS['high'])
    elif mood_category == 'low':
        mood = random.randint(1, 4)
        sleep_hours = random.uniform(3, 6)
        appetite = random.randint(2, 5)
        concentration = random.randint(2, 5)
        comment = random.choice(COMMENTS['low'])
    else:  # medium
        mood = random.randint(5, 7)
        sleep_hours = random.uniform(6, 8)
        appetite = random.randint(5, 8)
        concentration = random.randint(5, 8)
        comment = random.choice(COMMENTS['medium'])
    
    return {
        'mood': mood,
        'sleep_hours': round(sleep_hours, 1),
        'appetite': appetite,
        'concentration': concentration,
        'comment': comment
    }

def create_entry(token, entry):
    """Create an entry with authentication."""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        res = requests.post(f'{API_BASE}/entries', json=entry, headers=headers)
        if res.status_code == 201:
            return True
        else:
            print(f"❌ Error creando entrada: {res.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción al crear entrada: {e}")
        return False

def generate_sample_data():
    """Generate realistic sample data for all users."""
    print("=" * 60)
    print("MoodKeeper - Generador de Datos de Prueba")
    print("=" * 60)
    print()
    
    # Step 1: Create accounts
    print("📝 Paso 1: Creando cuentas...")
    for user in USERS:
        create_account(user)
        time.sleep(0.5)
    
    print()
    print("🔐 Paso 2: Iniciando sesión...")
    tokens = {}
    for user in USERS:
        token = login(user)
        if token:
            tokens[user['handle']] = token
        time.sleep(0.5)
    
    print()
    print("📊 Paso 3: Generando entradas de prueba...")
    
    total_entries = 0
    
    # Generate entries for each user with different patterns
    for user in USERS:
        handle = user['handle']
        if handle not in tokens:
            print(f"⚠️  No se pudo obtener token para {handle}, saltando...")
            continue
        
        token = tokens[handle]
        
        # Different patterns for different users
        if handle == 'carlos':
            # Carlos tiene tendencia mixta
            categories = ['high'] * 3 + ['medium'] * 4 + ['low'] * 3
        elif handle == 'maria':
            # María está mayormente bien
            categories = ['high'] * 6 + ['medium'] * 3 + ['low'] * 1
        else:  # juan
            # Juan tiene más días difíciles
            categories = ['low'] * 5 + ['medium'] * 3 + ['high'] * 2
        
        random.shuffle(categories)
        
        print(f"\n  Generando entradas para {handle}:")
        for i, category in enumerate(categories, 1):
            entry = generate_entry(category)
            if create_entry(token, entry):
                total_entries += 1
                mood_emoji = '😊' if entry['mood'] >= 7 else ('😐' if entry['mood'] >= 5 else '😢')
                print(f"    [{i}/{len(categories)}] {mood_emoji} Mood: {entry['mood']}, Sleep: {entry['sleep_hours']}h, Comment: {entry['comment'][:30]}...")
            time.sleep(0.3)
    
    print()
    print("=" * 60)
    print(f"✅ Generación completada!")
    print(f"📊 Total de entradas creadas: {total_entries}")
    print()
    print("🌐 Próximos pasos:")
    print("1. Abrir dashboard: http://127.0.0.1:5500/frontend/dashboard.html")
    print("2. Ver API: http://127.0.0.1:8001/docs")
    print("3. Revisar alertas y correlaciones en el dashboard")
    print("=" * 60)

if __name__ == '__main__':
    try:
        generate_sample_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
