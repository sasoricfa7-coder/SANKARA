import sys
import os
import json

rouge = "\033[1m\033[91m"
simple = "\033[0m"
vert = "\033[1m\033[92m"
nom_table = "correspondance.json"

def arret() :
    sys.exit(1)

def verifie_debut() :
    if len(sys.argv) > 1 :
        nom_fichier = (sys.argv[1])
    else :
        print(f"{rouge} Erreur le script lancer seul ne sert pas.{simple}")
        arret()

    tuple_temporaire = os.path.splitext(nom_fichier)
    if tuple_temporaire[1] != ".sk" :
        print(f"{rouge} Erreur l'extension inconnu{simple}")
        print(f"Extension correct {vert} : .sk{simple}")
        arret()

    return nom_fichier

def charger(nom_fichier) :
    dictionnaire = {}
    with open(nom_table, "r", encoding="utf-8") as f :
        table_correspondance = json.load(f)

    with open(nom_fichier, "r", encoding="utf-8") as f :
        for numero, ligne in enumerate (f, start=1) :
            dictionnaire[numero] = ligne.rstrip().replace("\t", "    ")
            print(f"[ligne {numero}] = {ligne.rstrip()}")

    return dictionnaire, table_correspondance

def indentation(dictionnaire) :
    dictionnaire_final = {}
    dictionnaire_commentaire = {}
    dict_longueur_commentaire = {}
    valide = False
    chaine_commentaire = ""
    for i, ligne in dictionnaire.items() :
        if ligne == "" :
            continue
        nbr_espace = len(ligne) - len(ligne.lstrip())
        if ((nbr_espace % 4) != 0) :
            print("Mal indenté")
            print(f"{rouge} [ligne : {i}] : {ligne} {simple}")
            arret()

        if "/*" in ligne or valide :
            fin = False
            valide = True
            index = ligne.find("/*")
            index_depart = index # pour pouvoir bien replacer les commentaires dans la code source rust generer

            if "*/" in ligne :
                marge = ligne.find("*/") + 2
                valide = False
            else :
                marge = len(ligne)
            for index in range(marge) :
                chaine_commentaire += ligne[index]

            dictionnaire_commentaire[i] = chaine_commentaire
            dict_longueur_commentaire[index_depart] = len(chaine_commentaire) # J'enregistre d'abord 
            chaine_commentaire = "" # regarde c'est après avoir enregistrer la longueur que je vide 

            continue

        elif "//" in ligne :
            index = ligne.find("//")

            if index != -1 and ligne[:index].isspace() :
                dictionnaire_commentaire[i] = ligne
                dict_longueur_commentaire[index] = len(ligne)

            else :
                temporaire = ligne
                ligne = ligne[:index]
                dictionnaire_commentaire[i] = temporaire[index:]
                dict_longueur_commentaire [index] = len(temporaire[index:])

        niveau_indentation = nbr_espace // 4
        ligne_info = {
            "niveau_indentation" : niveau_indentation,
            "contenu" : ligne.lstrip()
        }
        dictionnaire_final[i] = ligne_info
        


    return dictionnaire_final, dictionnaire_commentaire, dict_longueur_commentaire

def main() : # La fonction principale
    nom_fichier =  verifie_debut()
    dictionnaire, table_correspondance = charger(nom_fichier)
    dictionnaire_final, dictionnaire_commentaire, dict_longueur_commentaire =  indentation(dictionnaire)

    for i, j in dictionnaire_final.items() :
        print(i, j.items())

    for i, j in dictionnaire_commentaire.items() :
        print(i, j.items())

    for i, j in dict_longueur_commentaire.items() :
        print(i, j.items())

if __name__ == "__main__" :
    main()
