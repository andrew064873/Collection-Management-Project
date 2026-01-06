from urllib.request import urlopen
import json, requests, pandas, os
from tkinter.ttk import *
from tkinter import *
from tkinter import simpledialog
from repository import Repository

repoPath = os.getcwd().replace("\\", "/") + "/Repositories"

def update_collection_tree():  
    
    collectionList.delete(0, 'end')
    
    collectionList.add_command(label = "Create New Collection", command = create_collection)
    
    for collection in os.listdir(repoPath + "/Stored Collections/"):
        collectionList.add_command(label = collection[:-5])
        
def update_collection_menu():
    pass
    
def create_collection():
    owner = simpledialog.askstring("Create new collection.", "Please enter the collection owner's name.")
    collection = Repository(owner)
    
    update_collection_tree()
    
def load_collection(collectionPath):
    pass

def sort_tree(repository, columnName, reverse):
    
    repository.sort_values([columnName, "Name"], reverse)

    tree.delete(*tree.get_children())
        
    for col in repository.columns:
        tree.heading(col, text=col, command = lambda col = col: sort_tree(repository, col, reverse if columnName != col else not reverse))
        tree.column(col, width=100)
        
    for _, row in repository.iterrows():
        tree.insert("", "end", values=list(row))
        
if __name__ == "__main__":
    urlsByBrand = {"McFarlane Toys": "https://www.mephitsu.co.uk/mcfarlane-directory", 
                   "Marvel Legends": "https://www.mephitsu.co.uk/marvel-legends"}
        
    root = Tk()
    root.geometry("1000x300")
    root.title("Collection Manager")
    
    menubar = Menu(root)
        
    menubar.add_command(label = "Available Figures")
      
    if not os.path.isfile(repoPath + "/Stored Collections/"):
        os.makedirs(repoPath + "/Stored Collections/", exist_ok = True)
        
    collectionList = Menu(menubar, tearoff=0)
    
    update_collection_tree()
   
    menubar.add_cascade(label="Collections", menu = collectionList)
    menubar.add_command(label = "Exit", command = root.destroy)
    
    root.config(menu = menubar)
    
    figureRepository = Repository("master")
    
    collectionMenu = ["Create a new collection."]
    init_disp = StringVar(root)
    init_disp.set("Select Active Collection")
    
    activeCollectionMenu = OptionMenu(root, init_disp, *collectionMenu)
    activeCollectionLabel = Label(root, text = "Select Active Collection")
    activeCollectionLabel.pack(expand = True, side = LEFT, anchor = NW)
    activeCollectionMenu.pack(expand=True, side=LEFT, anchor = N)
    update_collection_menu()
    
    tree = Treeview(root,  columns = list(figureRepository.columns), show = 'headings')
    tree.pack(expand=True, fill='both')
    
    if os.path.isfile(repoPath + "/figureRepository.xlsx"):
        figureRepository.update_repository(urlsByBrand)
        
    else:
        figureRepository.create_repository(urlsByBrand)
            
    for col in figureRepository.columns:
        tree.heading(col, text=col, command = lambda col = col: sort_tree(figureRepository, col, False))
                
    for _, row in figureRepository.iterrows():
        tree.insert("", "end", values=list(row))
            
    root.mainloop()
    
    