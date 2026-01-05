from urllib.request import urlopen
import json, requests, pandas, os
from tkinter.ttk import *
from tkinter import *
from figure import Figure
#from repository import Repository

def create_repository(urlsByBrand, dirPath):
    print("Creating Repository")
    figureRepositoryList = []
    
    for brand in urlsByBrand:
        response = requests.get(urlsByBrand.get(brand))
        
        if response.status_code == 200:
            html_content = response.content
            data = pandas.read_html(html_content)
            sortedData = data[0]
            
            for index, row in data[0].iterrows():
            
                if not pandas.isnull(row.tolist()[0]):
                    item = Figure(row.tolist(), brand)
                    figureRepositoryList.append(item)
            
        else:
            print("Error: Figure list unable to be retreived.")
            
    figureRepositoryList = sorted(figureRepositoryList, key = lambda x: (x.brand, x.name))
    
    figureRepositoryFrame = pandas.DataFrame(columns = ["Name", "Brand", "Wave", "Release Year", "Source"])
    
    for x in figureRepositoryList:
        figureRepositoryFrame.loc[len(figureRepositoryFrame)] = x.tolist()
        
    figureRepositoryFrame.to_excel(dirPath + "/figureRepository.xlsx", index = False)
    
    return figureRepositoryFrame
        
def update_repository(figureRepository, urlsByBrand, dirPath):
    print("Updating Repository")
    
    for brand in urlsByBrand:
        response = requests.get(urlsByBrand.get(brand))
        
        if response.status_code == 200:
                html_content = response.content
                data = pandas.read_html(html_content)
                sortedData = data[0]
                
                for index, row in data[0].iterrows():
                    
                    if not pandas.isnull(row.tolist()[0]):
                        item = Figure(row.tolist(), brand)
                        
                        if item.tolist() not in figureRepository.values.tolist():
                            print("Adding " + item.name)
                            figureRepository.loc[len(figureRepository)] = item.tolist()
                            
    figureRepository = figureRepository.sort_values(by=['Brand', 'Name']).reset_index(drop=True)
    figureRepository.to_excel(dirPath + "/figureRepository.xlsx", index = False)
                      
    return figureRepository

def sort_tree(repository, tree, columnName, reverse):
    
    repository = repository.sort_values(by = columnName, ascending = not reverse).reset_index(drop=True)

    tree.delete(*tree.get_children())
        
    for col in repository.columns:
        tree.heading(col, text=col, command = lambda col = col: sort_tree(repository, tree, col, reverse if columnName != col else not reverse))
        tree.column(col, width=100)
        
    for _, row in repository.iterrows():
        tree.insert("", "end", values=list(row))
        
    
if __name__ == "__main__":
    
    urlsByBrand = {"McFarlane Toys": "https://www.mephitsu.co.uk/mcfarlane-directory", "Marvel Legends": "https://www.mephitsu.co.uk/marvel-legends"}
    dirPath = "C:/Users/andre/Documents/VS Code/Collection/Repositories"
    
    root = Tk()
    root.geometry("1000x300")
    root.title("Collection Manager")
    
    menubar = Menu(root)
        
    menubar.add_command(label = "Available Figures")
    
    collectionList = Menu(menubar, tearoff=0)
    
    for collection in os.listdir(dirPath + "/Stored Collections/"):
        collectionList.add_command(label = collection[:-5])
        
    menubar.add_cascade(label="Collections", menu = collectionList)
    menubar.add_command(label = "Exit", command = root.destroy)
    
    root.config(menu = menubar)
    
    try:
        figureRepository = update_repository(pandas.read_excel(dirPath + "/figureRepository.xlsx"), urlsByBrand, dirPath)
    except FileNotFoundError:
        figureRepository = create_repository(urlsByBrand, dirPath)
        
    tree = Treeview(root,  columns = list(figureRepository.columns), show = 'headings')
    tree.pack(expand=True, fill='both')
    
    for col in figureRepository.columns:
        tree.heading(col, text=col, command = lambda col = col: sort_tree(figureRepository, tree, col, False))
        print(col)
        
    for _, row in figureRepository.iterrows():
        tree.insert("", "end", values=list(row))
        
    root.mainloop()