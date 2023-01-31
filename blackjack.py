from random import *

# Constructeur de la classe joueur
# Le joueur est déterminée par une instance de cette classe
# Le croupier est simplement un joueur un peu spécial (+ Attribut ValeurApresLaquelleOnNePiochePlus)
class Joueur():
    def __init__(self):
        self.cartes = [] # Les cartes piochées au fur et à mesure
        self.nom = "" 
        self.valeurApresLaquelleOnNePiochePlus = 0 #le nom est un peu long XD
        self.montantJouable = 0

    def ajouterCarte(self,carte):
        """Ajoute une carte à la main du joueur"""
        self.cartes.append(carte)

    def getCartes(self):
        """Renvoie la liste des cartes présentes dans la main de joueur"""
        return self.cartes

    def setNom(self, nom = ""):
        """Modifie le nom de l'instance"""
        if nom != "": 
            self.nom = nom
        else : 
            self.nom = str(input("Quel est votre nom ? : "))

    def getNom(self):
        """Renvoie le nom de l'instance"""
        return self.nom

    def setValeurApresLaquelleOnNePiochePlus(self, entier):
        """Uniquement utilisé par le croupier et par les bots
        Etablie une valeur telle que lorsque la somme des cartes de la main du joueur dépassent cette valeur,
        le bot arrête de piocher"""
        self.valeurApresLaquelleOnNePiochePlus = entier

    def getValeurApresLaquelleOnNePiochePlus(self):
        """Renvoie la valeur définie juste au dessus"""
        return self.valeurApresLaquelleOnNePiochePlus

    def getMontantJouable(self):
        """Le montant jouable correpond a l'argent sur le compte du joueur"""
        return self.montantJouable
    
    def setMontantJouable(self, valeur):
        """Modifie la valeur du montant jouable"""
        self.montantJouable = valeur

    def soustraireMontantJouable(self,valeur):
        """Soustrait une valeur donnée au montant jouable
        Cette soustraction est effectuée lors du pari"""
        self.montantJouable -= valeur

    def ajouterMontantJouable(self,valeur):
        """Ajoute une valeur donnée au montant jouable"""
        self.montantJouable += valeur

    def getSommeCartes(self):
        """Renvoie la somme des cartesprésentes dans la main du joueur
        A savoir que Vallet,Dame,Roi et As valent 10
        L'As peut aussi valoir seulement 1 si et seulement si la somme dépasse 21"""
        somme = 0
        quantiteAs = 0
        for carte in self.cartes :
            try : 
                somme += int(carte[:-1])
            except :
                if carte[:-1] == "A":
                    quantiteAs += 1
                    somme += 11
                else :
                    somme += 10
        while somme > 21 and quantiteAs > 0 :
            somme -= 9
            quantiteAs -= 1
        return somme
    
    def resetMain(self):
        """Supprime toutes les cartes de la main du joueur"""
        self.cartes = []

    def afficherLaMain(self):
        """Tout est dans le nom"""
        if self.getNom() == "Croupier":
            print("\t\tMain du croupier : ")
        else :
            print(f"\t\tMain de {self.getNom()} :")
        print(f"\t\t", end="   ")
        for carte in self.cartes : 
            print(carte, end = " ")
        print("(" + str(self.getSommeCartes()) + ")")

# Constructeur du jeu en lui même
class BlackJack():
    def __init__(self):
        self.cartesRestantes = [] # le paquet de carte
        self.sommeMaximalePossible = 21 # La somme à ne pas dépasser
        self.resetJeu() # Paquet de carte neuf

    def piocher(self):
        """Renvoie une carte au hasard dans le paquet de jeu et la supprime de celui-ci"""
        cartePioche = choice(self.cartesRestantes)
        self.cartesRestantes.remove(cartePioche)
        return cartePioche

    def resetJeu(self):
        """Le paquet de jeu redevient tout neuf"""
        self.cartesRestantes = ['2♥', '2♦', '2♣', '2♠', '3♥', '3♦', '3♣', '3♠', '4♥', '4♦', '4♣', '4♠', '5♥', '5♦', '5♣', '5♠', '6♥', '6♦', '6♣', '6♠', '7♥', '7♦', '7♣', '7♠', '8♥', '8♦', '8♣', '8♠', '9♥', '9♦', '9♣', '9♠', '10♥', '10♦', '10♣', '10♠', 'V♥', 'V♦', 'V♣', 'V♠', 'D♥', 'D♦', 'D♣', 'D♠', 'R♥', 'R♦', 'R♣', 'R♠', 'A♥', 'A♦', 'A♣', 'A♠']

    def enleverCarte(self,carte):
        """Enleve la carte passée en parametre du paquet"""
        try : 
            self.cartesRestantes.remove(carte)
        except:
            pass

    def tour(self, croupier, joueur, montantParie):
        """Implémente un tour de jeu"""
        # Creation des variables et affichage de départ
        # Debut du jeu
        # Le croupier pioche toujours une carte en premier
        self.resetJeu()
        croupier.ajouterCarte(self.piocher())
        croupier.afficherLaMain()
        # Ensuite c'est au tour du joueur
        joueur.ajouterCarte(self.piocher())
        joueur.ajouterCarte(self.piocher())
        joueur.afficherLaMain()
        
        # On demande au joueur s'il veut continuer de piocher ou arreter
        jeuTermine = False 
        while not jeuTermine : 
            STR_INPUT_PIOCHE_STOP = "\tChoix du joueur : (1:pioche | 2:stop) :"
            volonteDuJoueur = input(STR_INPUT_PIOCHE_STOP)
            while volonteDuJoueur not in ["1","2"]:
                print("Erreur, veuillez retaper : ")
                volonteDuJoueur = input(STR_INPUT_PIOCHE_STOP)
            # Cas où il souhaite arreter
            if volonteDuJoueur == "2" :
                break
            # Cas où il souhaite piocher
            elif volonteDuJoueur == "1" : 
                joueur.ajouterCarte(self.piocher())
                joueur.afficherLaMain()
            # A la fin de chaque tour on vérifie que la somme des cartes n'a pas dépassée le maximum
            if joueur.getSommeCartes() > self.sommeMaximalePossible : 
                print("\tTOUR PERDU")
                return 0
            if joueur.getSommeCartes() == 21:
                print("\tBLACKJACK !!")
                break
        if joueur.getSommeCartes() <= self.sommeMaximalePossible :
            while croupier.getSommeCartes() < croupier.getValeurApresLaquelleOnNePiochePlus():
                croupier.ajouterCarte(self.piocher()) 
                croupier.afficherLaMain()
            if croupier.getSommeCartes() > self.sommeMaximalePossible :
                print("\tTOUR GAGNE")
                return montantParie*2
            elif croupier.getSommeCartes() > joueur.getSommeCartes():
                print("\tTOUR PERDU")
                return 0
            elif croupier.getSommeCartes() == joueur.getSommeCartes():
                print("\tEGALITE")
                return montantParie
            elif croupier.getSommeCartes() < joueur.getSommeCartes():
                print("\tTOUR GAGNE")
                return 2*montantParie
            print("ERREUR TOUR()")
            return 0
        

    def jouer(self):
        """Implémente une partie complète du jeu jusqu'à ce que le compte soit vide ou que le joueur veuille arreter"""
        croupier = Joueur()
        croupier.setNom("Croupier")
        croupier.setValeurApresLaquelleOnNePiochePlus(17)
        joueur = Joueur()
        joueur.setNom()

        # Definition du montant jouable
        AFFICHAGE_INPUT_MONTANT_JOUABLE = "Entrez le montant maximal que vous pourrez jouer (en €) : "
        montantJouable = input(AFFICHAGE_INPUT_MONTANT_JOUABLE)
        try :
            montantJouable = int(montantJouable)
        except:
            pass
        while type(montantJouable) != int or montantJouable <= 0:
            print("Erreur, Veuillez ressaisir")
            montantJouable = input(AFFICHAGE_INPUT_MONTANT_JOUABLE)
            try :
                montantJouable = int(montantJouable)
            except :
                pass
        joueur.setMontantJouable(montantJouable)

        # Lancement du corps du jeu
        partieEnCours = "O"
        while partieEnCours.upper() == "O":
            print()
            print("***")
            self.resetJeu()
            croupier.resetMain()
            joueur.resetMain()
            AFFICHAGE_INPUT_MONTANT_PARI = "\tRentrez le montant que vous voulez parier (somme maximal : " + str(joueur.getMontantJouable())+ ") : "

            montantParie = input(AFFICHAGE_INPUT_MONTANT_PARI)
            try :
                montantParie = int(montantParie)
            except:
                pass

            while type(montantParie) !=  int or  montantParie <= 0 or montantParie > joueur.getMontantJouable():
                print("\tErreur, veuillez ressaisir")
                montantParie = input(AFFICHAGE_INPUT_MONTANT_PARI)
                try :
                    montantParie = int(montantParie)
                except:
                    pass

            # lancement de la partie
            joueur.soustraireMontantJouable(montantParie)
            resultatDuTour = self.tour(croupier, joueur, montantParie)
            joueur.ajouterMontantJouable(resultatDuTour)
            print()
            print(f"NOUVEAU SOLDE : {joueur.getMontantJouable()}€")
            if joueur.getMontantJouable() == 0:
                print(f"PLUS AUCUN MONTANT JOUABLE : Arrêt de la partie")
                return
            # Demande si le joueur souhaite continuer
            AFFICHAGE_INPUT_CONTINUER_PARTIE = "\tSouhaitez vous continuer ? (o/n) : "
            partieEnCours = input(AFFICHAGE_INPUT_CONTINUER_PARTIE)
            while partieEnCours.upper() not in ["O","N",""]:
                print(f"\tErreur, veuillez ressaisir")
                partieEnCours = input(AFFICHAGE_INPUT_CONTINUER_PARTIE)
            if partieEnCours == "":
                partieEnCours = "O"


    def tourIAcontreIANaive(self, croupier, bot, montantParie):
        croupier.ajouterCarte(self.piocher())
        while bot.getSommeCartes() < bot.getValeurApresLaquelleOnNePiochePlus():
            bot.ajouterCarte(self.piocher())
        while croupier.getSommeCartes() < croupier.getValeurApresLaquelleOnNePiochePlus():
            croupier.ajouterCarte(self.piocher())
        if bot.getSommeCartes() > 21 : 
            return 0
        elif croupier.getSommeCartes() > 21 :
            return 2*montantParie
        elif croupier.getSommeCartes() == bot.getSommeCartes():
            return montantParie
        elif croupier.getSommeCartes() > bot.getSommeCartes():
            return 0
        elif croupier.getSommeCartes() < bot.getSommeCartes():
            return 2*montantParie

    def etudeStrategieUneValeurMaxNaive(self,aPartirDeCeNombreOnArreteDePiocher):
        pourcentages = {"P":0,"E":0,"G":0}
        croupier = Joueur()
        croupier.setNom("Croupier")
        croupier.setValeurApresLaquelleOnNePiochePlus(17)

        bot = Joueur()
        bot.setNom("Bot")
        bot.setValeurApresLaquelleOnNePiochePlus(aPartirDeCeNombreOnArreteDePiocher) # Oui oui il y a seulement deux appels
        bot.setMontantJouable(1000000)

        for k in range(1000000):
            self.resetJeu()
            bot.resetMain()
            croupier.resetMain()
            montantParie = 1
            bot.soustraireMontantJouable(montantParie)
            resultatDuTour = self.tourIAcontreIANaive(croupier, bot, montantParie)
            if resultatDuTour == 0 :
                pourcentages["P"] += 1
            elif resultatDuTour == montantParie :
                pourcentages["E"] += 1
            else : 
                pourcentages["G"] += 1
            bot.ajouterMontantJouable(resultatDuTour)
        print(f"Somme à la fin : {bot.getMontantJouable()}")
        return pourcentages

    def etudeStrategieNaive(self):
        print("Le croupier s'arrête de piocher quand il a au moins 17 points")
        for valeurMax in range(4,21):
            print(f"On s'arrete de piocher lorsqu'on a au moins {valeurMax} points")
            print(self.etudeStrategieUneValeurMaxNaive(valeurMax))

    def tourIAcontreIAPremiereCarteDefinie(self, croupier, bot, premiereCarte, montantParie):
        croupier.ajouterCarte(premiereCarte)
        self.enleverCarte(premiereCarte)
        while bot.getSommeCartes() < bot.getValeurApresLaquelleOnNePiochePlus():
            bot.ajouterCarte(self.piocher())
        while croupier.getSommeCartes() < croupier.getValeurApresLaquelleOnNePiochePlus():
            croupier.ajouterCarte(self.piocher())
        if bot.getSommeCartes() > 21 : 
            return 0
        elif croupier.getSommeCartes() > 21 :
            return 2*montantParie
        elif croupier.getSommeCartes() == bot.getSommeCartes():
            return montantParie
        elif croupier.getSommeCartes() > bot.getSommeCartes():
            return 0
        elif croupier.getSommeCartes() < bot.getSommeCartes():
            return 2*montantParie

    def etudeStrategieUneValeurMaxEtPremiereCarteConnue(self, carteDepart, aPartirDeCeNombreOnArreteDePiocher):
        pourcentages = {"P":0,"E":0,"G":0}
        croupier = Joueur()
        croupier.setNom("Croupier")
        croupier.setValeurApresLaquelleOnNePiochePlus(17)

        bot = Joueur()
        bot.setNom("Bot")
        bot.setValeurApresLaquelleOnNePiochePlus(aPartirDeCeNombreOnArreteDePiocher) # Oui oui il y a seulement deux appels
        bot.setMontantJouable(100000)

        for k in range(100000):
            self.resetJeu()
            bot.resetMain()
            croupier.resetMain()
            montantParie = 1
            bot.soustraireMontantJouable(montantParie)
            resultatDuTour = self.tourIAcontreIAPremiereCarteDefinie(croupier, bot, carteDepart, montantParie)
            if resultatDuTour == 0 :
                pourcentages["P"] += 1
            elif resultatDuTour == montantParie :
                pourcentages["E"] += 1
            else : 
                pourcentages["G"] += 1
            bot.ajouterMontantJouable(resultatDuTour)
        return pourcentages

    def etudeStrategiePremiereCarteConnue(self):
        for carte in ['2♥', '3♥', '4♥',  '5♥',  '6♥', '7♥', '8♥','9♥', '10♥', 'V♥', 'D♥', 'R♥', 'A♥']:
            print(carte)
            for valeurMax in range(4,21):
                x = self.etudeStrategieUneValeurMaxEtPremiereCarteConnue(carte,valeurMax)
                print(f'{x["P"]},{x["E"]},{x["G"]}')




if __name__ == '__main__':
    b = BlackJack()
    b.jouer()
