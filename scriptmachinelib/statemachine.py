"""
>>> n1 = Node('n1')
>>> n2 = FunctionNode('n2', ''.join, ['foo', 'bar'])
>>> n3 = CmdNode('n3', 'ls', stdout=subprocess.PIPE)
>>> n1.add_child(n2)
>>> n2.add_child(n3)
>>> sm = StateMachine(n1)
>>> sm.run()
>>> sm.run_list
['n1', 'n2', 'n3']

"""

import subprocess

NOT_RUN = 'not_run'
FINISHED = 'finished'


class Node(object):
    """
    
    """
    def __init__(self, name):
        self.name = name
        self.children = []
        self.state = { 'status': NOT_RUN }

    def run(self, parent_state=None):
        """
        parent_state is a dictionary that contains result of parent and status
        """
        pass

    def next_node(self):
        for child in self.children:
            if child.matches(self.state):
                return child
        return None

    def matches(self, parent_state_map):
        """
        Given a potential parent's output determine if you are ready
        to execute
        """
        return True

    def add_child(self, child):
        self.children.append(child)

    def success(self):
        """
        Node was executed successfully
        """
        return True
    
class FunctionNode(Node):
    def __init__(self, name, func, *args, **kw):
        Node.__init__(self, name)
        self.func = func
        self.args = args
        self.kw = kw

    def run(self, parent_state=None):
        result = self.func(*self.args, **self.kw)
        self.state['result'] = result
        self.state['status'] = FINISHED

class CmdNode(Node):
    def __init__(self, name, cmd, *args, **kw):
        """
        run cmd as subprocess.Popen, *kw are application Popen params
        """
        Node.__init__(self, name)
        self.cmd = cmd
        self.args = args
        self.kw = kw

    def run(self, parent_state=None):
        p = subprocess.Popen(self.cmd, *self.args, **self.kw)
        self.state['returncode'] = p.returncode
        if p.stdout:
            self.state['stdout'] = p.stdout.read()
        if p.stderr:
            self.state['stderr'] = p.stderr.read()
        self.state['status'] = FINISHED

    def sucess(self):
        return self.state['status'] == 0
    
class StateMachine(object):
    def __init__(self, start_node):
        self.start_node = start_node
        self.node_map = {start_node.name:start_node}
        self.cur_node = self.start_node
        self.run_list = []
        self.exhausted = False
        
    def run(self, parent_state=None):
        done = False
        while not done:
            self.cur_node.run(parent_state)
            self.run_list.append(self.cur_node.name)
            if not self.cur_node.success():
                done = True
            self.cur_node = self.cur_node.next_node()
            if not self.cur_node:
                done = True
        self.exhausted = True
    
    def reload(self):
        self.exhausted = False
        self.run_list = []
        self.cur_node = self.start_node

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

        
        
    
