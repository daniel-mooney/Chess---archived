from chess import Chess
import numpy as np


board_1 = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', '0', 'B', 'Q', 'K', 'B', '0', 'R'],
            ['7', 'P', 'P', 'P', 'P', '0', 'P', 'P', 'P'],
            ['6', '0', '0', 'N', '0', '0', 'N', '0', '0'],
            ['5', '0', '0', '0', '0', 'P', '0', '0', '0'],
            ['4', '0', '0', 'b', '0', 'p', '0', '0', '0'],
            ['3', '0', '0', '0', '0', '0', 'q', '0', '0'],
            ['2', 'p', 'p', 'p', 'p', '0', 'p', 'p', 'p'],
            ['1', 'r', 'n', 'b', '0', 'k', '0', 'n', 'r']
        ])

board_2 = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', 'R', 'N', 'B', 'Q', 'K', 'B', '0', 'R'],
            ['7', 'P', 'P', '0', '0', 'P', 'P', 'P', 'P'],
            ['6', '0', '0', '0', '0', '0', 'N', '0', '0'],
            ['5', '0', '0', 'P', '0', '0', '0', '0', '0'],
            ['4', '0', '0', 'b', 'p', '0', '0', '0', '0'],
            ['3', '0', '0', 'n', '0', 'p', '0', '0', '0'],
            ['2', 'p', 'p', '0', '0', '0', 'p', 'p', 'p'],
            ['1', 'r', '0', 'b', 'q', 'k', '0', 'n', 'r']
        ])

board_3 = np.array([
            ["-", "A", "B", "C", "D", "E", "F", "G", "H"],
            ['8', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['7', '0', '0', 'K', '0', '0', 'N', '0', '0'],
            ['6', 'R', '0', '0', '0', '0', '0', '0', '0'],
            ['5', '0', '0', '0', '0', '0', '0', '0', 'p'],
            ['4', '0', '0', '0', '0', '0', '0', 'p', '0'],
            ['3', '0', '0', '0', '0', 'b', 'k', '0', '0'],
            ['2', '0', '0', '0', 'q', '0', '0', '0', '0'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0']
        ])
