"""Optional generic JSON OpenAPI importer. Adapt config/api_mapping.json to the specific official API spec."""
from pathlib import Path
import urllib.request, urllib.parse, json,csv,os,sys
ROOT=Path(__file__).resolve().parents[1]
config_path=ROOT/'config'/'api_mapping.json'
cfg=json.loads(config_path.read_text(encoding='utf-8'))
key=os.environ.get('DATA_GO_KR_API_KEY')
if not key: sys.exit('Missing DATA_GO_KR_API_KEY: do not commit the key')
if cfg['url'].startswith('https://example') or not cfg['url'].startswith('https://'): sys.exit('Set a real HTTPS API URL in config/api_mapping.json')
params={**cfg.get('params',{}),cfg.get('key_param','serviceKey'):key}
url=cfg['url']+('?' if '?' not in cfg['url'] else '&')+urllib.parse.urlencode(params)
with urllib.request.urlopen(url,timeout=20) as res: data=json.load(res)
for k in cfg['rows_path']:
    data=data[k]
if isinstance(data,dict):data=[data]
if not isinstance(data,list):sys.exit('rows_path must resolve to a JSON array')
fields=cfg['fields']
with (ROOT/'data'/'sample_prices.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['month','item_code','item_name','index_value','source'])
    for r in data:
        try: writer.writerow([r[fields['month']],r[fields['item_code']],r[fields['item_name']],float(r[fields['index_value']]),'공공데이터 API (원문 검증 필요)'])
        except (KeyError,ValueError,TypeError) as ex:print('Skip malformed item:',ex,file=sys.stderr)
print('Import complete: run python scripts/build.py')
