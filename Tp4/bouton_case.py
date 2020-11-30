"""
TODO: Ajoutez les docstrings et modifier le code au besoin.
"""

from tkinter import Button

class BoutonCase(Button):
    """un boutton permettant d'interagir avec la case du damier

        """

    def __init__(self, parent, rangee_x, colonne_y):
        self.rangee_x = rangee_x
        self.colonne_y = colonne_y
        super().__init__(parent, text=' ', padx=1, pady=3, height=1, width=2)
