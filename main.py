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
    for i, ligne in dictionnaire.items() :
        if ligne == "" :
            continue
        nbr_espace = len(ligne) - len(ligne.lstrip())
        if ((nbr_espace % 4) != 0) :
            print("Mal indenté")
            print(f"{rouge} [ligne : {i}] : {ligne} {simple}")
            arret()

        if "//" in ligne : # c'est exprès on verifie d'abord que le code est bien identé
            index = ligne.find("//")

            if index == 0:
                dictionnaire_commentaire[i] = ligne
                continue

            else :
                temporaire = ligne
                ligne = ligne[:index]
                dictionnaire_commentaire[i] = temporaire[index:] # pas besoin de savoir ou était placer, a ce stade le commentaire est à la fin

        niveau_indentation = nbr_espace // 4
        ligne_info = {
            "niveau_indentation" : niveau_indentation,
            "contenu" : ligne.lstrip()
        }
        dictionnaire_final[i] = ligne_info
        


    return dictionnaire_final, dictionnaire_commentaire

def main() : # La fonction principale
    nom_fichier =  verifie_debut()
    dictionnaire, table_correspondance = charger(nom_fichier)
    dictionnaire_final, dictionnaire_commentaire =  indentation(dictionnaire)

    for i, j in dictionnaire_final.items() :
        print(i, j.items())

    for i, j in dictionnaire_commentaire.items() :
        print(i, j)

if __name__ == "__main__" :
    main()
