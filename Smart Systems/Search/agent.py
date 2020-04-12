from collections import deque
import numpy as np
import time


class Agent:
    class SearchTypes:
        BREATH_FIRST_SEARCH = "BFS"
        DEPTH_FIRST_SEARCH = "DFS"
        DIJKSTRA = "DIJKSTRA"
        A_STAR = "A*"

    def __init__(self, env, type_search=SearchTypes.BREATH_FIRST_SEARCH, render=True):
        self.env = env
        self.type_search = type_search
        self.render = render

    def process(self):
        self.env.reset()

        if self.render:
            # Render tha maze
            self.env.render()

        # Perfom the search
        if self.type_search == self.SearchTypes.BREATH_FIRST_SEARCH:
            path = self.simulate_BFS()
        elif self.type_search == self.SearchTypes.A_STAR:
            path = self.simulate_A_star()

        if self.render and path:
            shortest_path = self.recover_solution_path(path)
            self.draw_path(shortest_path)

    def simulate_BFS(self):

        queue = deque()
        path = {}
        done = False

        initial_pos = self.env.maze_view._MazeView2D__robot
        queue.append(initial_pos)
        path[self.pos_2_vec(initial_pos)] = None

        while not done:
            node = queue.popleft()

            # Check if the cuurrentt node is the goal
            if all(node == self.env.maze_view.goal):
                done = True
                return path

            self.move_robot(node)
            self.handle_neighboors(node, path, queue)

            if self.render:
                self.env.maze_view.update()
                time.sleep(.1)

    def simulate_DFS(self):
        pass

    def simulate_dijkstra(self):
        pass

    def simulate_A_star(self):
        pass

    def pos_2_vec(self, pos):
        return (pos[0], pos[1])

    def handle_neighboors(self, current, path, queue):
        for move in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            next_move = [current[0] + move[0], current[1] + move[1]]
            # Valide borders
            if next_move[0] < 0 or next_move[0] > 9 or next_move[1] < 0 or next_move[1] > 9:
                continue

            self.move_robot(next_move, set_pos=False)
            new_pos = self.env.maze_view._MazeView2D__robot
            # A move was valid if pos changed
            # valid = not all(current == new_pos)
            valid = self.is_open(current, next_move, move)
            # Return to the current
            self.move_robot(current)

            if valid and self.pos_2_vec(next_move) not in path and next_move not in queue:
                queue.append(next_move)
                path[self.pos_2_vec(next_move)] = self.pos_2_vec(current)

    def move_robot(self, dir, set_pos=True):
        # update the drawing
        self.env.maze_view._MazeView2D__draw_robot(transparency=0)

        # move the robot
        if set_pos:
            self.env.maze_view._MazeView2D__robot = np.array(dir)
        else:
            self.env.maze_view._MazeView2D__robot += np.array(dir)
        # if it's in a portal afterward
        if self.env.maze_view.maze.is_portal(self.env.maze_view.robot):
            self.env.maze_view._MazeView2D__robot = np.array(self.env.maze_view.maze.get_portal(
                tuple(self.env.maze_view.robot)).teleport(tuple(self.env.maze_view.robot)))
        self.env.maze_view._MazeView2D__draw_robot(transparency=255)

    def move_robot(self, dir, set_pos=True):
        # update the drawing
        self.env.maze_view._MazeView2D__draw_robot(transparency=0)

        # move the robot
        if set_pos:
            self.env.maze_view._MazeView2D__robot = np.array(dir)
        else:
            self.env.maze_view._MazeView2D__robot += np.array(dir)
        # if it's in a portal afterward
        if self.env.maze_view.maze.is_portal(self.env.maze_view.robot):
            self.env.maze_view._MazeView2D__robot = np.array(self.env.maze_view.maze.get_portal(
                tuple(self.env.maze_view.robot)).teleport(tuple(self.env.maze_view.robot)))
        self.env.maze_view._MazeView2D__draw_robot(transparency=255)

    def recover_solution_path(self, path):
        final_pos = (9, 9)
        shortest_path = deque()
        shortest_path.append(final_pos)
        ancestor = path[final_pos]
        while ancestor:
            shortest_path.appendleft(ancestor)
            ancestor = path[ancestor]
        return shortest_path

    def is_open(self, current, next_move, move):

        if move == [0, 1]:
            dir = "S"
        elif move == [0, -1]:
            dir = "N"
        elif move == [1, 0]:
            dir = "E"
        elif move == [-1, 0]:
            dir = "W"

        x1, y1 = next_move[0], next_move[1]
        # if cell is still within bounds after the move
        if self.env.maze_view.maze.is_within_bound(x1, y1):
            # check if the wall is opened
            this_wall = bool(self.env.maze_view.maze.get_walls_status(
                self.env.maze_view.maze.maze_cells[current[0], current[1]])[dir])

            other_wall = bool(self.env.maze_view.maze.get_walls_status(
                            self.env.maze_view.maze.maze_cells[x1, y1])[self.env.maze_view.maze._Maze__get_opposite_wall(dir)])
            return this_wall or other_wall
        return False

    def draw_path(self, path):
        path = list(path)
        for cell in path:
            self.env.maze_view._MazeView2D__colour_cell(
                cell, colour=(160, 60, 60), transparency=240)
            self.env.render()
