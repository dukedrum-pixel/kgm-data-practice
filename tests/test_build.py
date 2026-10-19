import unittest,subprocess,sys,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BuildTest(unittest.TestCase):
    def test_build(self):
        subprocess.run([sys.executable,str(ROOT/'scripts'/'build.py')],cwd=ROOT,check=True)
        html=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        self.assertIn('강판 가격지수',html)
        self.assertIn('month,item_code,item_name,index_value,source',html)
        self.assertIn('선택한 조건에 해당하는 데이터가 없습니다.',html)
        self.assertIn('aria-live="polite"',html)
        self.assertIn('price-index-${item.value}-${year.value}.csv',html)
        self.assertIn("quote=x=>",html)
        self.assertIn("const safeText=x=>",html)
        self.assertIn(r"/^[\u0000-\u0020]*[=+\-@]/.test(s)",html)
        self.assertIn('?"\'"+s:s',html)
        self.assertIn("quote(safeText(r.name))",html)
        self.assertIn("td.textContent=x",html)
        self.assertNotIn("innerHTML",html)
        self.assertNotIn('/*__DATA__*/',html)

    def test_pages_deploy_is_limited_to_main(self):
        workflow=(ROOT/'.github'/'workflows'/'pages.yml').read_text(encoding='utf-8')
        self.assertIn(
            "if: github.event_name != 'pull_request' && github.ref == 'refs/heads/main'",
            workflow,
        )

    @unittest.skipUnless(shutil.which('node'), 'Node.js is not installed')
    def test_previous_month_comparison_handles_year_boundary_and_gaps(self):
        html=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        match=re.search(r'function consecutiveMonths\(previous,current\)\{[^}]+\}',html)
        self.assertIsNotNone(match)
        cases=[['2025-12','2026-01'],['2025-11','2026-01'],
               ['2026-01','2025-12'],['2025-04','2025-05']]
        script=(match.group(0)+';const cases='+json.dumps(cases)
                +';console.log(JSON.stringify(cases.map(([a,b])=>consecutiveMonths(a,b))));')
        result=subprocess.run([shutil.which('node'),'-e',script],check=True,
                              capture_output=True,text=True)
        self.assertEqual(json.loads(result.stdout),[True,False,False,True])
if __name__=='__main__':unittest.main()
