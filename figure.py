class Figure():
    def __init__(self, dfRow, brand):
        self.name = dfRow[0]
        self.brand = brand
        self.release = int(dfRow[4])
        self.wave = dfRow[6]
        self.source = dfRow[7]
        
    def __str__(self):
        return f"{self.name}, {self.brand}, {self.wave}, {self.release}, {self.source}"
    
    def tolist(self):
        return [self.name, self.brand, self.wave, self.release, self.source]
    