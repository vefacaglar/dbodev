class Numbers: 
    def __init__ (self,_id = 0,index = 0,number = 0):
        self._id = _id
        self.index = index
        self.number = number

    def ToString(self):
        print("id:",self._id,"index:",self.index,"number:",self.number)

    def CollectionName(self):
        return "numbers"