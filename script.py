from IPython.display import Image
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import requests_cache
import pandas as pd
import csv
requests_cache.install_cache("bases_scraping", expire_after=10e5)


listeLien=[]
listeCategorie=[]
listePrix=[]
listePhoto=[]
listeTaille=[]
listePiece=[]
listeVille=[]
listeCodePostal=[]

for i in range(1,2): #21000
    url = "https://www.logic-immo.com/vente-immobilier/options/grouplocalities=1_0,13_0,6_0,4_0,8_0,3_0,2_0,9_0,11_0,10_0,5_0,7_0,12_0,14_0,15_0,16_0,17_0,18_0,19_0,20_0,21_0,22_0/groupprptypesids=1,2,7"
    if i!=1:
        url = url+"/page="+str(i)

    #print(url)
    response = requests.get(url)
    response
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "lxml")
    
    # On recupere tous les liens
    rows1 = soup.find_all("nav", {"id": "meaOrpiAnnouncesList"})
    rows2 = soup.find_all("nav", {"id": "announcesList"})
    rows=rows1+rows2
        
    for i in rows:
        #lien
        data = i.find_all("a", {"class": "linkToFa"})
        print(data)
        for lien in data:
            lien=lien['href']
            listeLien.append(lien)

        #categorie
        data = i.find_all("span",{"class":"announceDtlInfosPropertyType"})
        for categorie in data:
            listeCategorie.append(categorie.text.strip())
            
        #taille
        data = i.find_all("span",{"class":"announceDtlInfosArea"})
        for taille in data:
            listeTaille.append(taille.text.strip())
            
        #piece
        data = i.find_all("span",{"class":"announceDtlInfosNbRooms"})
        for piece in data:
            listePiece.append(piece.text.strip())
            
        #prix
        data = i.find_all("span",{"class":"announceDtlPrice"})
        for prix in data:
            listePrix.append(prix.text.strip())
            
        #photo
        data = i.find_all("img",{"class":"announcePicture"})
        for photo in data:
            photo=photo['src']
            listePhoto.append(photo)
            
        #Ville+CP
        data = i.find_all("div",{"class":"announcePropertyLocation"})
        for villeCp in data:
            cpt=0
            for elem in villeCp:
                if cpt==0:
                    ville,code=str(elem).split("(")
                    #ville
                    listeVille.append(ville.strip())
                    #code postal
                    listeCodePostal.append(code.strip()[:-1])
                    cpt+=1

#On cree dataframe avec les differentes entetes
df = pd.DataFrame({'Lien': listeLien, 'Photo': listePhoto,
                   'Categorie': listeCategorie, 'Taille': listeTaille,
                   'Piece': listePiece,'Prix': listePrix, 
                   'Ville': listeVille,'Code-Postal': listeCodePostal })
df.index.name = 'Index'

#On cree un fichier csv dans lequel on va ajouter nos donnees
df.to_csv("dataImmo.csv", sep=';',encoding="utf-8-sig")

