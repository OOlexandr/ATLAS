class Field:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value