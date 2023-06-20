class data_storage:
    def __init__(self,filename):
        self.filename = filename

    def save_to_file(self,data):
        
        with open(self.filename,'a') as log:
            log.write(str(data) + ",")
        log.close()
    

data = data_storage("hello.txt")
data.save_to_file(34)
