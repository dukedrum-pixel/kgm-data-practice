import unittest,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BuildTest(unittest.TestCase):
    def test_build(self):
        subprocess.run([sys.executable,str(ROOT/'scripts'/'build.py')],cwd=ROOT,check=True)
        html=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        self.assertIn('강판 가격지수',html)
        self.assertIn('filtered_data.csv',html)
        self.assertNotIn('/*__DATA__*/',html)
if __name__=='__main__':unittest.main()
