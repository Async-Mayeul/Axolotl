import unittest
from io import StringIO
import sys
import requests
sys.path.insert(0, '../src/axolotl_c2/')
import listener

class TestListener(unittest.TestCase):

    def setUp(self):
        self.name = 'biggardListener'
        self.port = 5001
        self.ipaddress = '127.0.0.1'
        self.pingRes = {'message': 'pong'}
        self.agentConf = {
            'name': 'biggardAgent', 
            'ip': '127.0.0.1', 
            'hostname': 'linux', 
            'key': '1234'
        }
        self.taskConf = {
            'type': 'shell',
            'agent': 'biggardAgent',
            'command': 'id'
        }
        self.result = {
            'agent': 'biggardAgent',
            'result': 'uid=1000(victim) gid=1000(victim) groupes=1000(victim)'
        }

        self.listener = listener.Listener(self.name,self.port,self.ipaddress)
        self.listener.start()

    def test_startlistener(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        listener.start()
        sys.stdout = sys.__stdout__
        print('[Test] : {}'.format(capturedOutput.getvalue()))
    
    def test_ping(self):
        r = requests.get('http://127.0.0.1:5001/ping')
        self.assertEqual(r.json, self.pingRes)

    def test_register(self):
        r = requests.post('http://127.0.0.1:5001/register', data=self.agentConf)
        agentName = self.listener.agentsList['biggardAgent'].getName()
        self.assertEqual(agentName, 'biggardAgent')

    def test_settask(self):
        r = requests.post('http://127.0.0.1:5001/setTask', data=self.taskConf)
        agentTask = self.listener.agentsList['biggardAgent'].getTask()
        self.assertEqual(agentTask.tastType, 'shell')

    def test_gettask(self):
        r = requests.get('http://127.0.0.1:5001/getTask?agent=biggardAgent')
        assertTrue(r.status_code)

    def test_getresult(self):
        r = requests.post('http://127.0.0.1:5001/postResult', data=self.result)
        result = requests.get('http://127.0.0.1:5001/getResult?agent=biggardAgent')
        assertTrue(result.status_code)

if __name__ == '__main__':
    unittest.main()
