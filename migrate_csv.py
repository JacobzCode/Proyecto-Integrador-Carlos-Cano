"""
Migration script to add extended fields to existing entries.csv
Adds: sleep_hours, appetite, concentration columns with empty values for existing entries.
"""
import csv
import os
import shutil
from datetime import datetime

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
ENTRIES_PATH = os.path.join(DATA_DIR, 'entries.csv')
BACKUP_PATH = os.path.join(DATA_DIR, f'entries_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

def migrate_entries_csv():
    """Migrate entries.csv to include new extended fields."""
    
    if not os.path.exists(ENTRIES_PATH):
        print(f"❌ File not found: {ENTRIES_PATH}")
        return False
    
    # Create backup
    print(f"📁 Creating backup: {BACKUP_PATH}")
    shutil.copy2(ENTRIES_PATH, BACKUP_PATH)
    print(f"✅ Backup created successfully")
    
    # Read existing data
    existing_rows = []
    old_headers = []
    
    with open(ENTRIES_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        old_headers = reader.fieldnames
        for row in reader:
            existing_rows.append(row)
    
    print(f"📊 Found {len(existing_rows)} existing entries")
    print(f"📋 Old headers: {old_headers}")
    
    # Check if migration is needed
    if 'sleep_hours' in old_headers and 'appetite' in old_headers and 'concentration' in old_headers:
        print("✅ CSV already has extended fields. No migration needed.")
        return True
    
    # Define new headers
    new_headers = ['id', 'account_id', 'handle', 'mood', 'comment', 'sleep_hours', 'appetite', 'concentration', 'created']
    print(f"📋 New headers: {new_headers}")
    
    # Write migrated data
    with open(ENTRIES_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_headers, extrasaction='ignore')
        writer.writeheader()
        
        for row in existing_rows:
            # Add empty values for new fields
            row['sleep_hours'] = ''
            row['appetite'] = ''
            row['concentration'] = ''
            writer.writerow(row)
    
    print(f"✅ Migration completed successfully!")
    print(f"✅ Updated {len(existing_rows)} entries with new schema")
    print(f"📁 Backup saved at: {BACKUP_PATH}")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("MoodKeeper - CSV Schema Migration")
    print("=" * 60)
    print()
    
    success = migrate_entries_csv()
    
    print()
    if success:
        print("🎉 Migration completed successfully!")
        print()
        print("Next steps:")
        print("1. Verify new CSV structure")
        print("2. Test with: python main.py")
        print("3. Check Swagger: http://127.0.0.1:8001/docs")
    else:
        print("❌ Migration failed. Check error messages above.")
        print("💡 Your data is safe - backup created before any changes.")
    
    print("=" * 60)
