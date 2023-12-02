import time
import unittest
from lib.HTMLTestRunner_PY3 import HTMLTestRunner

import app
from script.login import login

suite=unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))

report_file=app.BASE_DIR+"/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))

with open(report_file,'wb')as f:
    runner=HTMLTestRunner(f,title="P2P金融项目",description="test")
    runner.run(suite)
