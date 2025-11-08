from fastapi import FastAPI, HTTPException, status, Depends, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Tuple
from .dto import AccountCreate, SessionCreate, AccountOut, EntryCreate, EntryOut
from .storage import AccountStore, EntryStore
from .security import hash_secret, verify_secret, make_token, read_token
from . import insights
from fastapi import Response

app = FastAPI(title='MoodKeeper', description='Service for mood entries', version='0.1')

# Allow the frontend (served e.g. at http://127.0.0.1:5500) to call the API during development
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

account_store = AccountStore()
entry_store = EntryStore()


def _current_user(authorization: str = Header(..., alias='Authorization')) -> Tuple:
    # Accept standard 'Authorization: Bearer <token>' header
    auth = authorization
    if not isinstance(auth, str) or not auth.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid auth scheme')
    token = auth.split(' ', 1)[1]
    handle = read_token(token)
    if not handle:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token')
    account = account_store.find_by_handle(handle)
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Account not found')
    return account, token


@app.post('/api/accounts', response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(acc: AccountCreate):
    if account_store.find_by_handle(acc.handle):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Handle already exists')
    h = hash_secret(acc.secret)
    a = account_store.create(acc.handle, acc.email, h)
    return AccountOut(id=a.id, handle=a.handle, email=a.email, created=a.created)


@app.post('/api/sessions')
def create_session(s: SessionCreate):
    a = account_store.find_by_handle(s.handle)
    if not a or not verify_secret(s.secret, a.hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    t = make_token(a.handle)
    return {'access_token': t, 'token_type': 'bearer'}


@app.post('/api/sessions/logout')
def logout(user_and_token = Depends(_current_user)):
    # stateless token: logout is client-side removal; for real revocation implement storage
    user, token = user_and_token
    return {'message': f'Logged out {user.handle}'}


@app.post('/api/entries', response_model=EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(entry: EntryCreate, authorization: str = Header(None, alias='Authorization')):
    # Allow anonymous submissions if Authorization is not provided or invalid
    acct = None
    if authorization and isinstance(authorization, str) and authorization.startswith('Bearer '):
        token = authorization.split(' ', 1)[1]
        handle = read_token(token)
        if handle:
            acct = account_store.find_by_handle(handle)

    # fallback anonymous account
    if not acct:
        class _Anon: id = 0; handle = 'anonymous'
        acct = _Anon()

    if not (1 <= entry.mood <= 10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='mood must be 1-10')
    
    # Validate optional fields
    if entry.sleep_hours is not None and not (0 <= entry.sleep_hours <= 24):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='sleep_hours must be 0-24')
    if entry.appetite is not None and not (1 <= entry.appetite <= 10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='appetite must be 1-10')
    if entry.concentration is not None and not (1 <= entry.concentration <= 10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='concentration must be 1-10')
    
    e = entry_store.create(acct.id, acct.handle, entry.mood, entry.comment, entry.sleep_hours, entry.appetite, entry.concentration)
    return EntryOut(id=e.id, account_id=e.account_id, handle=e.handle, mood=e.mood, comment=e.comment, sleep_hours=e.sleep_hours, appetite=e.appetite, concentration=e.concentration, created=e.created)


@app.get('/api/entries')
def list_entries():
    items = []
    for e in entry_store.list_all():
        items.append({
            'id': e.id, 
            'account_id': e.account_id, 
            'handle': e.handle, 
            'mood': e.mood, 
            'comment': e.comment, 
            'sleep_hours': e.sleep_hours,
            'appetite': e.appetite,
            'concentration': e.concentration,
            'created': e.created
        })
    return items


@app.get('/api/insights/summary')
def insights_summary():
    return insights.summary()


@app.get('/api/insights/average')
def insights_avg():
    return insights.avg_by()


@app.get('/api/insights/alerts')
def insights_alerts(threshold: float = 3.0, days: int = 30):
    return insights.alerts(threshold=threshold, days=days)


@app.get('/api/insights/plot/{plot_name}')
def insights_plot(plot_name: str, type: str = None):
    png = insights.plot_png(plot_name, plot_type=type)
    if png is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Plot not available')
    return Response(content=png, media_type='image/png')


@app.get('/api/recommendations')
def get_recommendations(risk_level: str = 'MODERADO'):
    """Get personalized recommendations based on risk level (ALTO, MODERADO, BAJO)"""
    if risk_level not in ['ALTO', 'MODERADO', 'BAJO']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='risk_level must be ALTO, MODERADO, or BAJO')
    return insights.get_recommendations_for_risk(risk_level)


@app.get('/api/insights/correlations')
def insights_correlations():
    """Get correlations between mood and extended fields"""
    return insights.correlations()
