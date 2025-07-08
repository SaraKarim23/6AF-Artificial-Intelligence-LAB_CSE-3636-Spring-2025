import math
import heapq


class Algo:
    def __init__(self):
        self.ROW = 9
        self.COL = 9
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float("inf")  # Total cost of the cell (g + h)
        self.g = float("inf")  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
        self.mat = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 1, 0, 0],
        ]
        self.src = (4, 4)
        self.targets = [
            (0, 0),
            (0, 5),
            (0, 8),
            (2, 0),
            (2, 8),
            (5, 0),
            (6, 7),
            (8, 0),
            (8, 2),
            (8, 6),
        ]
        self.update_targets = []
        self.foodNames = ["Burger", "Pizza", "Pasta", "Sandwich", "Sushi"]
        self.foodMakingTime = [5, 7, 8, 4, 6]
        self.path = []

    def construct_matrix(self, table_numbers):
        # set 0 to the remaining cells of table_numbers in the matrix
        # print(table_numbers)
        for i in range(9):
            if i not in table_numbers:
                ik, jk = self.targets[i]
                self.mat[ik][jk] = 0
            else:
                self.update_targets.append(self.targets[i])

        # print(self.mat)

    # Check if a cell is valid (within the grid)
    def is_valid(self, row, col):
        return (row >= 0) and (row < self.ROW) and (col >= 0) and (col < self.COL)

    # Check if a cell is unblocked
    def is_unblocked(self, row, col):
        return self.mat[row][col] == 1

    # Check if a cell is the destination
    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def calculate_h_value(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    # Trace the path from source to destination
    def trace_path(self, cell_details, dest):
        self.path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (
            cell_details[row][col].parent_i == row
            and cell_details[row][col].parent_j == col
        ):
            self.path.append({"row": row, "col": col})
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        self.path.append({"row": row, "col": col})
        # Reverse the path to get the path from source to destination
        self.path.reverse()

    # Implement the A* search algorithm
    def a_star_search(self, dest):
        # Check if the source and destination are valid
        if not self.is_valid(self.src[0], self.src[1]) or not self.is_valid(
            dest[0], dest[1]
        ):
            print("Source or destination is invalid")
            return

        # Check if the source and destination are unblocked
        if not self.is_unblocked(self.src[0], self.src[1]) or not self.is_unblocked(
            dest[0], dest[1]
        ):
            print("Source or the destination is blocked")
            return

        # Check if we are already at the destination
        if self.is_destination(self.src[0], self.src[1], dest):
            print("We are already at the destination")
            return

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        # Initialize the details of each cell
        cell_details = [[Algo() for _ in range(self.COL)] for _ in range(self.ROW)]

        # Initialize the start cell details
        i = self.src[0]
        j = self.src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if (
                    self.is_valid(new_i, new_j)
                    and self.is_unblocked(new_i, new_j)
                    and not closed_list[new_i][new_j]
                ):
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        # Trace and print the path from source to destination
                        self.trace_path(cell_details, dest)
                        found_dest = True
                        return
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if (
                            cell_details[new_i][new_j].f == float("inf")
                            or cell_details[new_i][new_j].f > f_new
                        ):
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")

    def get_details(self, orders):
        table_numbers = []
        information = []
        for order in orders:
            table_number = int(order["tableNumber"].replace("t", "")) - 1
            table_numbers.append(table_number)
            food_items = order["foodItems"]
            total_time = 0
            for food_item in food_items:
                food_id = int(food_item["id"]) - 1
                quantity = food_item["quantity"]
                total_time += self.foodMakingTime[food_id] * quantity
            information.append(
                {
                    "table": f"t{table_number + 1}",
                    "target": self.targets[table_number],
                    "time": total_time,
                    "cost": 0,
                    "path": [],
                }
            )
        self.construct_matrix(table_numbers)
        for info in information:
            self.a_star_search(info["target"])
            info["path"] = self.path
            info["cost"] = len(self.path) - 1

        return information
