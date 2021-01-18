"""
Module contenant la description de la classe InterfacePartie, l'interface du jeu Démineur. C'est à travers cette
interface que se déroule la partie de Démineur et toutes ses fonctionnalités.
"""
import tkinter
from tkinter import Tk, Frame, Button, messagebox, simpledialog, filedialog, Label
from tableau import Tableau
from bouton_case import BoutonCase
from case import Case
import configparser


class InterfacePartie(Tk):
    """
    L'interface du jeu Démineur
    """
    def __init__(self):
        """
        Initialisation de la classe avec des valeurs par défaut
        """
        # Appel de la classe parent
        super().__init__()


        # Nom de la fenêtre
        self.title("Démineur")


        # Instantiation d'un tableau
        self.tableau_mines = Tableau()


        #Instantiation du frame
        bouton_frame = Frame(self)
        bouton_frame.grid()

        #chrono = Chronometre(bouton_frame)

        bouton_nouvelle_partie = Button(bouton_frame, text='Nouvelle partie', command=self.nouvelle_partie)
        bouton_nouvelle_partie.grid(row=0, column=0)

        bouton_quitter = Button(bouton_frame, text="Quitter", command=self.quitter_partie)
        bouton_quitter.grid(row=0, column=1)

        bouton_sauvegarder_partie = Button(bouton_frame, text="Sauvegarder partie", command=self.sauvegarder_partie)
        bouton_sauvegarder_partie.grid(row=1, column=0)

        bouton_charger_partie = Button(bouton_frame, text="Charger partie", command=self.charger_partie)
        bouton_charger_partie.grid(row=1, column=1)

        bouton_taille_damier = Button(bouton_frame, text="Sélection taille damier", command=self.taille_damier)
        bouton_taille_damier.grid(row=2, column=0)

        bouton_instruction = Button(bouton_frame, text="Instructions", command=self.afficher_instructions)
        bouton_instruction.grid(row=2, column=1)

        self.compteur_de_tours = 1
        self.label_compteur_de_tours = Label(bouton_frame, text="Tour n°"+str(self.compteur_de_tours))
        self.label_compteur_de_tours.grid(row=3, column=0)


        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        # Instantiation des boutons du damier de jeu
        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i+1, j+1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<Button-3>', self.placer_drapeau)
                self.dictionnaire_boutons[(i+1, j+1)] = bouton

    def quitter_partie(self):

        if messagebox.askyesno('Quitter la partie', 'voulez-vous vraiment quitter le jeu ?'):
            self.quit()

    def devoiler_solution(self, event):
        """
        Methode permettant de devoiler toutes les cases du tableau

        Args:
            event : Évènement à l'origine du lancement de la fonction (<Button-1>)
        """

        for bouton in self.dictionnaire_boutons.values():

            case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)

            if case.est_minee:
                bouton['text'] = "💣"


            else:
                bouton['text'] = case.nombre_mines_voisines

    def devoiler_case(self, event):
        """
        TODO
        Méthode qui dévoile le contenu de la case dans l'interface

        Args:
            event : Évènement à l'origine du lancement de la fonction (<Button-1>)
        """

        # On identifie le bouton de case cliqué et la case correspondante.
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)

        # On vérifie que la case n'est pas marquée d'un drapeau.
        if not bouton['text'] == '⛳':

            # On dévoile toutes les cases à dévoiler pour le tour avec la fonction devoiler_case de tableau.py et on
            # récupère la liste des cases dévoilées lors du tour.
            liste_des_cases_a_devoiler = self.tableau_mines.devoiler_case(bouton.rangee_x, bouton.colonne_y)

            # Si la case est minée, on affiche la solution et le message de défaite.
            if case.est_minee:
                self.devoiler_solution(event)
                afficher = "Perdu !"
                messagebox.showinfo(message=afficher)


            # Sinon, on affiche le nombre de mines voisines au bouton pour tous les boutons à dévoiler lors du tour.
            else:
                for case_a_devoiler in liste_des_cases_a_devoiler:
                    bouton = self.dictionnaire_boutons[(case_a_devoiler[0], case_a_devoiler[1])]
                    case = self.tableau_mines.obtenir_case(case_a_devoiler[0], case_a_devoiler[1])
                    bouton['text'] = case.nombre_mines_voisines

                    # Si toutes les cases ont été dévoilées, on affiche la solution et le message de victoire.
                    if self.tableau_mines.nombre_cases_sans_mine_a_devoiler == 0:
                        self.devoiler_solution(event)
                        afficher = "Félicitation ! vous avez remporté la partie"
                        messagebox.showinfo(message=afficher)

            self.compteur_de_tours += 1
            self.label_compteur_de_tours['text'] = "Tour n°"+str(self.compteur_de_tours)

    def sauvegarder_partie(self):
        """
            Methode permettant de sauvegarder la partie en cours
        """
        # On crée le fichier de sauvegarde.
        sauvegarde = filedialog.asksaveasfile(initialdir="/",
                                               title="Entrez le nom du fichier de sauvegarde",
                                               filetypes=(("fichier texte", "*.txt"), ("tous les fichiers", "*.*")))

        # On y enregistre les données de la partie.
        sauvegarde.write(str(self.tableau_mines.dimension_rangee) + '\n')
        sauvegarde.write(str(self.tableau_mines.dimension_colonne) + '\n')
        sauvegarde.write(str(self.tableau_mines.nombre_mines) + '\n')
        sauvegarde.write(str(self.compteur_de_tours))

        for bouton in self.dictionnaire_boutons:
            texte_du_bouton = self.dictionnaire_boutons[bouton]['text']
            case = self.tableau_mines.obtenir_case(bouton[0], bouton[1])

            if case.est_minee:
                sauvegarde.write('\nM')
            else:
                sauvegarde.write('\n' + str(case.nombre_mines_voisines))

            if case.est_devoilee:
                sauvegarde.write('D')
            elif texte_du_bouton == '⛳':
                sauvegarde.write('F')
            else:
                sauvegarde.write('?')

        # On ferme le fichier.
        sauvegarde.close()

    def placer_drapeau(self, event):
        """
        Méthode permettant de placer ou retirer un drapeau sur une case avec un clic droit de souris. Une case marquée
        d'un drapeau ne peut être dévoilée."""
        bouton = event.widget
        case = self.tableau_mines.obtenir_case(bouton.rangee_x, bouton.colonne_y)

        if not case.est_devoilee:
            if bouton['text'] == ' ':
                bouton['text'] = '⛳'


            elif bouton['text'] == '⛳':
                bouton['text'] = ' '

    # ajouté par raouf a 9h41
    def charger_partie(self):
        """
            Methode permettant de charger la partie sauvegardée precédemment
        """
        # On ouvre le fichier à charger.
        chargement = filedialog.askopenfile(initialdir="/",
                                               title="Entrez le nom du fichier de sauvegarde",
                                               filetypes=(("fichier texte", "*.txt"), ("tous les fichiers", "*.*")))

        # On lit le fichier, puis on le ferme.
        partie = chargement.readlines()
        chargement.close()

        # Les variables suivantes serviront à récupérer les données de la partie à charger.
        dimensions_rangees = int(partie[0])
        dimensions_colonnes = int(partie[1])
        nombres_mines = int(partie[2])
        dictionnaire_cases = {}
        nombre_cases_sans_mines_a_devoiler = dimensions_rangees * dimensions_colonnes - nombres_mines
        no_tour = int(partie[3])
        donnees_des_cases = partie[4:]

        # On construit dictionnaire_cases avec les données récupérées.
        for x in range(1, dimensions_rangees + 1):
            for y in range(1, dimensions_colonnes + 1):
                ligne = donnees_des_cases[dimensions_rangees * (x - 1) + y - 1]
                dictionnaire_cases[(x, y)] = Case()
                # On vérifie si la case est minée.
                if 'M' in ligne:
                    dictionnaire_cases[(x, y)].est_minee = True
                else:
                    dictionnaire_cases[(x, y)].nombre_mines_voisines = int(ligne[0])
                # On vérifie si la case est dévoilée ou marquée d'un drapeau.
                if 'D' in ligne:
                    dictionnaire_cases[(x, y)].est_devoilee = True
                    nombre_cases_sans_mines_a_devoiler -= 1
                else:
                    if 'F' in ligne:
                        dictionnaire_cases[(x, y)].est_marquee_d_un_drapeau = True # voir les modifications apportées à case.py
                #  On assigne le nombre de mines voisines à la case.

        # On instancie le tableau.
        self.tableau_mines = Tableau(dimensions_rangees, dimensions_colonnes, nombres_mines)
        self.tableau_mines.dictionnaire_cases = dictionnaire_cases
        self.tableau_mines.nombre_cases_sans_mine_a_devoiler = nombre_cases_sans_mines_a_devoiler

        # On construit le damier.
        self.compteur_de_tours = no_tour
        self.label_compteur_de_tours['text'] = "Tour n°" + str(self.compteur_de_tours)

        self.cadre.grid_forget()

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<Button-3>', self.placer_drapeau)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton
                # On finit par afficher les cases dévoilées ou marquées d'un drapeau.
                case = self.tableau_mines.obtenir_case(i + 1, j + 1)
                if case.est_devoilee:
                    if case.est_minee:
                        bouton['text'] = '💣'
                    else:
                        bouton['text'] = case.nombre_mines_voisines
                elif case.est_marquee_d_un_drapeau:
                    bouton['text'] = '⛳'

    def nouvelle_partie(self):
        """
        Méthode qui réinitialise l'interface pour recommencer une partie
         """
        self.tableau_mines = Tableau()

        for bouton in self.dictionnaire_boutons.values():
            bouton['text'] = " "

        self.compteur_de_tours = 1
        self.label_compteur_de_tours['text'] = "Tour n°" + str(self.compteur_de_tours)

    def taille_damier(self):
        """
        Méthode permettant de choisir la taille du damier et le nombre de mines
        """
        # On demande au joueur d'entrer les données nécessaires.
        r = simpledialog.askinteger("taille du damier", "nombre de lignes?")
        c = simpledialog.askinteger("taille du damier", "nombre de colonne?")
        m = simpledialog.askinteger("taille du damier", "nombre de mines?")
        while m > r * c:
            m = simpledialog.askinteger("taille du damier", "Le nombre de mine maximal possible " + str(
                r * c) + "\n Entrez nombre de mines")

        # On instancie le nouveau damier.
        self.tableau_mines.dimension_rangee = r
        self.tableau_mines.dimension_colonne = c
        self.tableau_mines.nombre_mines = m
        self.tableau_mines = Tableau(r, c, m)

        self.compteur_de_tours = 1
        self.label_compteur_de_tours['text'] = "Tour n°" + str(self.compteur_de_tours)

        self.cadre.grid_forget()

        self.cadre = Frame(self)
        self.cadre.grid(padx=10, pady=10)

        self.dictionnaire_boutons = {}

        for i in range(self.tableau_mines.dimension_rangee):
            for j in range(self.tableau_mines.dimension_colonne):
                bouton = BoutonCase(self.cadre, i + 1, j + 1)
                bouton.grid(row=i, column=j)
                bouton.bind('<ButtonRelease-1>', self.devoiler_case)
                bouton.bind('<Button-3>', self.placer_drapeau)
                self.dictionnaire_boutons[(i + 1, j + 1)] = bouton

    def afficher_instructions(self):
        """Methode permettant d'afficher les instructions du jeu

        """
        # liste des instructions a afficher
        afficher_1 = "Voici les instructions :\n" \
                     " -Le but du jeu est de déminer les cases sans tomber sur une mine.\n" \
                     " -Dévoilez une case avec le clic gauche de la souris.\n"
        afficher_2 = "\n -Placez un drapeau sur une mine avec le clic droit.\n" \
                     " -La partie est perdue lorsque vous dévoilez une mine.\n" \
                     " -La solution est annoncée lorsque la partie est perdu.\n"
        afficher_3 = "\n  -La partie est gagnée lorsque vous trouvez toutes les mines.\n" \
                     " -Le chronomètre commence dès que vous commencez la partie.\n" \
                     " -Pour quitter la partie, appuyez sur le boutton 'Quitter'.\n "
        afficher_4 = "\n -Vous pouvez définir la taille du damier en utilisant le boutton 'Sélection taille damier'.\n "

        # affichage de ces instructions
        messagebox.showinfo(title="✨✨Instructions du PyMineur✨✨",
                            message=afficher_1 + afficher_2 + afficher_3 + afficher_4)