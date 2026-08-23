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

            if index != -1 and ligne[:index].isspace() :
                if ligne[2:] != "" :
                    dictionnaire_commentaire[i] = ligne # C'est un choix un commentaire vide sert à quoi ?
                continue

            elif index == 0 :
                if ligne[2:] != "" :
                    dictionnaire_commentaire[i] = ligne # C'est un choix un commentaire vide sert à quoi ?
                continue

            else :
                if ligne[index-1].isspace() : # On vérifie que le // au milieu est bien précédé d'un espace
                    temporaire = ligne
                    ligne = ligne[:index]
                    dictionnaire_commentaire[i] = temporaire[index:] # pas besoin de savoir ou était placer, a ce stade le commentaire est à la fin
                else :
                    pass # Si c'est collé (ex: une URL ou autre), on laisse passer comme du code normal !

        niveau_indentation = nbr_espace // 4
        ligne = ligne.strip() # on nettoie tout car on a déja calculer l'indentation
        
        if ligne.endswith(";") :
            print(f"{rouge}Erreur de syntaxe [ligne {i}] : Pas de point-virgule (;) dans ce langage !{simple}")
            arret()
            
        ligne_info = {
            "niveau_indentation" : niveau_indentation,
            "contenu" : ligne
        }
        dictionnaire_final[i] = ligne_info
        


    return dictionnaire_final, dictionnaire_commentaire

def pile_indentation() :
    global dictionnaire_final
    if not dictionnaire_final :
        print(f"Erreur : {rouge} Fichier vide ou sans code exploitable. {simple}")
        arret()
        
    pre = next(iter(dictionnaire_final))
    if dictionnaire_final[pre]["niveau_indentation"] != 0 :
        print(f"Erreur d'indentation : {rouge} 0 comme niveau initiale est obligatoire{simple}")
        arret()

    L = [0]
    for i, info in dictionnaire_final.items() :
        niveau_indentation = info["niveau_indentation"]
        sommet_actu = L[-1]

        if niveau_indentation > sommet_actu and ((niveau_indentation - sommet_actu) == 1) :
            L.append(niveau_indentation)
            dictionnaire_final[i]["reçoit"] = "{"
            continue

        elif niveau_indentation < sommet_actu :
            s = 0
            while L and L[-1] > niveau_indentation:
                L.pop()
                s += 1
            if L[-1] != niveau_indentation :
                print("identation non respecter.")
                print(i, " : ", info["contenu"])
                arret()
                
            dictionnaire_final[i]["nombre_fermeture"] = s
            dictionnaire_final[i]["reçoit"] = "}" * s
            
            continue

        elif niveau_indentation == sommet_actu :
            continue

        else :
            print("identation non respecter.")
            print(i, " : ", info["contenu"])
            arret()

    if L[-1] != 0 :
        s = 0
        while L and L[-1] > 0 :
            L.pop()
            s += 1
        dernière_ligne = list(dictionnaire_final.keys())[-1]
        dictionnaire_final[dernière_ligne]["reçoit"] = dictionnaire_final[dernière_ligne].get("reçoit", "") + "}" * s
        
    return L

def main() : # La fonction principale
    global dictionnaire_final
    nom_fichier =  verifie_debut()
    dictionnaire, table_correspondance = charger(nom_fichier)
    dictionnaire_final, dictionnaire_commentaire =  indentation(dictionnaire)

    pile = pile_indentation() # Il va utiliser le dictionnaire globalement car si le code est lourd je gaspillerai la rame

    for i, j in dictionnaire_final.items() :
        print(i, j)
        
if __name__ == "__main__" :
    dictionnaire_final = {}
    main()
