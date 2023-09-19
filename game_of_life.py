import random
import time
from collections import namedtuple
import copy
import pygame
from typing import List, Tuple, Optional


def grid_state_in_history(grid: List[List[int]], history) -> bool:
    return any(grid == past_grid for past_grid in history)


class GameOfLife:
    def __init__(self) -> None:
        self.UPDATE_SPEED_SECONDS: float = 0.01
        self.GRID_HEIGHT: int = 80
        self.GRID_WIDTH: int = 80
        self.EMPTY_CELL: int = 0
        self.FULL_CELL: int = 1
        self.CELL_SIZE: int = 10
        self.WINDOW_WIDTH: int = self.GRID_WIDTH * self.CELL_SIZE
        self.WINDOW_HEIGHT: int = self.GRID_HEIGHT * self.CELL_SIZE
        self.STABILITY_THRESHOLD: int = 10
        self.FONT_PATH: str = "/System/Library/Fonts/HelveticaNeue.ttc"

        self.BLACK: Tuple[int, int, int] = (0, 0, 0)
        self.WHITE: Tuple[int, int, int] = (255, 255, 255)
        self.GRAY: Tuple[int, int, int, Optional[int]] = (10, 10, 10, 128)

        self.Coordinates: namedtuple = namedtuple('Coordinates', ['row', 'column'])

        try:
            pygame.init()
            self.title_font = pygame.font.Font(self.FONT_PATH, 36)
            self.font = pygame.font.Font(self.FONT_PATH, 25)
            self.screen = pygame.display.set_mode(
                (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            pygame.display.set_caption("Conway's Game of Life")
        except Exception as e:
            print(f"Error initializing pygame: {e}")

    def create_grid(self) -> List[List[int]]:
        grid = [[self.FULL_CELL if random.randint(1, 5) == 1 else self.EMPTY_CELL
                 for _column in range(self.GRID_WIDTH)]
                for _row in range(self.GRID_HEIGHT)]
        return grid

    def draw_grid(self, grid: List[List[int]]) -> None:
        line_width: int = 1

        for row in range(self.GRID_HEIGHT):
            for column in range(self.GRID_WIDTH):
                color = self.BLACK if grid[row][column] == self.FULL_CELL else self.WHITE
                pygame.draw.rect(self.screen, color, (column * self.CELL_SIZE,
                                                      row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw horizontal lines
        for row in range(self.GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, self.GRAY, (0, row * self.CELL_SIZE),
                             (self.GRID_WIDTH * self.CELL_SIZE, row * self.CELL_SIZE), line_width)

        # Draw vertical lines
        for column in range(self.GRID_WIDTH + 1):
            pygame.draw.line(self.screen, self.GRAY, (column * self.CELL_SIZE, 0),
                             (column * self.CELL_SIZE, self.GRID_HEIGHT * self.CELL_SIZE), line_width)

        pygame.display.flip()

    def draw_generation_number(self, generation: int) -> None:
        try:
            text_surface = self.font.render(
                f"Generation: {generation}", True, self.BLACK)

            border_rect = text_surface.get_rect()
            border_rect.inflate_ip(10, 10)
            border_rect.topleft = (5, 5)

            background_rect = border_rect.copy()
            background_rect.inflate_ip(-2, -2)
            pygame.draw.rect(self.screen, self.WHITE, background_rect)

            pygame.draw.rect(self.screen, self.BLACK, border_rect, 2)
            self.screen.blit(text_surface, (10, 10))
        except Exception as e:
            print(
                f"An error occurred while drawing the generation number: {e}")

    def draw_grid(self, grid: List[List[int]]) -> None:
        try:
            for row in range(self.GRID_HEIGHT):
                for column in range(self.GRID_WIDTH):
                    cell_color = self.WHITE if grid[row][column] == self.EMPTY_CELL else self.BLACK
                    pygame.draw.rect(self.screen, cell_color, (column * self.CELL_SIZE,
                                                               row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)
                    pygame.draw.rect(self.screen, self.GRAY, (column * self.CELL_SIZE,
                                                              row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 1)
        except Exception as e:
            print(f"An error occurred while drawing the grid: {e}")

    def count_neighbors(self, grid: List[List[int]], coordinates: namedtuple) -> int:
        row, column = coordinates.row, coordinates.column
        count = 0
        try:
            for row_shift in [-1, 0, 1]:
                for column_shift in [-1, 0, 1]:
                    if row_shift == 0 and column_shift == 0:
                        continue
                    if 0 <= row + row_shift < self.GRID_HEIGHT and 0 <= column + column_shift < self.GRID_WIDTH:
                        count += grid[row + row_shift][column + column_shift]
        except Exception as e:
            print(f"An error occurred while counting neighbors: {e}")
        return count

    def update_grid(self, grid: List[List[int]]) -> List[List[int]]:
        new_grid = copy.deepcopy(grid)
        try:
            for row in range(self.GRID_HEIGHT):
                for column in range(self.GRID_WIDTH):
                    neighbor_count = self.count_neighbors(
                        grid, self.Coordinates(row, column))
                    if grid[row][column] == self.FULL_CELL:
                        if neighbor_count not in [2, 3]:
                            new_grid[row][column] = self.EMPTY_CELL
                    elif neighbor_count == 3:
                        new_grid[row][column] = self.FULL_CELL
        except Exception as e:
            print(f"An error occurred while updating the grid: {e}")
        return new_grid

    def count_all_cells(self, grid: List[List[int]]) -> int:
        return sum(1 for row in range(self.GRID_HEIGHT)
                   for column in range(self.GRID_WIDTH)
                   if grid[row][column] == self.FULL_CELL)

    def create_empty_grid(self) -> list:
        return [[self.EMPTY_CELL for _column in range(self.GRID_WIDTH)] for _row in range(self.GRID_HEIGHT)]

    def draw_custom_grid(self):
        grid: List[List[int]] = self.create_empty_grid()
        running: bool = True
        drawing: bool = False
        last_toggled_cell: Optional[Tuple[int, int]] = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row, column = mouse_y // self.CELL_SIZE, mouse_x // self.CELL_SIZE
                    grid[row][column] = self.EMPTY_CELL if grid[row][column] == self.FULL_CELL else self.FULL_CELL
                    last_toggled_cell = (row, column)
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    last_toggled_cell = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            if drawing:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, column = mouse_y // self.CELL_SIZE, mouse_x // self.CELL_SIZE
                if (row, column) != last_toggled_cell:
                    grid[row][column] = self.EMPTY_CELL if grid[row][column] == self.FULL_CELL else self.FULL_CELL
                    last_toggled_cell = (row, column)

            self.draw_grid(grid)
            pygame.display.flip()

        return grid

    def run_simulation(self, grid: List[List[int]]):
        generation_number: int = 0
        grid_history: List[List[List[int]]] = []
        stable_generation_number: Optional[int] = None
        should_draw: bool = True

        running = True
        while running:
            running, should_draw = self.handle_events(
                running, should_draw, grid, generation_number, stable_generation_number)

            if stable_generation_number is None:
                time.sleep(self.UPDATE_SPEED_SECONDS)

                if grid_state_in_history(grid, grid_history):
                    stable_generation_number = generation_number
                    should_draw = True
                else:
                    grid_history.append(copy.deepcopy(grid))
                    if len(grid_history) > self.STABILITY_THRESHOLD:
                        grid_history.pop(0)

                    grid = self.update_grid(grid)
                    generation_number += 1
                    should_draw = True

        pygame.quit()

    def handle_events(self, running: bool, should_draw: bool, grid: List[List[int]], generation_number: int,
                      stable_generation_number: Optional[int]) -> Tuple[bool, bool]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if should_draw:
            self.draw_grid(grid)
            self.draw_generation_number(generation_number)
            pygame.display.flip()
            should_draw = False

        return running, should_draw

    def main_game_loop(self) -> None:
        def draw_button(text: str, x: int, y: int, padding: int = 10) -> pygame.Rect:
            try:
                text_surface = self.font.render(text, True, self.BLACK)
                text_rect = text_surface.get_rect()
                button_rect = pygame.Rect(
                    x, y, text_rect.width + padding * 2, text_rect.height + padding * 2)
                pygame.draw.rect(self.screen, self.BLACK, button_rect, 3)
                pygame.draw.rect(self.screen, self.WHITE,
                                 button_rect.inflate(-2, -2))
                text_rect.center = button_rect.center
                self.screen.blit(text_surface, text_rect)
                return button_rect
            except Exception as ex:
                print(f"An error occurred while drawing the button: {ex}")
                return pygame.Rect(0, 0, 0, 0)

        title: str = "Conway's Game of Life"
        try:
            title_surface = self.title_font.render(title, True, self.BLACK)
            title_rect = title_surface.get_rect()
            title_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 4)
        except Exception as e:
            print(f"An error occurred while rendering the title: {e}")
            return

        option1: str = "Start with a random grid"
        option2: str = "Draw your own starting grid"

        button_padding = 30
        padding = 10
        option1_button_width = self.font.size(option1)[0] + padding * 2
        option1_button_x = (self.WINDOW_WIDTH - option1_button_width) // 2
        option2_button_width = self.font.size(option2)[0] + padding * 2
        option2_button_x = (self.WINDOW_WIDTH - option2_button_width) // 2

        option1_button = draw_button(
            option1, option1_button_x, self.WINDOW_HEIGHT // 2 - button_padding)
        option2_button = draw_button(
            option2, option2_button_x, self.WINDOW_HEIGHT // 2 + button_padding)

        running = True
        grid: Optional[List[List[int]]] = None

        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if option1_button.collidepoint(pygame.mouse.get_pos()):
                            grid = self.create_grid()
                            running = False
                        if option2_button.collidepoint(pygame.mouse.get_pos()):
                            grid = self.draw_custom_grid()
                            running = False

                if option1_button.collidepoint(pygame.mouse.get_pos()) or option2_button.collidepoint(
                        pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(
                        pygame.SYSTEM_CURSOR_HAND)  # Change cursor type
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                self.screen.fill(self.WHITE)
                self.screen.blit(title_surface, title_rect)
                option1_button = draw_button(
                    option1, option1_button.x, option1_button.y)
                option2_button = draw_button(
                    option2, option2_button.x, option2_button.y)
                pygame.display.flip()
            except Exception as e:
                print(f"An error occurred in the main game loop: {e}")
                running = False

        if grid is not None:
            self.run_simulation(grid)
        else:
            pygame.quit()


if __name__ == "__main__":
    game = GameOfLife()
    game.main_game_loop()
