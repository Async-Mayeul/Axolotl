import unittest
import os
import sys
sys.path.insert(0, '../src/axolotl_c2/')
import agent
import task

class TestAgent(unittest.TestCase):
    
    def setUp(self):
        self.path = '/tmp/biggardAgent'
        self.taskPath = '/tmp/biggardAgent/task'
        if not(os.path.exists(self.path)):
            os.mkdir(self.path)
        self.task = task.TaskShell(self.taskPath, 'id')
        self.agent = agent.Agent(
            'TestAgent', 
            '127.0.0.1', 
            'hostname', 
            'superkey'
        )

    def test_setname(self):
        self.agent.setName('biggard')
        self.assertEqual(self.agent.getName(), 'biggard')

    def test_agenttask(self):
        self.agent.setTask(self.task)
        self.assertEqual(self.agent.getTask().taskType, 'shell')
        with open(self.taskPath, 'r') as f:
            self.assertEqual(f.read(), 'shell:id')

if __name__ == '__main__':
    unittest.main()
