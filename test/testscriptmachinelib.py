# Copyright (c) 2009 Matt Harrison

import unittest
import subprocess

import scriptmachinelib
from scriptmachinelib import statemachine as sm

class Echo(sm.Node):
    def run(self, ps=None):
        self.state['output'] = ps

class MatchFoo(sm.Node):
    def matches(self, parent_state=None):
        if parent_state and parent_state['output'] == 'foo':
            return True
        return False


class Loop3(sm.Node):
    def matches(self, parent_state=None):
        if parent_state and parent_state['output'] < 3:
            return True
        return False
    def run(self, ps=None):
        count = self.state.get('output', 0)
        self.state['output'] = count + 1
    
class TestScriptmachinelib(unittest.TestCase):
    def test_simple(self):
        n1 = sm.Node('n1')
        n2 = sm.FunctionNode('n2', ''.join, ['foo', 'bar'])
        n3 = sm.CmdNode('n3', 'ls', stdout=subprocess.PIPE)
        n1.add_child(n2)
        n2.add_child(n3)
        s = sm.StateMachine(n1)
        s.run()
        self.assertEquals(s.run_list, ['n1', 'n2', 'n3'])

    def test_input(self):
        
        n1 = Echo('n1')
        s = sm.StateMachine(n1)
        s.run('foo')
        self.assertEquals(n1.state['output'], 'foo')

    def test_branch(self):
        n1 = Echo('n1')
        n2 = MatchFoo('n2')
        n3 = sm.Node('default')
        n1.add_child(n2)
        n1.add_child(n3)
        s = sm.StateMachine(n1)
        s.run()
        self.assertEquals(s.run_list, ['n1', 'default'])
        s.reload()
        s.run('foo')
        self.assertEquals(s.run_list, ['n1', 'n2'])

    def test_loop(self):
        n1 = Loop3('n1')
        n1.add_child(n1)
        s = sm.StateMachine(n1)
        s.run()
        self.assertEquals(s.run_list, ['n1', 'n1', 'n1'])
if __name__ == '__main__':
    unittest.main()
