import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import string
import random



html=urlopen( "https://en.wikipedia.org/wiki/Rabat" ).read()
html2=urlopen( "https://en.wikivoyage.org/wiki/Rabat" ).read()


clean_text=' '.join(BeautifulSoup(html, "html.parser" ).stripped_strings )
clean_text2=' '.join(BeautifulSoup(html2, "html.parser" ).stripped_strings )


lower_text=clean_text.lower()
lower_text2=clean_text2.lower()

out = lower_text.translate(str.maketrans('', '', string.punctuation))
out2 = lower_text2.translate(str.maketrans('', '', string.punctuation))


#Etape 1 : Modélisation du texte comme succession de lettres (Chaine de Markov d’ordre 1) :

def indice(lettre):
    if (ord(lettre) >=ord('a') and ord(lettre)<=ord('z')) or lettre  ==" " :
        if(lettre==" "):
            return 0
        else:
            asci=ord(lettre)-ord('a')+1
    else :
        asci = -1
    return asci

def incre(text):
    M=np.zeros((27,27))
    for i in range(0,len(text)-1):
        if indice(text[i]) != -1 and indice(text[i+1]) != -1:
            M[indice(text[i])][indice(text[i+1])]=M[indice(text[i])][indice(text[i+1])]+1
    return M     


m = incre(out)
compteur = np.zeros(27)
incre(out)
for i in range(27):
    compteur[i]=sum(m[i])


proba=np.zeros((27,27))
for i in range(27):
    proba[i] = m[i]/compteur[i]



tentative = 0
score  = 0


def incre2(text):
    M=np.zeros((27,27))
    s=np.zeros((27,27))
    tentative =np.zeros((27,27))
    for i in range(0,len(text)-1):
        if indice(text[i]) != -1 and indice(text[i+1]) != -1:
            tentative[indice(text[i])][indice(text[i+1])]+=1
            M[indice(text[i])][indice(text[i+1])]=M[indice(text[i])][indice(text[i+1])]+proba[indice(text[i])][indice(text[i+1])]
    for i in range(27):
        for j in range(27):
            s[i][j]=M[i][j]/tentative[i][j]            
        
    return s



m2=incre(out2)
proba2=np.zeros((27,27))
for i in range(27):
    proba2[i] = m2[i]/compteur[i]


#on remarque que les  deux matrices celle qui se base sur la probabilté du premier text et celle qui se limite 

#PATIE 3

def indice_multi(lettre):
    return ord(lettre)-ord('a')



def incre_multi(text):
    M=np.zeros((26,26,26,26))
    for i in range(0,len(text)-3):
        M[indice_multi(text[i])][indice_multi(text[i+1])][indice_multi(text[i+2])][indice_multi(text[i+3])]=+1
        print("oui")
    return M     



#Etape 4 : Modélisation du texte comme succession de mots:

def list_mot(text):
    liste = text.split()
    nbrListe = list(set(liste))
    return nbrListe


def matrice4(text):
    list_text = text.split()
    mots = list(set(list_text))
    M= np.zeros((len(mots),len(mots)))
    for i in range (len(list_text)-1) :
        M[mots.index(list_text[i])][mots.index(list_text[i+1])]+=1
    return M

#Etape 5 : Génération de texte avec un modèle de Markov:

def proba_gene(m):
    compteur = np.zeros(len(m))
    for i in range(len(m)):
        compteur[i]=sum(m[i])
        proba=np.zeros((len(m),len(m)))
        for i in range(len(m)):
            proba[i] = m[i]/compteur[i]
    return proba


def mot_suivant(nb,m):
        i=0
        while nb > m[i]:
            i=i+1
        
        return(i)

def poid_uniforme(text,pro,mot):
        ma = matrice4(text)
        list_text = text.split()
        mots = list(set(list_text))
        indice=mots.index(mot)
        ligne_proba=proba_gene(ma)[indice]
        m=np.zeros(len(ligne_proba))
        m=np.cumsum(ligne_proba)
        res=mot_suivant(random.random(),m)
        return mots[res] 

def generalis(text,nb_mot):
    chaine= " "
    t=matrice4(text)
    list_text = text.split()
    pro=proba_gene(t)
    mots = list(set(list_text))
    mot =mots[random.randint(0,len(mots)-1)]
    chaine= chaine+mot+" " 
    for i in range(nb_mot): 
        mot=poid_uniforme(text,pro,mot)
        chaine= chaine+mot+" " 
    print(chaine)


teext =" Jennie Fletcher est issue de la classe ouvrière : son père tient une petite boutique, mais elle et ses frères et sœurs travaillent en usine. Elle profite d'un programme d'apprentissage de la natation dans les écoles primaires de Leicester. "

generalis(teext,50)
