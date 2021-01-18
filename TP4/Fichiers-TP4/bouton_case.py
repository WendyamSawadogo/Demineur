"""
Module contenant la description de la classe BoutonCase, un bouton correspondant à une case du jeu Démineur
"""

from tkinter import Button

class BoutonCase(Button):
    """
    Bouton correspondant à une case du jeu Démineur
    """
    def __init__(self, parent, rangee_x, colonne_y):
        """
        Initialisation d'un bouton de case

        Args:
            parent : Statut du bouton
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        """
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        super().__init__(parent, text=' ', padx=1, pady=3, height=1, width=2)