class Player:
    def __init__(self, id, color):
        self.id = id
        self.mention = "<@!" + str(id) + ">"
        self.color = color


class Board:
    def __init__(self):
        self.color_order = ["Green", "Yellow", "Red", "Blue"]
        self.color_to_players = {}
        # create a 2x7x6 board (dxwxh)
        self.board = []
        self.doubles_used = {}
        for depth in range(2):
            deep = []
            for columns in range(7):
                column = []
                for rows in range(6):
                    column.append("None")
                deep.append(column)
            self.board.append(deep)

    def get_player_color(self, count):
        return self.color_order[count - 1]

    def add_player(self, id, count):
        if count < 5:
            curr_color = self.get_player_color(count)
            temp = Player(id, curr_color)
            self.color_to_players[curr_color] = temp
            self.doubles_used[curr_color] = 0

    def mention_player(self, color):
        return self.color_to_players[color].mention

    def id_player(self, color):
        return self.color_to_players[color].id

    def get_color(self, player_id):
        for i in self.color_to_players.values():
            if i.id == player_id:
                return i.color
        return "None"

    def get_player_count(self):
        return len(self.color_to_players)

    def convert_color(self, color):
        if color == "Blue":
            return (50, 119, 222)
        elif color == "Red":
            return (230, 62, 43)
        elif color == "Yellow":
            return (255, 255, 0)
        elif color == "Green":
            return (52, 220, 90)
        else:
            return (0, 0, 0)

    def next_color(self, color):
        curr_index = 0
        for i in range(self.get_player_count()):
            if self.color_order[i] == color:
                curr_index = i + 1
                break
        if curr_index == self.get_player_count():
            curr_index = 0
        return self.color_order[curr_index]

    def drop(self, front, column, color):
        if front != "double":
            deep = 0
            if front == "front":
                deep = 1
            u = 0
            for i in self.board[deep][column]:
                if i == "None":
                    k = u
                    while k < 5:
                        if self.board[deep][column][k+1] != "None":
                            u = k + 2
                        k += 1
                    self.board[deep][column][u] = color
                    break
                u += 1
        else:
            u = 0
            for i in self.board[0][column]:
                if i == "None" and self.board[1][column][u] == "None":
                    self.board[1][column][u] = color
                    self.board[0][column][u] = color
                    break
                u += 1
