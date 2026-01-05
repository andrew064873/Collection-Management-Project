import requests, pandas, os

class Repository:
    def __init__(self, owner):
        self.owner = owner
        self.repository = pandas.DataFrame(columns = ["Name", "Brand", "Wave", "Release Year", "Source"])
        self.columns = self.repository.columns
        
        if owner != "master":
            self.initialize_collection(owner)
        else:
            self.fileLoc = os.getcwd().replace("\\", "/") + "/Repositories"
            self.fileName = "figureRepository.xlsx"
        
    def save(self):
        self.repository.to_excel(f"{self.fileLoc}/{self.fileName}", index = False)
        
    def saveNew(self):
        if os.path.exists(f"{self.fileLoc}/{self.fileName}"):
            print("do not overwrite")
        else:
            self.repository.to_excel(f"{self.fileLoc}/{self.fileName}", index = False)
        
    def iterrows(self):
        return self.repository.iterrows()
    
    def sort_values(self, byVal, reverse):
        self.repository = self.repository.sort_values(by = byVal, ascending = not reverse).reset_index(drop = True)
            
    def load_repository(self, owner):
        if owner == "master":
            self.fileLoc = os.getcwd().replace("\\", "/") + "/Repositories"
            self.fileName = "figureRepository.xlsx"
        else:
            self.fileName = "{owner}'s Collection.xlsx"
            self.fileLoc = os.getcwd().replace("\\", "/") + "Repositories/Stored Collections/{self.fileName}"
        
        self.owner = owner
        self.repository = pandas.read_excel(self.fileLoc + "/" + self.fileName)
                    
    def create_repository(self, urlsByBrand):
        if self.owner != "master":
            return
        
        figureRepositoryList = []
        
        for brand in urlsByBrand:
            response = requests.get(urlsByBrand.get(brand))
            
            if response.status_code == 200:
                html_content = response.content
                data = pandas.read_html(html_content)
                sortedData = data[0]
                
                for index, row in data[0].iterrows():
                
                    if not pandas.isnull(row.tolist()[0]):
                        figureRepositoryList.append([row.tolist()[0], brand, row.tolist()[6], int(row.tolist()[4]), row.tolist()[7]])
                
            else:
                print("Error: Figure list unable to be retreived.")
                  
        for item in figureRepositoryList:
            self.repository.loc[len(self.repository)] = item
            
        self.repository.sort_values(by=['Brand', 'Name']).reset_index(drop=True)
        self.save()
        
    def update_repository(self, urlsByBrand):
        if self.owner != "master":
                return
        self.load_repository("master")
            
        print("Updating Repository")
        
        for brand in urlsByBrand:
            response = requests.get(urlsByBrand.get(brand))
            
            if response.status_code == 200:
                    html_content = response.content
                    data = pandas.read_html(html_content)
                    sortedData = data[0]
                    
                    for index, row in data[0].iterrows():
                        
                        if not pandas.isnull(row.tolist()[0]):
                            item = [row.tolist()[0], brand, row.tolist()[6], int(row.tolist()[4]), row.tolist()[7]]
                            
                            if item not in self.repository.values.tolist():
                                print("Adding " + item[0])
                                self.repository.loc[len(self.repository)] = item
                                
        self.repository = self.repository.sort_values(by=['Brand', 'Name']).reset_index(drop=True)
        self.save()
        
    def initialize_collection(self, owner):
        self.fileLoc = os.getcwd().replace("\\", "/") + "/Repositories/Stored Collections/"
        self.fileName = f"{owner}'s Collection.xlsx"
        
        self.saveNew()
    