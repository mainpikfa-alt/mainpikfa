# Размеры окна
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# Параметры игрового поля
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 50
BOARD_SIZE = GRID_SIZE * CELL_SIZE

# Позиции досок
BOARD1_X = MARGIN
BOARD1_Y = MARGIN + 100
BOARD2_X = WINDOW_WIDTH - MARGIN - BOARD_SIZE
BOARD2_Y = MARGIN + 100

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
GREEN = (0, 128, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Размеры кораблей
# 1 × четырехпалубный, 2 × трехпалубных, 3 × двухпалубных, 4 × однопалубных
SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]