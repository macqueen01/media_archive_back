
class ProcessControl():

    def __init__(self):
        self.PROCESS_STATUS = {}

    def add(self, id, process):
        self.PROCESS_STATUS[id] = process
        return None
    
    def remove(self, id):
        if self.PROCESS_STATUS[id]:
            process = self.PROCESS_STATUS[id]
            self.PROCESS_STATUS[id] = None
            return process
        else:
            return None
            
    def get(self, id):
        if self.PROCESS_STATUS[id]:
            return self.PROCESS_STATUS[id]
        else:
            return None
    
