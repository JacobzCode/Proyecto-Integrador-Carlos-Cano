import os
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
ACCOUNTS = os.path.join(DATA, 'accounts.csv')
ENTRIES = os.path.join(DATA, 'entries.csv')


def _ensure(path, headers):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def _next_id(path):
    if not os.path.exists(path):
        return 1
    with open(path, 'r', newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        maxid = 0
        for row in r:
            try:
                v = int(row.get('id', 0))
                if v > maxid:
                    maxid = v
            except Exception:
                continue
    return maxid + 1


@dataclass
class AccountRecord:
    id: int
    handle: str
    email: str
    hashed: str
    created: datetime


class AccountStore:
    def __init__(self):
        _ensure(ACCOUNTS, ['id','handle','email','hashed','created'])

    def create(self, handle, email, hashed):
        aid = _next_id(ACCOUNTS)
        now = datetime.now().isoformat()
        with open(ACCOUNTS, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([aid, handle, email, hashed, now])
        return AccountRecord(id=aid, handle=handle, email=email, hashed=hashed, created=datetime.fromisoformat(now))

    def _iter(self):
        if not os.path.exists(ACCOUNTS):
            return
        with open(ACCOUNTS, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    yield AccountRecord(id=int(row.get('id',0)), handle=row.get('handle'), email=row.get('email'), hashed=row.get('hashed'), created=datetime.fromisoformat(row.get('created')))    
                except Exception:
                    continue

    def find_by_handle(self, handle):
        for a in self._iter():
            if a.handle == handle:
                return a
        return None


@dataclass
class EntryRecord:
    id: int
    account_id: int
    handle: str
    mood: int
    comment: Optional[str]
    sleep_hours: Optional[float]
    appetite: Optional[int]
    concentration: Optional[int]
    created: datetime


class EntryStore:
    def __init__(self):
        _ensure(ENTRIES, ['id','account_id','handle','mood','comment','sleep_hours','appetite','concentration','created'])

    def create(self, account_id, handle, mood, comment, sleep_hours=None, appetite=None, concentration=None):
        eid = _next_id(ENTRIES)
        now = datetime.now().isoformat()
        with open(ENTRIES, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([eid, account_id, handle, mood, comment or '', sleep_hours or '', appetite or '', concentration or '', now])
        return EntryRecord(id=eid, account_id=account_id, handle=handle, mood=mood, comment=comment, sleep_hours=sleep_hours, appetite=appetite, concentration=concentration, created=datetime.fromisoformat(now))

    def list_all(self):
        items = []
        if not os.path.exists(ENTRIES):
            return items
        with open(ENTRIES, 'r', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                try:
                    sleep_hours = float(row.get('sleep_hours')) if row.get('sleep_hours') else None
                    appetite = int(row.get('appetite')) if row.get('appetite') else None
                    concentration = int(row.get('concentration')) if row.get('concentration') else None
                    items.append(EntryRecord(
                        id=int(row.get('id',0)), 
                        account_id=int(row.get('account_id',0)), 
                        handle=row.get('handle'), 
                        mood=int(row.get('mood',0)), 
                        comment=row.get('comment') or None, 
                        sleep_hours=sleep_hours,
                        appetite=appetite,
                        concentration=concentration,
                        created=datetime.fromisoformat(row.get('created'))
                    ))
                except Exception:
                    continue
        return items

    def get(self, eid):
        for e in self.list_all():
            if e.id == eid:
                return e
        return None
