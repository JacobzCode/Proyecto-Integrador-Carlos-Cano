"""
Script simple para agregar datos de prueba directamente al CSV.
No requiere que el servidor esté corriendo.
"""
import csv
import os
from datetime import datetime, timedelta
import random

ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT, 'data')
ENTRIES_CSV = os.path.join(DATA_DIR, 'entries.csv')

def get_next_id():
    """Get next available ID from entries.csv"""
    if not os.path.exists(ENTRIES_CSV):
        return 1
    
    max_id = 0
    with open(ENTRIES_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                current_id = int(row.get('id', 0))
                if current_id > max_id:
                    max_id = current_id
            except:
                pass
    return max_id + 1

def add_sample_entries():
    """Add sample entries with extended fields"""
    
    # Check if file exists and has headers
    if not os.path.exists(ENTRIES_CSV):
        print("❌ Error: entries.csv no existe. Ejecuta el servidor primero.")
        return
    
    print("=" * 60)
    print("MoodKeeper - Agregar Datos de Prueba al CSV")
    print("=" * 60)
    print()
    
    # Sample data patterns
    entries = [
        # User: carlos - tendencia mixta
        {'handle': 'carlos', 'mood': 8, 'sleep': 8.0, 'appetite': 9, 'concentration': 8, 'comment': 'Excelente día'},
        {'handle': 'carlos', 'mood': 7, 'sleep': 7.5, 'appetite': 7, 'concentration': 7, 'comment': 'Me siento bien'},
        {'handle': 'carlos', 'mood': 6, 'sleep': 6.0, 'appetite': 6, 'concentration': 6, 'comment': 'Día normal'},
        {'handle': 'carlos', 'mood': 3, 'sleep': 5.0, 'appetite': 4, 'concentration': 3, 'comment': 'Me siento triste'},
        {'handle': 'carlos', 'mood': 2, 'sleep': 4.5, 'appetite': 3, 'concentration': 2, 'comment': 'Día difícil'},
        
        # User: maria - mayormente bien
        {'handle': 'maria', 'mood': 9, 'sleep': 8.5, 'appetite': 9, 'concentration': 9, 'comment': 'Feliz y motivada'},
        {'handle': 'maria', 'mood': 8, 'sleep': 8.0, 'appetite': 8, 'concentration': 8, 'comment': 'Todo bien'},
        {'handle': 'maria', 'mood': 7, 'sleep': 7.0, 'appetite': 7, 'concentration': 7, 'comment': 'Buena semana'},
        {'handle': 'maria', 'mood': 6, 'sleep': 6.5, 'appetite': 6, 'concentration': 6, 'comment': 'Un poco cansada'},
        
        # User: juan - más días difíciles
        {'handle': 'juan', 'mood': 2, 'sleep': 4.0, 'appetite': 3, 'concentration': 2, 'comment': 'No me siento bien'},
        {'handle': 'juan', 'mood': 3, 'sleep': 5.0, 'appetite': 4, 'concentration': 3, 'comment': 'Sigo mal'},
        {'handle': 'juan', 'mood': 2, 'sleep': 3.5, 'appetite': 2, 'concentration': 2, 'comment': 'Necesito ayuda'},
        {'handle': 'juan', 'mood': 4, 'sleep': 6.0, 'appetite': 5, 'concentration': 4, 'comment': 'Mejorando un poco'},
        {'handle': 'juan', 'mood': 3, 'sleep': 5.5, 'appetite': 4, 'concentration': 3, 'comment': 'Sigo luchando'},
    ]
    
    next_id = get_next_id()
    base_date = datetime.now() - timedelta(days=len(entries))
    
    # Add entries
    added_count = 0
    with open(ENTRIES_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for i, entry in enumerate(entries):
            # Increment dates
            timestamp = (base_date + timedelta(days=i)).isoformat()
            
            row = [
                next_id + i,                    # id
                1,                              # account_id (dummy)
                entry['handle'],                # handle
                entry['mood'],                  # mood
                entry['comment'],               # comment
                entry['sleep'],                 # sleep_hours
                entry['appetite'],              # appetite
                entry['concentration'],         # concentration
                timestamp                       # created
            ]
            
            writer.writerow(row)
            added_count += 1
            
            # Show progress
            mood_emoji = '😊' if entry['mood'] >= 7 else ('😐' if entry['mood'] >= 5 else '😢')
            print(f"✅ [{i+1}/{len(entries)}] {mood_emoji} {entry['handle']}: mood={entry['mood']}, sleep={entry['sleep']}h")
    
    print()
    print("=" * 60)
    print(f"✅ Se agregaron {added_count} entradas al CSV")
    print()
    print("📊 Distribución:")
    print(f"  • carlos: 5 entradas (mixtas)")
    print(f"  • maria:  4 entradas (positivas)")
    print(f"  • juan:   5 entradas (negativas)")
    print()
    print("🌐 Próximos pasos:")
    print("1. Iniciar servidor: python main.py")
    print("2. Abrir dashboard: http://127.0.0.1:5500/frontend/dashboard.html")
    print("3. Verificar alertas y correlaciones")
    print("=" * 60)

if __name__ == '__main__':
    try:
        add_sample_entries()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de que:")
        print("1. El archivo data/entries.csv existe")
        print("2. Tienes permisos de escritura")
        print("3. El CSV tiene el formato correcto")
