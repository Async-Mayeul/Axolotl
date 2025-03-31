import unittest
import os
import sys
sys.path.insert(0, '../src/axolotl_c2/')
import task

class testTask(unittest.TestCase):

    def setUp(self):
        self.result = 'uid=1000 gid=1000 group=wookiee'
        self.path = '/tmp/biggardAgent'
        self.taskPath = '/tmp/biggardAgent/task'
        if not(os.path.exists(self.path)):
            os.mkdir(self.path)
        self.taskShell = task.TaskShell(self.taskPath, 'id')

    def test_writetask(self):
        with open(self.taskPath, 'r') as f:
            self.assertEqual(f.read(), 'shell:id')

    def test_cleartask(self):
        self.taskShell.clearTask()
        self.assertFalse(os.path.exists(self.taskPath))

    def test_receiveresult(self):
        self.taskShell.receiveResult(self.result)
        self.assertEqual(self.taskShell.getResult(), self.result)

if __name__ == '__main__':
    unittest.main()
