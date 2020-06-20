
class POC(object):
    def __init__(self):
        self.target = None
        self.url = None
        self.path = None
        self.params = None
        self.mode = None
        self.headers = None
        self.protocol = getattr(self, "poc_info")['protocol']
        self.pocDesc = getattr(self,"poc_info")['desc']
    
    def _execute(self):
        if self.mode == 'check':
            self._check()
        elif self.mode == 'exploit':
            self._exploit()

    def auto_execute(self, target, mode = 'check'):
        self.target = target
        self.mode = mode

        self._execute()

    def _check(self):
        raise NotImplementedError
    
    def _exploit(self):
        raise NotImplementedError
    
    