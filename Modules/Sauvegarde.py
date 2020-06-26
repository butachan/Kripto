# coding: utf8
import os
import time
import codecs
import base64
import hashlib


def TransformationChiffre(chaine):

    """Fonction qui renvoi sous forme de la liste d'entiers correspont chacun à la valeur
    unicode des caratères de la chaine précisée en arguments """

    liste = list(chaine)

    for index in range(len(liste)):
    # On récupere chaque caratères de la liste

        liste[index] = ord(liste[index])
        # ord(x) est la fonction qui pour tout charactère Unicode (sous type str) x renvoie sa valeur Unicode
        # Cette fonction transforme donc le message en une suite de chiffres qui correspond à leur valeur Unicode

    return liste
    # On renvoi la liste des caractères au format


def TransformationCaractères(ListeUnicode):

    """Fonction qui convertit la liste de numéros Unicode en une chaine de caractères
    correspondant à chacun des numéros convertis et mis bout à bout"""

    for index in range(len(ListeUnicode)):

        # Boucle de sécurité : Si jamais on doit convertir des nombres
        # ne rentrant pas dans la table de caractères Unicode

        if ListeUnicode[index] > 1114111 :

            # Les caractères Unicode vont de 0 à 1114111.
            # Si, à cause du cryptage, la valeur viendrait à quitter cette plage de donnée, cela provoquerait une erreur
            # On fait donc en sorte que les cactères restent toujours dans cette plage de donnée.

            ListeUnicode[index] = ListeUnicode[index] - 1114111

        elif ListeUnicode[index] < 0 :

            ListeUnicode[index] = ListeUnicode[index] + 1114111

        ListeUnicode[index] = chr(ListeUnicode[index])
        # chr(x) est la fonction qui pour toute valeur Unicode x nous renvoie son charactère Unicode (sous type str)
        # Cette fonction transforme donc la suite de charactère chiffrés sous forme Unicode en message

    return str("".join(ListeUnicode))


def ChiffrementVignère(MotDePasse, chaine) :

    """Fonction qui chiffre une chaine avec un mot de passe comme clef de chiffrement,
    selon la méthode de Vignère"""

    chaine = TransformationChiffre(chaine)
    # On transforme la chaine en chiffres

    MotDePasse = GénérationMotDePasseSécurisé(MotDePasse)
    MotDePasse = TransformationChiffre(MotDePasse)
    # On hash le mot de passe, afin d'obtenir un nombre plus élévé de caractères

    nombreItérationsVigenère = (len(chaine) // len(MotDePasse))+ 1
    # On calcule le nombre de fois où on aura besoin de répéter le mot de passe
    # pour pouvoir crypter le message entier selon la méthode Vigenère

    longueurItérationVigenère = len(MotDePasse)
    # On calcule la longueur du mot de passe pour savoir le nombre de
    # caractères cryptables selon Vigenère en n'utilisant qu'une seule fois
    # le mot de passe

    for x in range(0, nombreItérationsVigenère) :
    # x correspond au nombre de fois où l'on devra utiliser le mot de passe
    # pour appliquer la méthode de cryptage de Vigenère

        for y in range(0, longueurItérationVigenère) :
        # y correspond à la position du caractère du mot de passe utilisé
        # au sein du mot de passe pour crypter selon Vigenère

            try:

                chaine[x*longueurItérationVigenère+y] = chaine[x*longueurItérationVigenère+y] - MotDePasse[y]
                # On crypte chaque carractère selon Vigenère, en additionnant les valeurs des caractères du message et du mot de passe

            except IndexError:

                pass
                # Si on a fini de crypter tous les caractères mais que la boucle de cyptage continue
                # On ne fait rien


    chaine = TransformationCaractères(chaine)
    chaine = chaine.encode("utf-8")
    chaine = base64.b64encode(chaine)
    chaine = chaine.decode("utf-8")
    #On encode en base64

    return str(chaine)
    # On retourne le message chiffré, sous forme de caratères



def DéchiffrementVignère(MotDePasse, chaine):

    """ Fonction qui déchiffre une chaine avec un de mot de passe,
    selon la méthode de Vignère """

    chaine = chaine.encode("utf-8")
    chaine = base64.b64decode(chaine)
    chaine = chaine.decode("utf-8")

    print(MotDePasse)
    print(chaine)

    chaine = TransformationChiffre(chaine)
    # On transforme la chaine à chiffrer en liste d'entiers

    MotDePasse = GénérationMotDePasseSécurisé(MotDePasse)
    MotDePasse = TransformationChiffre(MotDePasse)
    # On hashe le mot le mot de passe, et on le transforme en liste d'entiers

    nombreItérationsVigenère = len(chaine) // len(MotDePasse) + 1
    # On calcule le nombre de fois où on aura besoin de répéter le mot de passe
    # pour pouvoir crypter le message entier selon la méthode Vigenère

    longueurItérationVigenère = len(MotDePasse)
    # On calcule la longueur du mot de passe pour savoir le nombre de
    # caractères cryptables selon Vigenère en n'utilisant qu'une seule fois
    # le mot de passe

    for x in range(0, nombreItérationsVigenère) :
    # x correspond au nombre de fois où l'on devra utiliser le mot de passe
    # pour appliquer la méthode de cryptage de Vigenère

        for y in range(0, longueurItérationVigenère):
        # y correspond à la position du caractère du mot de passe utilisé
        # au sein du mot de passe pour crypter selon Vigenère

            try:

                chaine[x*longueurItérationVigenère+y] = chaine[x*longueurItérationVigenère+y] - MotDePasse[y]
                # On décrypte chaque carractère selon Vigenère, en soustrayant les valeurs des caractères du mot de passe à ceux du message

            except IndexError:

                pass
                # Si on a fini de crypter tous les caractères mais que la boucle de cyptage continue
                # On ne fait rien

    résultat = TransformationCaractères(chaine)
    print(" ====> " + résultat)

    return résultat


def GénérationMotDePasseSécurisé(MotDePasse):

    motDePasseUser = hashlib.sha224(bytes(MotDePasse, "utf-8")).hexdigest()
    motDePasseConstant = hashlib.sha224(b"q55|R,~gS2.m)RD5d^5N8KcS6?v7Lhb<").hexdigest()
    # On hashe le mot de passe de l'utilisateur + un mot de passe constant pour obtenir un mot bien plus sécurisé

    motDePasseFinal = motDePasseUser + motDePasseConstant

    résultat = []

    for caractère in motDePasseFinal:
    # Pour chaque caratère du hash

        try:
        # On essaie de convertir en entier pour vérifier si le caractère est un chiffre
            caractère = int(caractère)

        except ValueError:
        # En cas d'erreur de valeur, c'est une lettre, on ne fait rien
            pass

        else:
        # On transforme en lettre le chiffre en ajoutant 100 pour éviter d'avoir les tabulations de la table ascii
            caractère = chr(caractère + 100)

        finally:
        # On finit par ajout le caractère, converti ou non au résultat
            résultat.append(caractère)

    return "".join(résultat)



def InitialisationSauvegarde(motDePasse):

    """ Qui créé un fichier de sauvegarde au bon emplacement """

    try :
            # On essaie de créer un dossier pour stocker les fichiers de sauvegardes
        os.makedirs("Messages sauvegardés")
    except FileExistsError :
        # Si le fichier existe déjà
        pass

    NomFichier = "Messages sauvegardés/" + time.strftime("%A-%d-%B-%H.%M.%S")+".KriptoFile"
    # On défini le nom du fichier avec le jour, la date, le mois et l'heure de début de la conversation

    DateDébutConversation = time.strftime("%A %d %B")
    HeureDébutConversation = time.strftime("%H:%M:%S")
    # On récupère l'heure et la date du début de la conversation

    Annonce = ChiffrementVignère(motDePasse, str(f"Début de la conversation le {DateDébutConversation} à {HeureDébutConversation}."))
    # On chiffre l'annonce du début du fichier

    fichier = open(NomFichier, "w")

    fichier.write(Annonce)
    fichier.write("\n")
    fichier.close()
    # On écrit l'annonce de façon chiffrée puis on saute une ligne

    return NomFichier


def NouvelleLigne(NomFichier, MotDePasse, chaine):

    """ Fichier qui ajoute une ligne chiffrée au fichier demandé """

    ChaineChiffré = ChiffrementVignère(MotDePasse, chaine)

    fichier = open(NomFichier, "a")

    fichier.write(ChaineChiffré)
    fichier.write("\n")
    fichier.close()
    # On ouvre le fichier de de sauvegarde, on écrit le message chiffré
    # Puis on retourne à ligne


def LectureSauvegarde(NomFichier, MotDePasse):


    """ Fonction qui lit, déchiffre et retourne sous forme de liste
    chaque ligne du fichier demandé """

    ListeLignes = []

    with open(NomFichier, "r") as fichier :

        for ligne in fichier :
            ListeLignes.append(ligne)

    fichier.close()

    for index in range(len(ListeLignes)):
    # Pour chaque ligne

        ListeLignes[index] = DéchiffrementVignère(MotDePasse, ListeLignes[index])
        # On déchiffre la ligne

        ListeLignes[index] = list(ListeLignes[index])
        ListeLignes[index].pop(-1)
        # On transforme la ligne en liste et on retire le derniere caratères "\U0010ffa2"

        ListeLignes[index] = "".join(ListeLignes[index])
        # On retransforme la ligne en texte

    return ListeLignes
