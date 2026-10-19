"""CSV -> static HTML dashboard; Python standard library only."""
from pathlib import Path
import csv, json, html, sys
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'sample_prices.csv'
OUT=ROOT/'site'/'index.html'

def main():
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
    payload=json.dumps(cleaned,ensure_ascii=False).replace('<','\\u003c')
    template=(ROOT/'dashboard_template.html').read_text(encoding='utf-8')
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(template.replace('/*__DATA__*/',payload),encoding='utf-8')
    print(f'Created {OUT} / {len(cleaned)} records')
if __name__=='__main__': main()
