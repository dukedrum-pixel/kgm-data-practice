"""CSV -> static HTML dashboard; Python standard library only."""
from pathlib import Path
import csv, json, html, sys
try:
    from .data_quality import inspect_csv, format_report, has_errors
except ImportError:  # Direct execution as `python scripts/build.py`.
    from data_quality import inspect_csv, format_report, has_errors
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'sample_prices.csv'
OUT=ROOT/'site'/'index.html'

def main():
    diagnostics=inspect_csv(DATA)
    print(format_report(diagnostics))
    if has_errors(diagnostics):
        raise ValueError('Input CSV failed quality checks')
    with DATA.open(encoding='utf-8-sig',newline='') as f:
        records=list(csv.DictReader(f))
    assert records,'No input rows'
    cleaned=[]
    for r in records:
        assert len(r['month'])==7 and r['month'][4]=='-','Invalid month'
        value=float(r['index_value'])
        assert value>0,'Index must be > 0'
        cleaned.append({'month':r['month'],'code':r['item_code'],'name':r['item_name'],'value':value,'source':r['source']})
    cleaned.sort(key=lambda x:(x['code'],x['month']))
    payload=serialize_payload(cleaned)
    template=(ROOT/'dashboard_template.html').read_text(encoding='utf-8')
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(template.replace('/*__DATA__*/',payload),encoding='utf-8')
    print(f'Created {OUT} / {len(cleaned)} records')

def serialize_payload(records):
    """Encode data safely for an inline script element."""
    return (json.dumps(records, ensure_ascii=False)
            .replace('<', '\\u003c')
            .replace('\u2028', '\\u2028')
            .replace('\u2029', '\\u2029'))

if __name__=='__main__': main()
