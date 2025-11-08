import os
from datetime import datetime
from typing import Optional, Dict, Any
import math

_HAS_PANDAS = True
try:
    import pandas as pd
except Exception:
    pd = None
    _HAS_PANDAS = False

from io import BytesIO

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENTRIES = os.path.join(ROOT, 'data', 'entries.csv')
RECOMMENDATIONS = os.path.join(ROOT, 'data', 'recommendations.csv')


def _load_entries():
    if not _HAS_PANDAS:
        return None
    if not os.path.exists(ENTRIES):
        return pd.DataFrame()
    df = pd.read_csv(ENTRIES)
    if 'created' in df.columns:
        df['created'] = pd.to_datetime(df['created'], errors='coerce')
    if 'mood' in df.columns:
        df['mood'] = pd.to_numeric(df['mood'], errors='coerce')
    return df


def summary():
    df = _load_entries()
    if df is None:
        return {'error': 'pandas required'}
    if df.empty:
        return {'count':0}
    s = df['mood'].describe().to_dict()
    mood_stats = {}
    for k, v in s.items():
        try:
            fv = float(v)
            # convert non-finite (nan/inf) to None for JSON safety
            mood_stats[k] = fv if math.isfinite(fv) else None
        except Exception:
            mood_stats[k] = None
    return {'count': int(df.shape[0]), 'mood_stats': mood_stats}


def avg_by(handle_col='handle'):
    df = _load_entries()
    if df is None:
        return {'error': 'pandas required'}
    if df.empty or handle_col not in df.columns:
        return {}
    r = df.groupby(handle_col)['mood'].mean().sort_values(ascending=False)
    out = {}
    for k, v in r.items():
        try:
            fv = float(v)
            out[str(k)] = fv if math.isfinite(fv) else None
        except Exception:
            out[str(k)] = None
    return out


def compute_composite_score(mood, sleep_hours=None, appetite=None, concentration=None):
    """
    Compute composite mental health score (0-100).
    - mood: 1-10 scale (weighted 40%)
    - sleep_hours: 0-24 (weighted 20%, optimal 7-9h)
    - appetite: 1-10 scale (weighted 20%)
    - concentration: 1-10 scale (weighted 20%)
    """
    score = 0
    weights_sum = 0
    
    # Mood component (40% weight)
    mood_normalized = (mood / 10.0) * 100
    score += mood_normalized * 0.4
    weights_sum += 0.4
    
    # Sleep component (20% weight)
    if sleep_hours is not None:
        if 7 <= sleep_hours <= 9:
            sleep_score = 100
        elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
            sleep_score = 80
        elif 5 <= sleep_hours < 6 or 10 < sleep_hours <= 11:
            sleep_score = 60
        else:
            sleep_score = 40
        score += sleep_score * 0.2
        weights_sum += 0.2
    
    # Appetite component (20% weight)
    if appetite is not None:
        appetite_normalized = (appetite / 10.0) * 100
        score += appetite_normalized * 0.2
        weights_sum += 0.2
    
    # Concentration component (20% weight)
    if concentration is not None:
        concentration_normalized = (concentration / 10.0) * 100
        score += concentration_normalized * 0.2
        weights_sum += 0.2
    
    # Normalize by actual weights used
    if weights_sum > 0:
        final_score = score / weights_sum * 100
    else:
        final_score = mood_normalized
    
    return round(final_score, 2)


def detect_negative_trend(entries_list, window=3):
    """
    Detect if there's a negative trend in recent entries.
    Returns True if the last 'window' entries show declining mood.
    """
    if len(entries_list) < window:
        return False
    
    recent = entries_list[-window:]
    moods = [e.get('mood', 0) for e in recent]
    
    # Check if generally declining
    declining = True
    for i in range(1, len(moods)):
        if moods[i] > moods[i-1]:
            declining = False
            break
    
    return declining


def compute_risk_level(composite_score, trend_negative=False):
    """
    Classify risk level based on composite score and trend.
    Returns: 'ALTO', 'MODERADO', 'BAJO'
    """
    if composite_score < 40 or (composite_score < 60 and trend_negative):
        return 'ALTO'
    elif composite_score < 70 or (composite_score < 80 and trend_negative):
        return 'MODERADO'
    else:
        return 'BAJO'


def alerts(threshold=3, days=30):
    df = _load_entries()
    if df is None:
        return {'error': 'pandas required'}
    if df.empty:
        return {'count':0,'items':[]}
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    recent = df[df['created'] >= cutoff]
    
    # Enhanced alert detection with composite scoring
    alerts_items = []
    
    for handle in recent['handle'].unique():
        user_entries = recent[recent['handle'] == handle].sort_values('created')
        
        if user_entries.empty:
            continue
        
        # Calculate composite scores for each entry
        entries_with_scores = []
        for _, row in user_entries.iterrows():
            mood = row.get('mood', 5)
            sleep_hours = row.get('sleep_hours') if 'sleep_hours' in row.index else None
            appetite = row.get('appetite') if 'appetite' in row.index else None
            concentration = row.get('concentration') if 'concentration' in row.index else None
            
            composite = compute_composite_score(mood, sleep_hours, appetite, concentration)
            
            entries_with_scores.append({
                'id': int(row.get('id', 0)),
                'handle': handle,
                'mood': float(mood),
                'composite_score': composite,
                'created': pd.Timestamp(row.get('created')).isoformat(),
                'comment': row.get('comment') or ''
            })
        
        # Calculate average composite score
        avg_composite = sum(e['composite_score'] for e in entries_with_scores) / len(entries_with_scores)
        
        # Detect trend
        trend_negative = detect_negative_trend(entries_with_scores, window=3)
        
        # Determine risk level
        risk_level = compute_risk_level(avg_composite, trend_negative)
        
        # Add to alerts if not BAJO or if mood critically low
        if risk_level != 'BAJO' or any(e['mood'] <= threshold for e in entries_with_scores):
            for entry in entries_with_scores:
                if entry['mood'] <= threshold or risk_level == 'ALTO':
                    alerts_items.append({
                        **entry,
                        'risk_level': risk_level,
                        'avg_composite': round(avg_composite, 2),
                        'trend_negative': trend_negative
                    })
    
    return {'count': len(alerts_items), 'items': alerts_items}


def get_recommendations_for_risk(risk_level='MODERADO'):
    """
    Get personalized recommendations based on risk level.
    Returns list of recommendations from recommendations.csv.
    """
    if not _HAS_PANDAS:
        # Fallback recommendations without pandas
        fallback = {
            'ALTO': [
                {'title': '🚨 Contacto Profesional Urgente', 'description': 'Tu estado emocional muestra señales de alerta. Te recomendamos contactar a un profesional de salud mental.'},
                {'title': '📞 Línea de Crisis 24/7', 'description': 'Línea 106 de orientación en salud mental (Colombia) disponible 24/7.'}
            ],
            'MODERADO': [
                {'title': '🧘 Técnicas de Relajación', 'description': 'Practicar técnicas de respiración profunda y mindfulness puede ayudarte a reducir el estrés.'},
                {'title': '💪 Actividad Física Regular', 'description': 'El ejercicio físico regular mejora significativamente el estado de ánimo.'}
            ],
            'BAJO': [
                {'title': '✅ Mantener Hábitos Saludables', 'description': 'Continúa con tus hábitos saludables: ejercicio regular, alimentación balanceada.'},
                {'title': '🌱 Crecimiento Personal', 'description': 'Considera explorar nuevas actividades que te apasionen.'}
            ]
        }
        return fallback.get(risk_level, fallback['MODERADO'])
    
    try:
        if not os.path.exists(RECOMMENDATIONS):
            return []
        
        df = pd.read_csv(RECOMMENDATIONS)
        filtered = df[df['risk_level'] == risk_level]
        
        recommendations = []
        for _, row in filtered.iterrows():
            rec = {
                'id': int(row.get('id', 0)),
                'title': str(row.get('title', '')),
                'description': str(row.get('description', ''))
            }
            if 'url' in row.index and pd.notna(row['url']):
                rec['url'] = str(row['url'])
            recommendations.append(rec)
        
        return recommendations
    except Exception:
        return []


def correlations():
    """
    Calculate correlations between mood and extended fields.
    Returns dict with correlation coefficients.
    """
    df = _load_entries()
    if df is None or df.empty:
        return {'error': 'No data available'}
    
    correlations_dict = {}
    
    # Check which columns exist
    numeric_cols = ['mood', 'sleep_hours', 'appetite', 'concentration']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) < 2:
        return {'error': 'Insufficient data for correlations'}
    
    try:
        # Calculate correlations
        corr_matrix = df[available_cols].corr()
        
        # Extract relevant correlations with mood
        if 'mood' in corr_matrix.index:
            for col in available_cols:
                if col != 'mood':
                    corr_value = corr_matrix.loc['mood', col]
                    if not math.isnan(corr_value):
                        correlations_dict[f'mood_vs_{col}'] = round(float(corr_value), 3)
        
        # Add interpretation
        interpretations = []
        for key, value in correlations_dict.items():
            abs_val = abs(value)
            if abs_val > 0.7:
                strength = "fuerte"
            elif abs_val > 0.4:
                strength = "moderada"
            else:
                strength = "débil"
            
            direction = "positiva" if value > 0 else "negativa"
            interpretations.append(f"{key}: correlación {strength} {direction} ({value})")
        
        return {
            'correlations': correlations_dict,
            'interpretations': interpretations,
            'sample_size': int(df.shape[0])
        }
    except Exception as e:
        return {'error': f'Error calculating correlations: {str(e)}'}


def plot_png(plot_name: str, plot_type: str = None) -> Optional[bytes]:
    """Generate PNG bytes for supported plots: 'hist', 'by_handle', 'ts'"""
    if not _HAS_PANDAS:
        return None
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
    except Exception:
        return None

    df = _load_entries()
    if df is None or df.empty:
        return None

    buf = BytesIO()
    try:
        if plot_name == 'hist':
            # distribution of mood values
            vals = df['mood'].dropna()
            if plot_type and plot_type.lower() in ('pie','doughnut'):
                # pie/doughnut by mood value counts
                counts = vals.astype(int).value_counts().sort_index()
                if counts.empty:
                    return None
                labels = [str(i) for i in counts.index]
                sizes = counts.values
                plt.figure(figsize=(6,6))
                if plot_type.lower() == 'doughnut':
                    # draw a doughnut by setting wedgeprops width
                    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'width':0.4})
                    plt.title('Mood distribution (doughnut)')
                else:
                    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                    plt.title('Mood distribution (pie)')
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                return buf.read()
            if plot_type and plot_type.lower() in ('scatter','points'):
                # scatter of mood over time - fallback to index if created missing
                x = None
                if 'created' in df.columns and not df['created'].isna().all():
                    x = df['created']
                else:
                    x = range(len(df))
                plt.figure(figsize=(10,4))
                plt.scatter(x, df['mood'], alpha=0.6)
                plt.title('Mood scatter over time')
                try:
                    plt.xticks(rotation=45)
                except Exception:
                    pass
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                return buf.read()
            # default: histogram
            plt.figure(figsize=(8,4))
            sns.histplot(vals, bins=10)
            plt.title('Mood distribution')
            plt.tight_layout()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            return buf.read()

        if plot_name == 'by_handle':
            # Show top handles
            top = df['handle'].value_counts().head(10).index.tolist()
            sub = df[df['handle'].isin(top)]
            if plot_type and plot_type.lower() in ('pie','doughnut'):
                counts = df['handle'].value_counts().head(10)
                plt.figure(figsize=(6,6))
                plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90)
                plt.title('Entries by handle (top 10)')
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                return buf.read()
            if plot_type and plot_type.lower() in ('scatter','points'):
                plt.figure(figsize=(10,6))
                # stripplot/jitter to represent points per handle
                sns.stripplot(x='mood', y='handle', data=sub, jitter=True)
                plt.title('Mood points by handle (top 10)')
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                return buf.read()
            # default: boxplot
            plt.figure(figsize=(10,6))
            sns.boxplot(x='handle', y='mood', data=sub)
            plt.xticks(rotation=45)
            plt.title('Mood by handle (top 10)')
            plt.tight_layout()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            return buf.read()

        if plot_name == 'ts':
            if 'created' not in df.columns:
                return None
            ts = df.set_index('created').resample('D')['mood'].mean().dropna()
            ts = ts.last('90D')
            if plot_type and plot_type.lower() in ('scatter','points'):
                plt.figure(figsize=(10,4))
                plt.scatter(ts.index, ts.values, alpha=0.7)
                plt.title('Average mood per day (points)')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                return buf.read()
            # default line
            plt.figure(figsize=(10,4))
            sns.lineplot(x=ts.index, y=ts.values)
            plt.title('Average mood per day')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            return buf.read()
    except Exception:
        return None

    return None
