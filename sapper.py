from random import shuffle

MINE = 10

CLOSED = 0
OPEN = 1
FLAGGED = 2

CONTINUES = 0
WON = 1
LOST = 2

def pad(item, length:int = 2)->str:
    item = str(item)
    return ' ' * (length - len(item)) + item

def _debug_print_table(field: list[list[int]])->None:
    for row in field:
        print(*list(map(pad, row)))

class Game:
    def _count_mines_around_cells(self)->None:
        for i in range(self.rows): # для каждой строки
            for j in range(self.cols): # для каждого столбца
                if self.field[i][j] != 10: # если ячейка i,j - не мина
                    continue # то пропускаем
                # если не пропустили, то в i, j мина
                for x in range(max(0, i-1), min(i+2, self.rows)): # для каждой строки вокруг iй
                    for y in range(max(0, j-1), min(j+2, self.cols)): # для каждого столбца вокруг j-го
                        self.field[x][y] += int(self.field[x][y] != 10)
        return None

    def _create_field(self, first_row:int, first_col:int)->None:
        self.field = [[0] * self.cols for _ in range(self.rows)]
        self.field_state = [[CLOSED] * self.cols for _ in range(self.rows)]
        self.field_state[first_row][first_col] = OPEN

        pos = []
        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                if row != first_row or col != first_col:
                    pos.append((row, col))

        shuffle(pos)
        for i in range(min(mines, len(pos))):
            r = pos[i][0]
            c = pos[i][1]
            self.field[r][c] = MINE
        self._count_mines_around_cells()
        #print('DEBUG INFO: self.field created with state:')
        #_debug_print_table(self.field)
        #print('state:')
        #_debug_print_table(self.field_state)
        #print('END OF DEBUG INFO')
        #print()
        if mines >= len(pos):
            self.state = WON
        return None


    def __init__(self, rows:int, cols:int, mines:int, first_row:int, first_col:int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self._create_field(first_row, first_col)
        self.closed_count = rows * cols - 1
        self.state = CONTINUES

    def open_around_zero(self, row: int, col: int) -> None:
        for x in range(max(0, row - 1), min(row + 2, row)):
            for y in range(max(0, col - 1), min(col + 2, col)):
                self.open(x, y)
        return None

    def open(self, row:int, col:int)->None:
        if self.state != CONTINUES:
            return None
        if self.field_state[row][col] == CLOSED:
            self.field_state[row][col] = OPEN
            self.closed_count -= 1
            if self.field[row][col] == MINE:
                self.state = LOST
            elif self.mines == self.closed_count:
                self.state = WON
            elif self.field[row][col] == 0:
                self.open_around_zero(row, col)
        return None

    def flag(self, row:int, col:int)->None:
        if self.state != CONTINUES:
            return None
        if self.field_state[row][col] == CLOSED:
            self.field_state[row][col] = FLAGGED
        return None

    def unflag(self, row:int, col:int)->None:
        if self.state != CONTINUES:
            return None
        if self.field_state[row][col] == FLAGGED:
            self.field_state[row][col] = CLOSED
        return None


def print_game_field(game:Game)->None:
    max_row_width = len(str(game.rows - 1))
    max_col_width = len(str(game.cols - 1))
    print(' ' * (max_row_width + 1), end='|')
    for col in range(game.cols):
        print(pad(col, max_col_width), end='|')
    print()

    for row in range(game.rows):
        print(pad(row, max_row_width), '|', end='')
        for col in range(game.cols):
            toprnt = '-'
            if game.field_state[row][col] == OPEN:
                toprnt = '*'
                if game.field[row][col] != MINE:
                    toprnt = str(game.field[row][col])
            elif game.field_state[row][col] == FLAGGED:
                toprnt = 'P'
            print(pad(toprnt, max_col_width), end='|')
        print()

def get_validated_input_generic(input_message: str, error_message: str, clear, good, transform):
    x = clear(input(input_message))
    while not good(x):
        print(error_message)
        x = clear(input(input_message))
    return transform(x)


def get_int(message: str)->int:
    def good(x: str)->bool:
        return x.isdigit()
    def clear(x: str)->str:
        return x.strip()
    return get_validated_input_generic(message + ': ', 'введите число!', clear, good, int)

def get_two_bounded_ints(message: str, first_bound: int, second_bound: int)->tuple[int, int]:
    def good(x: list[str])->bool:
        if len(x) != 2:
            return False
        if not x[0].isdigit() or not x[1].isdigit():
            return False
        a, b = map(int, x)
        return (0 <= a < first_bound and
                0 <= b < second_bound)
    def clear(x: str):
        return x.strip().split()
    def transform(x):
        return (int(x[0]), int(x[1]))
    return get_validated_input_generic(message + ': ', 'Введите два числа через пробел!', clear, good, transform)


def get_character_from_set(message: str, good: list[str], case_sensitive: bool = False)->str:
    x = input(message + ': ').strip()
    y = '$$$'
    if not case_sensitive:
        x = x.lower()
        y = x.upper()
    while (not x in good) and (not y in good):
        x = input(message + ': ').strip()
        y = '$$$'
        if not case_sensitive:
            x = x.lower()
            y = x.upper()
    return x if x in good else y

rows = get_int("Строки")
cols = get_int("Столбцы")
mines = get_int("Кол-во мин")
print("Игра создается...")
print()
row, col = get_two_bounded_ints('Введите строку, столбец для открытия', rows, cols)
game = Game(rows, cols, mines, row, col)

print_game_field(game)

while game.state == CONTINUES:
    n = get_character_from_set("Какое действие совершить (Open [O] / FLag [F] / Unflag [U])", list('OFU'))
    row, col = get_two_bounded_ints("Строка, столбец", rows, cols)
    if n == "O":
        game.open(row, col)
    elif n == "F":
        game.flag(row, col)
    elif n == "U":
        game.unflag(row, col)
    print_game_field(game)

if game.state == LOST:
        print("Вы проиграли! :(")
        run = False
elif game.state == WON:
    print("Вы выиграли!")
    run = False
