# -*- coding: utf-8 -*-
"""
Module contenant la description de la classe Tableau. Un tableau est utilisé pour jouer une partie du jeu Démineur.

Auteurs: Simon Hardy, Pascal Germain
"""

from case import Case
from random import randint

class Tableau():
    """
    Tableau du jeu de démineur, implémentée avec un dictionnaire de cases.
    
    Warning:
        Si vous ajoutez des attributs à la classe Tableau, n'oubliez pas de les documenter ici.

    Attributes:
        dimension_rangee (int): Nombre de rangées du tableau
        dimension_colonne (int): Nombre de colonnes du tableau
        nombre_mines (int): Nombre de mines cachées dans le tableau

        nombre_cases_sans_mine_a_devoiler (int) : Nombre de cases sans mine qui n'ont pas encore été dévoilées
            Initialement, ce nombre est égal à dimension_rangee * dimension_colonne - nombre_mines

        dictionnaire_cases (dict): Un dictionnaire de case en suivant le format suivant:
            Les clés sont les positions du tableau sous la forme d'un tuple (x, y), 
                x étant le numéro de la rangée, y étant le numéro de la colonne.
            Les éléments sont des objets de la classe Case.
    """
    def __init__(self, dimension_rangee=5, dimension_colonne=5, nombre_mines=5):
        """ Initialisation d'un objet tableau.
        
        Attributes:
            dimension_rangee (int): Nombre de rangées du tableau (valeur par défaut: 5)
            dimension_colonne (int): Nombre de colonnes du tableau (valeur par défaut: 5)
            nombre_mines (int): Nombre de mines cachées dans le tableau (valeur par défaut: 5)
        """ 
    
        self.dimension_rangee = dimension_rangee
        self.dimension_colonne = dimension_colonne
        self.nombre_mines = nombre_mines

        # Le dictionnaire de case, vide au départ, qui est rempli par la fonction initialiser_tableau().
        self.dictionnaire_cases = {}

        self.initialiser_tableau()

        self.nombre_cases_sans_mine_a_devoiler = self.dimension_rangee * self.dimension_colonne - self.nombre_mines

    def valider_coordonnees(self, rangee_x, colonne_y):
        """
        Valide les coordonnées reçues en argument. Les coordonnées sont considérées valides si elles se trouvent bien
        dans les dimensions du tableau.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns:
            bool: True si les coordonnées (x, y) sont valides, False autrement
        """
        rangee_valide = rangee_x >= 1 and rangee_x <= self.dimension_rangee
        colonne_valide = colonne_y >= 1 and colonne_y <= self.dimension_colonne
        return rangee_valide and colonne_valide

    def obtenir_case(self, rangee_x, colonne_y):
        """
        Récupère une case à partir de ses numéros de ligne et de colonne
        
        Args:
            rangee_x (int) : Numéro de la rangée de la cas
            colonne_y (int): Numéro de la colonne de la case
        Returns:
            Case: Une référence vers la case obtenue
            (ou None si les cooordonnées ne sont pas valides)
        """
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return None
        
        coordonnees = (rangee_x, colonne_y)
        return self.dictionnaire_cases[coordonnees]

    def obtenir_voisins(self, rangee_x, colonne_y):
        """
        Retourne une liste de coordonnées correspondant aux cases voisines d'une case. Toutes les coordonnées retournées
        doivent être valides (c'est-à-dire se trouver à l'intérieur des dimensions du tableau).

        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut connaître les cases voisines
            colonne_y (int): Numéro de la colonne de la case dont on veut connaître les cases voisines

        Returns:
            list : Liste des coordonnées (tuple x, y) valides des cases voisines de la case dont les coordonnées
            sont reçues en argument
        """
        voisinage = ((-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1))

        liste_coordonnees_cases_voisines = []

        for voisin in voisinage:
            coord = (rangee_x + voisin[0], colonne_y + voisin[1])
            if self.valider_coordonnees(coord[0], coord[1]):
                liste_coordonnees_cases_voisines.append(coord)
                
        return liste_coordonnees_cases_voisines

    def initialiser_tableau(self):
        """
        Initialise le tableau à son contenu initial en suivant les étapes suivantes:
            1) On crée chacune des cases du tableau.
            2) On y ajoute ensuite les mines dans certaines cases qui sont choisies au hasard.
            3) À chaque fois qu'on ajoute une mine dans une case, vous devriez incrémenter dans chacune des cases
            voisines un attribut qui représentera le nombre de mines voisines pour ces cases.
        """
        for rangee_x in range(1, self.dimension_rangee+1):
            for colonne_y in range(1, self.dimension_colonne+1):
                coordonnees = (rangee_x, colonne_y)
                self.dictionnaire_cases[coordonnees] = Case()

        nb_mines_placees = 0

        while nb_mines_placees < self.nombre_mines:
            mine_x = randint(1, self.dimension_rangee)
            mine_y = randint(1, self.dimension_colonne)
            la_case = self.dictionnaire_cases[(mine_x, mine_y)]

            # Comme la position de la mine est aléatoire, il est possible que la case soit déjà minée.
            # Dans ce cas, on recommence!
            if not la_case.est_minee:
                la_case.ajouter_mine()
                nb_mines_placees += 1
                
                for coord_voisin in self.obtenir_voisins(mine_x, mine_y):
                    voisin = self.dictionnaire_cases[coord_voisin]
                    voisin.ajouter_une_mine_voisine()

    def valider_coordonnees_a_devoiler(self, rangee_x, colonne_y):
        """
        Valide que les coordonnées reçues en argument sont celles d'une case que l'on peut dévoiler 
        (donc que les coordonnées sont valides et que la case correspondante n'a pas encore été dévoilée).
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut valider les coordonnées
            colonne_y (int): Numéro de la colonne de la case dont on veut valider les coordonnées
        
        Returns
            bool: True si la case à ces coordonnées (x, y) peut être dévoilée, False autrement (donc si la
                  case a déjà été dévoilée ou que les coordonnées ne dont pas valides).
        """  
        if not self.valider_coordonnees(rangee_x, colonne_y):
            return False

        la_case = self.obtenir_case(rangee_x, colonne_y)
        return not la_case.est_devoilee
        
    def afficher_solution(self):
        """
        Méthode qui affiche la tableau solution à l'écran. La solution montre les mines pour les cases qui en contiennent
        et la valeur du nombre de mines voisines pour les autres cases.
        """
        print()
        for rangee_x in range(0, self.dimension_rangee+1):
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0:
                    car = '  |'
                elif rangee_x == 0:
                    car = str(colonne_y)
                elif colonne_y == 0:
                    car = str(rangee_x) + ' |'
                else:
                    case_xy = self.obtenir_case(rangee_x, colonne_y)   
                    if case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)
                    
                print(car, end=" ")
            
            print()
            if rangee_x == 0:
                print('--+-' + '--'*self.dimension_colonne)

    def afficher_tableau(self):
        """
        Méthode qui affiche le tableau à l'écran. Le tableau montre le contenu des cases dévoilées 
        (mine ou nombre de mines voisines) ou un point pour les cases non dévoilées.
        """
        print()
        for rangee_x in range(0, self.dimension_rangee+1):
            for colonne_y in range(0, self.dimension_colonne+1):
                if rangee_x == 0 and colonne_y == 0:
                    car = '  | '
                elif rangee_x == 0:
                    car = f'{colonne_y%10} '
                elif colonne_y == 0:
                    car = f'{rangee_x:<2}| '
                else:
                    case_xy = self.dictionnaire_cases[(rangee_x, colonne_y)]   
                    if not case_xy.est_devoilee: # Seule différence avec afficher_solution()
                        car = '.'
                    elif case_xy.est_minee:
                        car = 'M'
                    else:
                        car = str(case_xy.nombre_mines_voisines)
                    car += ' '
                 
                print(car, end="")
            
            print()
            if rangee_x == 0:
                print('--+-' + '--'*self.dimension_colonne)

    def contient_cases_a_devoiler(self):
        """
        Méthode qui indique si le tableau contient des cases à dévoiler.
        
        Returns:
            bool: True s'il reste des cases à dévoiler, False autrement.

        """
        return self.nombre_cases_sans_mine_a_devoiler > 0

    def devoiler_case(self, rangee_x, colonne_y):
        """
        Méthode qui dévoile le contenu de la case dont les coordonnées sont reçues en argument. Si la case ne
        contient pas de mine, on décrémente l'attribut qui représente le nombre de cases sans mine à dévoiler ; ensuite,
        on dévoile récursivement les voisins de la case qui ne sont pas voisins d'une mine. Parallèlement, la méthode
        retourne la liste des cases dévoilées lors du tour.
       
        Args:
            rangee_x (int) : Numéro de la rangée de la case à dévoiler
            colonne_y (int): Numéro de la colonne de la case à dévoiler

        Returns:
            liste_des_cases_a_devoiler (list) : Liste des cases dévoilées lors du tour
        """
        # On valide d'abord les coordonnées reçues en arguement.
        if self.valider_coordonnees_a_devoiler(rangee_x, colonne_y):

            case_xy = self.obtenir_case(rangee_x, colonne_y)
            case_xy.devoiler()
            liste_des_cases_a_devoiler = []

            # Si les coordonnées reçues en arguement correspondent à une case non-minée, on enchaine avec la
            # décrémentation l'attribut qui représente le nombre de cases sans mine à dévoiler et la concaténation des
            # coordonnées reçues en arguement à la liste des cases dévoilées lors du tour.
            if not case_xy.est_minee:
                self.nombre_cases_sans_mine_a_devoiler -= 1
                liste_des_cases_a_devoiler.append((rangee_x, colonne_y))

                # Si les coordonnées reçues en arguement correspondent à une case non-voisine d'une mine, on dévoile les
                # cases voisines récursivement jusqu'à ce qu'il ne reste que des cases voisines de mines à dévoiler lors
                # du présent tour.
                if not case_xy.est_voisine_d_une_mine():
                    voisins = self.obtenir_voisins(rangee_x, colonne_y)
                    for coord in voisins:
                        case_voisine = self.dictionnaire_cases[coord]
                        if not case_voisine.est_devoilee:
                            # La fonctionnalité récursive est implémentée ici.
                            voisins_a_devoiler = []
                            voisins_a_devoiler += self.devoiler_case(coord[0], coord[1])
                            for voisin in voisins_a_devoiler:
                                if not voisin in liste_des_cases_a_devoiler:
                                    liste_des_cases_a_devoiler.append(voisin)

            # On retourne la liste des cases dévoilées lors du tour.
            return liste_des_cases_a_devoiler
        
    def contient_mine(self, rangee_x, colonne_y):
        """
        Méthode qui vérifie si la case dont les coordonnées sont reçues en argument contient une mine.
        
        Args:
            rangee_x (int) : Numéro de la rangée de la case dont on veut vérifier si elle contient une mine
            colonne_y (int): Numéro de la colonne de la case dont on veut vérifier si elle contient une mine
        
        Returns:
            bool: True si la case à ces coordonnées (x, y) contient une mine, False autrement.
        """
        return self.obtenir_case(rangee_x, colonne_y).est_minee


#### Tests unitaires (à compléter) ###

def test_initialisation():
    tableau_test = Tableau()

    assert tableau_test.contient_cases_a_devoiler()
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == tableau_test.dimension_colonne * \
        tableau_test.dimension_rangee - tableau_test.nombre_mines


def test_valider_coordonnees():

    tableau_test = Tableau()
    dimension_x, dimension_y = tableau_test.dimension_rangee, tableau_test.dimension_colonne

    assert tableau_test.valider_coordonnees(dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x+1, dimension_y)
    assert not tableau_test.valider_coordonnees(dimension_x, dimension_y+1)
    assert not tableau_test.valider_coordonnees(-dimension_x, dimension_y)
    assert not tableau_test.valider_coordonnees(0, 0)


def test_obtenir_voisins():
    tableau_test = Tableau(9, 3)
    solution_obtenue = tableau_test.obtenir_voisins(9,3)
    solution_attendue = [(8, 2), (8, 3), (9, 2)]

    assert len(solution_obtenue) == len(solution_attendue)
    for coordonnee in solution_attendue:
        assert coordonnee in solution_obtenue

    solution_obtenue = tableau_test.obtenir_voisins(1, 2)
    solution_attendue = [(1, 1), (1, 3), (2, 1), (2, 2), (2, 3)]

    assert len(solution_obtenue) == len(solution_attendue)
    for coordonnee in solution_attendue:
        assert coordonnee in solution_obtenue


def test_valider_coordonnees_a_devoiler():
    tableau_test = Tableau(3, 4)
    tableau_test.dictionnaire_cases[(1,1)].devoiler()
    tableau_test.dictionnaire_cases[(2,3)].devoiler()

    for i in range(-1, 8):
        for j in range(-1, 8):
            valide = i >= 1 and i <= 3 and j >= 1 and j <= 4
            valide = valide and (i,j) not in [(1,1), (2,3)]
            assert tableau_test.valider_coordonnees_a_devoiler(i, j) == valide



def test_devoiler_case():
    tableau_test = Tableau(5, 5, 1)
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == 24

    for i in range(1,5):
        for j in range(1,5):
            case_ij = tableau_test.obtenir_case(i, j)
            case_ij.est_minee = False
            case_ij.nombre_mines_voisines = 0
            if (i,j) == (1,1):
                case_ij.est_minee = True
            elif i <= 2 and j <= 2:
                case_ij.nombre_mines_voisines = 1

    tableau_test.devoiler_case(1,2)
    assert tableau_test.nombre_cases_sans_mine_a_devoiler == 23
    assert tableau_test.obtenir_case(1,2).est_devoilee

    tableau_test.devoiler_case(3, 1)
    assert tableau_test.nombre_cases_sans_mine_a_devoiler < 23
    for i in range(2,5):
        for j in range(1,3):
            assert tableau_test.obtenir_case(i, j).est_devoilee


def test_case_contient_mine():
    tableau_test = Tableau(5, 5, 5)

    compteur = 0
    for i in range(1,6):
        for j in range(1, 6):
            if tableau_test.dictionnaire_cases[(i,j)].est_minee:
                assert tableau_test.contient_mine(i,j)
                compteur += 1
            else:
                assert not tableau_test.contient_mine(i,j)

    assert compteur == 5


if __name__ == '__main__':

    print('Tests unitaires...')
    test_initialisation()
    test_valider_coordonnees()
    test_obtenir_voisins()
    test_valider_coordonnees_a_devoiler()
    test_devoiler_case()
    test_case_contient_mine()
    print('Tests réussis!')