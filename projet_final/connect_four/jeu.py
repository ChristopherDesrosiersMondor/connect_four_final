"""
CURRENT BUGS

Le check for win dans le jeu ne sors pas si R gagne vertical
    [X] C'etais parce qu'on sortait pas du for loop sur les rangees dans check for win donc si le win venait pas de la
        derniere rangee ca callait pas

Le ai joue toujours dans la col1 si la hauteur de prediction est a 1 et agit weird a 2. a 3 tout va bien

Le ai ne bloque pas deux tours d'avance
    [X] Mettre le h a 5
    [X] Changer l'algorithme pour calculer le max en recursion des leaves
        [X] implementer la surcharge de < et > dans TNODE sur la valeur du board (data[1])

Le ai prend trop de temps a 5 de H
    [ ] Changer le deepcopy pour une fonction qui enleve le dernier coup jouer.

L'heuristique ne donnes pas de poid aux jetons en ligne genre 2 colles ou 3 colles
    [X] modifier l'heuristique pour en tenir compte.

"""


import copy
from random import randint
from math import inf


class Node:
    """Definit un node utiliser avec la theorie des graphe pour garder le board state du jeu"""
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
    """Definit un node dans le sens de la structure d'arbre"""
    def __init__(self, parent: 'TNode', data: object) -> None:
        self.parent = parent
        self.data = data
        self.board = data[0]
        self.value = data[1]
        self.colonne = data[2]
        self.enfants = []
        TNode.id += 1
        self.id = TNode.id

    """Weird comportement quand on arrive a evaluer un coup avant la victoire adverse le self devient un objet adversaire dans la fonction path_Value..."""
    def path_value(self, h: int) -> int:
        """Calculer la valeur d'un chemin de la feuille a la racine"""
        node = self
        value = 0
        for i in range(h):
            value = self.data[1] + value
            node = self.parent
        return value

    def childs_value(self) -> int:
        value = 0
        for enfant in self.enfants:
            value += enfant.data[1]
        return value

                #https://stackoverflow.com/questions/1649027/how-do-i-print-out-a-tree-structure
                # 
                #  {    
        #    public void PrintPretty(string indent, bool last)
        #    {
        #        Console.Write(indent);
        #        if (last)
        #        {
        #            Console.Write("\\-");
        #            indent += "  ";
        #        }
        #        else
        #        {
        #            Console.Write("|-");
        #            indent += "| ";
        #        }
        #        Console.WriteLine(Name);

        #        for (int i = 0; i < Children.Count; i++)
        #            Children[i].PrintPretty(indent, i == Children.Count - 1);
        #    }
        # }
    @staticmethod
    def last(node: 'TNode') -> bool:
        if not node.enfants:
            return True
        return False

    @staticmethod
    def print_pretty(node: 'TNode', indent: str = "", last: bool = False) -> None:
        to_print = ""
        if TNode.last(node):
            to_print += "|-----  "
        else:
            to_print += "\\-"
            indent += "|  "

        TNode.tree_rep += f"{indent}{to_print} V: {node.value} C:{node.colonne} \n"
        
        for enfant in node.enfants:
            TNode.print_pretty(enfant, indent, last)

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
        self.rangees = lignes
        self.colonnes = colonnes
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

    def node_voisinage(self) -> None:
        """
        Source: https://stackoverflow.com/questions/7872838/one-line-if-condition-assignment
        User Frost
        Use: one line asignment if else
        """
        matrice_jeu = self.matrice_jeu
        for R, rangee in enumerate(self.matrice_jeu):
            for C, node in enumerate(rangee):

                # Si la rangee depasse le nombre de rangees c'est que ya rien 
                r_in_range = R + 1 <= self.rangees - 1

                # Si la colonne depasse le nombre de colonnes c'est que y'a rien
                c_in_range = C + 1 <= self.colonnes - 1

                # Si Rangee est negatif y'a rien
                r_positive = R - 1 >= 0

                # Si Colonne est negatif y'a rien
                c_positive = C - 1 >= 0

                # Et ca fonctionne parce qu'on regarde just la ou les conditions qui pourraient briser l'assignement
                node.up = matrice_jeu[R-1][C] if r_positive else None
                node.down = matrice_jeu[R+1][C] if r_in_range else None
                node.right = matrice_jeu[R][C+1] if c_in_range else None
                node.left = matrice_jeu[R][C-1] if c_positive else None
                node.up_right = matrice_jeu[R-1][C+1] if c_in_range and r_positive else None
                node.up_left = matrice_jeu[R-1][C-1] if r_positive and c_positive else None
                node.down_right = matrice_jeu[R+1][C+1] if r_in_range and c_in_range else None
                node.down_left = matrice_jeu[R+1][C-1] if r_in_range and c_positive else None


    def first_empty_node(self, colonne: int) -> Node:
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
        return current_node


    def updater_board(self, jeton: str, node: Node) -> None:
        if node and node.valeur == "":
            node.valeur = f"{jeton}"


    # Retourner un tuple (win: bool, winner: str)
    # winner = "" si win != True
    def check_for_win(self) -> tuple:
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
        count = 0
        if node.valeur != '':
            count = 1
            
            count = Board.while_equal_value(node, d1, count)
            count = Board.while_equal_value(node, d2, count)
        
        # if count >= 4:
        #     count = inf 

        return count
    
    @staticmethod
    def check_direction_possible_win(node: Node, d1: str, d2: str):
        count = 2
        count_same_value = Board.check_direction(node, d1, d2)
        espace = 1
        list = [d1, d2]
        for d in list :
            current_node = node
            node_directions = current_node.directions()
            for i in range(3):
                if node_directions[d] is not None and (node_directions[d].valeur == node.valeur or node_directions[d].valeur == ''):
                    if node_directions[d].valeur == node.valeur:
                        count += 10
                        count *= 2
                    else:
                        count += 1
                    current_node = node_directions[d]
                    node_directions = current_node.directions()
                    espace += 1

        if espace < 4:
            count = 0
        
        if count_same_value >= 4:
            count = inf
        
        return count


class Joueureuse:
    """Definit une personne jouant au jeu de puissance 4"""
    def __init__(self, jeton_color: str) -> None:
        self.jeton = jeton_color

    def jouer(self, board: Board, colonne: int) -> None:
        node_to_modify = board.first_empty_node(colonne)
        board.updater_board(self.jeton, node_to_modify)


#Travailler sur une copie du board
class Ai_C4(Joueureuse):
    HAUTEUR  = 5
    """Definit un ai pouvant jouer contre une personne automatiquement"""
    def __init__(self, jeton_color: str, jeton_ennemi: str) -> None:
        super().__init__(jeton_color)
        self.jeton_ennemi = jeton_ennemi
        self.leaves = {}
        self.root = None
        self.tree = {}
        self.next_moves = []
    
    def jouer(self, board: Board) -> int:
        colonne = self.next_move(board)
        # TNode.print_pretty(self.root)
        # with open('test.txt', 'w', encoding='utf-8') as file:
        #     file.write(TNode.tree_rep)
        # TNode.tree_rep = ""
        node_to_modify = board.first_empty_node(colonne)
        board.updater_board(self.jeton, node_to_modify)
        return colonne

    def draw_solution(self):
        self.draw_tree(self.root, 0)
        affichage = ""
        for niveau, list_node in self.tree.items():
            for node in list_node:
                # if node.data[1] == inf or node.data[1] == -inf:
                affichage += f" {niveau}: v:{node.data[1]} c:{node.data[2]} "
            affichage += "\n"
        
        print(affichage)

    def draw_last(self):
        self.draw_tree(self.root, 0)
        affichage = ""
        for niveau, list_node in self.tree.items():
            try:
                self.tree[niveau+1]
            except:
                highest_node = max(list_node)
                lowest_node = min(list_node)
                affichage += f"high: {highest_node.data[1]} low:{lowest_node.data[1]}"

        print(affichage)

    def draw_tree(self, node: TNode, k: int):
        if not node.enfants:
            return
        
        for node in node.enfants:
            if k not in self.tree:
                self.tree[k] = [node]
            else:
                self.tree[k].append(node)
            self.draw_tree(node, (k+1))


    def node_value(self, node: Node) -> int:
        score_vertical = Board.check_direction_possible_win(node, "up", "down")
        score_horizontal = Board.check_direction_possible_win(node, "left", "right")
        score_backslash = Board.check_direction_possible_win(node, "down_right", "up_left")
        score_frontslash = Board.check_direction_possible_win(node, "down_left", "up_right")

        return score_vertical + score_horizontal + score_frontslash + score_backslash
        
    #on devrait l'appeler jouer comme dans la classe parent
    def jouer_colonne(self, jeton: str, board: Board, colonne: int) -> Board:
        node_jouer = board.first_empty_node(colonne)
        if node_jouer:
            board.updater_board(jeton, node_jouer)
        return board

    def board_value(self, board: Board) -> int:
        valeur = 0
        for row in board.matrice_jeu:
            for node in row:
                if node.valeur == self.jeton:
                    valeur += self.node_value(node)
                elif node.valeur == self.jeton_ennemi:
                    valeur -= self.node_value(node)
        return valeur

    def possible_moves(self, board: Board, jeton: str) -> list:
        data = []
        for col in range(1, board.colonnes + 1):
            this_board = copy.deepcopy(board)
            this_board = self.jouer_colonne(jeton, this_board, col)
            # print(this_board)
            # print(self.board_value(this_board))
            data.append((this_board, self.board_value(this_board), col))
            # node_jouer.valeur = ""
        return data


    def moves(self, node: TNode, h: int) -> None:
        """h doit etre impair"""
        if h <= 0:
            return

        # node data = (board, value) change == pour != si h est impair
        jeton = self.jeton if h % 2 != 0 else self.jeton_ennemi
        
        temp_board = copy.deepcopy(node.data[0])
        coups_possibles = self.possible_moves(temp_board, jeton)
        for data in coups_possibles:
            node.enfants.append(TNode(node, data))

        for enfant in node.enfants:
            self.moves(enfant, h-1)

    def valeur_enfants(self, node: TNode, valeur: int) -> int:
        if node.enfants == []:
            for node in node.enfants:
                valeur += node.data[1]
            return valeur

        for node in node.enfants:
            valeur += node.data[1]
        
        return self.valeur_enfants(node, valeur)

    @staticmethod
    def valeur(node: TNode, adversaire: bool = False):
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
        best_leave = Ai_C4.valeur(node)
        path = best_leave
        while path.parent.parent is not None:
            path = path.parent
        return path, best_leave

    def next_move(self, board: Board, h: int = HAUTEUR) -> int:
        self.root = TNode(None, (board, (self.board_value(board)), None))
        self.moves(self.root, h)
        best_path, best_leave = self.best_path(self.root)
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

    # valerie.jouer(board, 4)
    # ai.jouer(board)

    # valerie.jouer(board, 1)
    # ai.jouer(board)

    # valerie.jouer(board, 1)
    # ai.jouer(board)

    # valerie.jouer(board, 1)
    # ai.jouer(board)

    # print(board)
    # print(board.check_for_win())

if __name__ == "__main__":
    main()


