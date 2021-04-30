from Cell import Cell 
import tkinter

class Board:
    def __init__(self, rows, columns): 
        self._rows = rows
        self._columns = columns
        
        self._grid = []
        
        for cell_column in range(columns):
            row = []
            for cell_row in range(rows):
                cell = Cell()
                row.append(cell)
            self._grid.append(row)


        self.mainWindow = tkinter.Tk()
        self.mainWindow.minsize(500, 300)

        positionRight = int(self.mainWindow.winfo_screenwidth()/2 - 500/2)
        positionDown = int(self.mainWindow.winfo_screenheight()/2 - 300/2)
        self.mainWindow.geometry("+{}+{}".format(positionRight, positionDown))

        self.cell_dimension =  (self.mainWindow.winfo_screenheight() - 100)/rows

        self.board_canvas = tkinter.Canvas(
            master = self.mainWindow,
            borderwidth=1, 
            bg = "black",
            width=self._rows*self.cell_dimension,
            height=self._columns*self.cell_dimension)

        self.animate = False

        self.draw_board()


    def draw_board(self):
        cell_dimension = self.cell_dimension

        x0 = 0
        x = cell_dimension
        y0 = 0
        y = cell_dimension

        for row in self._grid:
            for cell in row:
                color_fill = 'white'
                if (cell.is_alive()):
                    color_fill = 'black'
                
                self.board_canvas.create_rectangle(x0, y0, x, y, fill=color_fill)
                x0 += cell_dimension
                x += cell_dimension

            x0 = 0
            x = cell_dimension
            y0 += cell_dimension
            y += cell_dimension
        
        self.frame = tkinter.Frame(master=self.mainWindow, bg="white")

        self.start_btn = tkinter.Button(master=self.frame, text="Evolve", width=20, height=2)
        self.start_btn.pack(side = tkinter.LEFT)
        self.start_btn.bind("<Button-1>", self.update_board)

        self.animate_btn = tkinter.Button(master=self.frame, text="Animate", width=20, height=2)
        self.animate_btn.pack(side = tkinter.LEFT)
        self.animate_btn.bind("<Button-1>", self.animate_board)

        self.stop_btn = tkinter.Button(master=self.frame, text="Stop", width=20, height=2)
        self.stop_btn.pack(side = tkinter.LEFT)
        self.stop_btn.bind("<Button-1>", self.stop_animation)

        self.frame.pack(expand = False)
        self.board_canvas.pack(fill = tkinter.BOTH, expand = False)

        self.mainWindow.resizable(False, False)
        self.mainWindow.mainloop() 
    
    
    def set_neighbours(self, own_row , own_column):
        search_min = -1
        search_max = 2

        for row in range(search_min,search_max):
            for column in range(search_min,search_max):
                neighbour_row = own_row + row
                neighbour_column = own_column + column 

                valid_neighbour = True

                if (neighbour_row) == own_row and (neighbour_column) == own_column:
                    valid_neighbour = False

                if (neighbour_row) < 0 or (neighbour_row) >= self._rows:
                    valid_neighbour = False

                if (neighbour_column) < 0 or (neighbour_column) >= self._columns:
                    valid_neighbour = False

                if valid_neighbour:
                    self._grid[own_row][own_column].neighbours.append(self._grid[neighbour_row][neighbour_column])


    def update_board(self, event):
        cell_count = 1
        new_grid = []
        for row in range(0,len(self._grid)):
            new_row = []
            for column in range(0,len(self._grid[row])):
                cell = self._grid[row][column]

                self.set_neighbours(row, column)

                living_cells = []

                for neighbour_cell in cell.neighbours:
                    if (neighbour_cell.is_alive()):
                        living_cells.append(neighbour_cell)

                new_cell = Cell()

                if (cell.is_alive()):
                    if len(living_cells) < 2 or len(living_cells) > 3:
                       self.board_canvas.itemconfig(cell_count, fill="white")
                       new_cell.set_dead()
                    else:
                        new_cell.set_alive()
                else:
                    if len(living_cells) == 3:
                       self.board_canvas.itemconfig(cell_count, fill="black")
                       new_cell.set_alive()
                    else:
                        new_cell.set_dead()

                new_row.append(new_cell)
                cell_count += 1

            new_grid.append(new_row)

        self._grid = new_grid


        if self.animate: 
            self.board_canvas.after(150, self.update_board, 0)


    def animate_board(self, event):
        self.animate = True
        self.update_board(0)


    def stop_animation(self, event):
        self.animate = False


Board(10, 10)