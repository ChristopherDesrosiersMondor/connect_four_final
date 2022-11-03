from random import randint
from math import inf


class Node:
    """Definit un node utilisé avec la theorie des graphes pour garder le board state du jeu"""
    def __init__(self) -> None:
        self.valeur = ""
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.up_right = None
        self.up_left = None
        self.down_right = None
        self.down_left = None
    
    def directions(self):
        """Retourne un dictionnaire avec ses voisins selon les directions suivantes:
        
           up
           down
           left
           right
           up_right
           up_left
           down_right
           down_left
        """
        return {
            "up": self.up,
            "down" : self.down,
            "left" : self.left,
            "right" : self.right,
            "up_right": self.up_right,
            "up_left": self.up_left,
            "down_right": self.down_right,
            "down_left": self.down_left
            }
    
    def __repr__(self) -> str:
        return self.valeur

    def __str__(self) -> str:
        return f"[{self.valeur:1}]"


class TNode:
    tree_rep = ""
    id = 0
    """Definit un node d'un arbre l'arborescence"""
    def __init__(self, parent: 'TNode', data: object) -> None:
        self.parent = parent
        self.data = data
        self.board = data[0]
        self.value = data[1]
        self.colonne = data[2]
        self.enfants = []
        TNode.id += 1
        self.id = TNode.id

    def path_value(self, h: int) -> int:
        """Calculer la valeur d'un chemin de la feuille a la racine"""
        node = self
        value = 0
        for i in range(h):
            value = self.data[1] + value
            node = self.parent
        return value

    @staticmethod
    def last(node: 'TNode') -> bool:
        """Methode pour verifier qu'un node est une leaves ou non"""
        if not node.enfants:
            return True
        return False

    """On fait la surcharge de get et lt pour pouvoir appeler max sur une liste de node"""
    def __gt__(self, otherTNode: 'TNode') -> bool:
        if self.data[1] < otherTNode.data[1]:
            return False
        
        return True

    def __lt__(self, otherTNode: 'TNode') -> bool:
        if self.data[1] > otherTNode.data[1]:
            return False
        
        return True

    def __repr__(self) -> str:
        return f"v: {self.value} id: {self.id}"

    def __str__(self) -> str:
        return str(self.data[1])


class Board:
    """Definit un board de puissance 4"""
    def __init__(self, lignes: int, colonnes: int) -> None:
        """Complexite: n^2"""
        self.rangees = lignes
        self.colonnes = colonnes
        self.nodes_to_value = []
        self.matrice_jeu = [[Node() for colonne in range(colonnes)] for rangee in range(lignes)]
        self.node_voisinage()
    
    def __str__(self) -> str:
        mat_string = ""
        for i in range(self.colonnes):
            mat_string += f"{(i+1):^3}"
        mat_string += "\n"
        for rangee in self.matrice_jeu:
            for node in rangee:
                mat_string += f"{str(node)}" 
            mat_string += "\n"
        return mat_string

    def __repr__(self) -> str:
        mat_string = ""
        for node in self.matrice_jeu[5]:
            mat_string += f"{str(node)}"
        return mat_string

    def fill(self, matrice: list):
        """Remplir les nodes du board avec les valeurs d'une matrice"""
        for i in range(len(matrice)):
            for j in range(len(matrice[0])):
                self.matrice_jeu[i][j].valeur = matrice[i][j]
                if self.matrice_jeu[i][j].valeur != '':
                    self.nodes_to_value.append(self.matrice_jeu[i][j])

    # optimisation possible: non-identifiee
    def board_to_matrice(self) -> list:
        """Utiliser le board pour generer une matrice de valeur qui le represente
           Complexite: n^2
        """
        matrice = [['' for colonne in range(self.colonnes)] for rangee in range(self.rangees)]
        for i, rangee in enumerate(self.matrice_jeu):
            for j, node in enumerate(rangee):
                matrice[i][j] = node.valeur
        return matrice
    
    def unfill(self) -> None:
        """Complexite: n^2"""
        for rangee in self.matrice_jeu:
            for node in rangee:
                node.valeur = ''
        self.nodes_to_value = []


    def node_voisinage(self) -> None:
        """Réseau voisinage: s'assurer que toutes les nodes connaissent leurs voisins
           complexite n^2
        """
        """
        Source: https://stackoverflow.com/questions/7872838/one-line-if-condition-assignment
        User Frost
        Use: one line asignment if else
        """
        matrice_jeu = self.matrice_jeu
        for R, rangee in enumerate(self.matrice_jeu):
            for C, node in enumerate(rangee):

                # Si la rangee depasse le nombre de rangees --> fin du tableau
                r_in_range = R + 1 <= self.rangees - 1

                # Si la colonne depasse le nombre de colonnes --> fin du tableau
                c_in_range = C + 1 <= self.colonnes - 1

                # Si Rangee est negatif --> fin du tableau
                r_positive = R - 1 >= 0

                # Si Colonne est negatif --> fin du tableau
                c_positive = C - 1 >= 0

                # on définit la position de chacun de ses voisins pour chaque node
                node.up = matrice_jeu[R-1][C] if r_positive else None
                node.down = matrice_jeu[R+1][C] if r_in_range else None
                node.right = matrice_jeu[R][C+1] if c_in_range else None
                node.left = matrice_jeu[R][C-1] if c_positive else None
                node.up_right = matrice_jeu[R-1][C+1] if c_in_range and r_positive else None
                node.up_left = matrice_jeu[R-1][C-1] if r_positive and c_positive else None
                node.down_right = matrice_jeu[R+1][C+1] if r_in_range and c_in_range else None
                node.down_left = matrice_jeu[R+1][C-1] if r_in_range and c_positive else None


    def first_empty_node(self, colonne: int) -> Node:
        """Trouve la première case vide dans une colonne
           Complexite: n
        """
        current_rangee = self.rangees - 1
        colonne_index = colonne - 1
        current_node = self.matrice_jeu[current_rangee][colonne_index]
        empty = False
        while not empty and current_rangee >= 0:
            if current_node.valeur != "":
                current_rangee -= 1
                current_node = current_node.up
            else:
                empty = True

        if empty:
            return current_node
        
        # si la colonne est pleine
        return None


    def updater_board(self, jeton: str, node: Node) -> None:
        """Complexite: min 1 -- max n"""
        if node and node.valeur == "":
            node.valeur = f"{jeton}"
            self.nodes_to_value.append(node)


    def check_for_win(self) -> tuple:
        """Regarde si 4 node ou plus de suite ont la meme valeur et retourne un bool et cette valeur
           Complexite: n^3
        """
        win = False
        winner = ""
        for rangee in self.matrice_jeu:
            for node in rangee:
                if node.valeur != "":
                    win = False
                    winner = ""
                
                    if Board.check_direction(node, "up", "down") >= 4:
                        win = True
                        winner = node.valeur
                        break

                    elif Board.check_direction(node, "left", "right") >= 4:
                        win = True
                        winner = node.valeur
                        break

                    elif Board.check_direction(node, "down_left", "up_right") >= 4:
                        win = True
                        winner = node.valeur
                        break
                            
                    elif Board.check_direction(node, "down_right", "up_left") >= 4:
                        win = True
                        winner = node.valeur
                        break
            if win:
                break

        return (win, winner)

    @staticmethod
    def while_equal_value(node: Node, direction: str, count: int) -> tuple:
        """Calcule la quantité de node de même valeur dans une direction
           Complexite: n
        """
        current_node = node
        node_directions = node.directions()
        while current_node.valeur == node.valeur:
            if node_directions[direction] and node_directions[direction].valeur == node.valeur:
                count += 1
                current_node = node_directions[direction]
                node_directions = current_node.directions()
            else:
                break
        return count

    @staticmethod
    def check_direction(node: Node, d1: str, d2: str):
        """Complexite: n"""
        count = 0
        if node.valeur != '':
            count = 1
            
            count = Board.while_equal_value(node, d1, count)
            count = Board.while_equal_value(node, d2, count)

        return count
    
    @staticmethod
    def check_direction_possible_win(node: Node, d1: str, d2: str):
        """Évalue la valeur d'un axe et ses possibilités de gagner
           Complexite: min 1 -- max n
           Baser sur la theorie de l'heuristique on donne des poids a certaines situations:
           "RRRR": inf,
           "R RR": 200,
           "RR R": 200,
           "RRR ": 500,
           "R R ": 30,
           "R  R": 30,
           "RR  ": 10,
           "R   ": 1
        """
        count = 0
        valeur = node.valeur

        liste_d = [d1, d2]
        for d in liste_d :
            current_node = node
            to_evaluate = current_node.valeur
            for i in range(3):
                if current_node.directions()[d] is not None and (current_node.directions()[d].valeur == '' or current_node.directions()[d].valeur == valeur):
                    letter = current_node.directions()[d].valeur
                    to_evaluate += letter if letter != '' else " "
                    # Source possible d'erreur: parent None
                    current_node = current_node.directions()[d]

            if len(to_evaluate) == 4:
                # nbr_jetons = list(representation).count(valeur)

                to_evaluate = to_evaluate.replace('N', 'R')
                scale = Ai_C4.scale[to_evaluate]
                count += scale
        
        return count


class Joueureuse:
    """Definit une personne jouant au jeu de puissance 4"""
    def __init__(self, jeton_color: str) -> None:
        self.jeton = jeton_color

    def jouer(self, board: Board, colonne: int) -> None:
        """Complexite: n"""
        node_to_modify = board.first_empty_node(colonne)
        board.updater_board(self.jeton, node_to_modify)


class Ai_C4(Joueureuse):
    HAUTEUR  = 5
    scale = {
        "RRRR": inf,
        "R RR": 200,
        "RR R": 200,
        "RRR ": 500,
        "R R ": 30,
        "R  R": 30,
        "RR  ": 10,
        "R   ": 1
    }

    """Definit un ai pouvant jouer contre une personne automatiquement"""
    def __init__(self, jeton_color: str, jeton_ennemi: str) -> None:
        """Complexite: n^2"""
        super().__init__(jeton_color)
        self.jeton_ennemi = jeton_ennemi
        self.root = None
        self.temp_board = Board(6, 7)

    
    def jouer(self, board: Board) -> int:
        colonne = self.next_move(board)
        node_to_modify = board.first_empty_node(colonne)
        board.updater_board(self.jeton, node_to_modify)
        return colonne


    def node_value(self, node: Node) -> int:
        score_vertical = Board.check_direction_possible_win(node, "up", "down")
        score_horizontal = Board.check_direction_possible_win(node, "left", "right")
        score_backslash = Board.check_direction_possible_win(node, "down_right", "up_left")
        score_frontslash = Board.check_direction_possible_win(node, "down_left", "up_right")

        return score_vertical + score_horizontal + score_frontslash + score_backslash


    def board_value(self, board: Board) -> int:
        valeur = 0
        for node in board.nodes_to_value:
            if node.valeur == self.jeton:
                valeur += self.node_value(node)
                continue
            valeur -= self.node_value(node)
        return valeur


    def possible_moves(self, board_state: list, jeton: str) -> list:
        data = []
        for col in range(1, self.temp_board.colonnes + 1):
            self.temp_board.fill(board_state)
            this_board = self.temp_board
            node_jouer = this_board.first_empty_node(col)
            if node_jouer:
                this_board.updater_board(jeton, node_jouer)
                board_value = self.board_value(this_board)
                data.append((this_board.board_to_matrice(), board_value, col))
            self.temp_board.unfill()

        return data


    def moves(self, node: TNode, h: int) -> None:
        """methode de resursion pour trouver tous les moves possibles sur plusieurs tours: h doit etre impair"""
        if h <= 0:
            return

        # node data = (board, value) change == pour != si h est impair
        jeton = self.jeton if h % 2 != 0 else self.jeton_ennemi
        
        board_state = node.data[0]
        coups_possibles = self.possible_moves(board_state, jeton)
        for data in coups_possibles:
            node.enfants.append(TNode(node, data))

        for enfant in node.enfants:
            self.moves(enfant, h-1)

    @staticmethod
    def hauteur(node, colonne = "", h = 0):
        """Methode pour renvoyer ou on est rendu dans la recursion"""
        if not node.parent:
            return h, colonne
        colonne_parent = node.parent.data[2]
        if colonne_parent is None:
            colonne_parent = 0
        return Ai_C4.hauteur(node.parent, str(colonne_parent)+str(colonne), h+1)

    @staticmethod
    def valeur(node: TNode, adversaire: bool = False) -> Node:
        """Methode pour connaitre le meilleur boardstate possible dans le futur selon la valeur max de chaque prochain coups, renvoie la feuille de la branche correspondante"""
        if not node.enfants:
            return node
        elif adversaire:
            return Ai_C4.valeur(min(node.enfants), not adversaire)
        else:
            nodes = []
            for enfant in node.enfants:
                nodes.append(Ai_C4.valeur(enfant, not adversaire))
            valeur = max(nodes)
            return valeur

    def best_path(self, node: TNode) -> TNode:
        """Traverse l'arbre a l'envers pour trouver le bon prochain coup a partir de la meilleur feuille"""
        best_leave = Ai_C4.valeur(node)
        path = best_leave
        while path.parent.parent is not None:
            path = path.parent
        return path

    def next_move(self, board: Board, h: int = HAUTEUR) -> int:
        board_state = board.board_to_matrice()
        self.root = TNode(None, (board_state, (self.board_value(self.temp_board)), None))
        self.temp_board.unfill()
        self.moves(self.root, h)
        best_path = self.best_path(self.root)
        return best_path.data[2]


def ai_game(board: Board, player1: Joueureuse, ai: Ai_C4) -> None:
    firstplayer =  randint(1,2)
    if firstplayer == 1:
        firstplayer = player1
        secondplayer = ai
    else:
        firstplayer = ai
        secondplayer = player1

    won = False
    turn_count = 0
    print(board)
    while not won:
        if turn_count % 2 == 0:
            active_player = firstplayer
        else:
            active_player = secondplayer
        print(f"C'est le tour de : {active_player.jeton}")

        if isinstance(active_player, Ai_C4):
            active_player.jouer(board)
        else:
            colonne = int(input("Entre la colonne : "))
            active_player.jouer(board, colonne)
        win, winner = board.check_for_win()
        turn_count += 1
        print(board)
        if win:
            print(f"La personne jouant: {winner} a gagner!")
            won = True


def main():
    board = Board(6, 7)
    valerie = Joueureuse("N")
    ai = Ai_C4("R", valerie.jeton)

    ai_game(board, valerie, ai)

if __name__ == "__main__":
    main()