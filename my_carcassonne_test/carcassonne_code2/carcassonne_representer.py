import os
from tkinter import *
from PIL import ImageTk, Image

import carcassonne_code2
from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.objects.side import Side
from carcassonne_code2.objects.tile import Tile

x_mouse_coords = -1000
y_mouse_coords = -1000
next_tile_turns = 0
canvas_width_change = 0
canvas_height_change = 0 
canvas_width = 1536
canvas_height = 742 #864 801
meeple_tipe_action = ()


class CarcassonneRepresenter:

    meeple_icons = {
        MeepleType.NORMAL: ["blue_meeple.png", "red_meeple.png", "black_meeple.png", "yellow_meeple.png", "green_meeple.png", "pink_meeple.png"],
        }
    tile_size = 60
    meeple_size = 15

    meeple_position_offsets = {
        Side.TOP: (tile_size / 2, (meeple_size / 2) + 3),
        Side.RIGHT: (tile_size - (meeple_size / 2) - 3, tile_size / 2),
        Side.BOTTOM: (tile_size / 2, tile_size - (meeple_size / 2) - 3),
        Side.LEFT: ((meeple_size / 2) + 3, tile_size / 2),
        Side.CENTER: (tile_size / 2, tile_size / 2),
        Side.TOP_LEFT: (tile_size / 4, (meeple_size / 2) + 3),
        Side.TOP_RIGHT: ((tile_size / 4) * 3, (meeple_size / 2) + 3),
        Side.BOTTOM_LEFT: (tile_size / 4, tile_size - (meeple_size / 2) - 3),
        Side.BOTTOM_RIGHT: ((tile_size / 4) * 3, tile_size - (meeple_size / 2) - 3)
    }

    def __init__(self):

        def toggle_fs(dummy=None):
            state = False if root.attributes('-fullscreen') else True
            root.attributes('-fullscreen', state)
            if not state:
                root.geometry('300x300+100+100')

        def getorigin(eventorigin):
            global x_mouse_coords, y_mouse_coords
            x_mouse_coords = eventorigin.x
            y_mouse_coords = eventorigin.y

        def get_turns(dummy=None):
            global next_tile_turns
            next_tile_turns = (next_tile_turns + 1) % 4

        def configure_scroll_region(event):
            self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        def scroll_left(event):
            global canvas_width_change
            canvas_width_change -= canvas_width / 10 
            self.canvas.xview_scroll(-1, "units")

        def scroll_right(event):
            global canvas_width_change
            canvas_width_change += canvas_width / 10 
            self.canvas.xview_scroll(1, "units")
      
        def scroll_up(event):
            global canvas_height_change
            canvas_height_change -= canvas_height / 10 
            self.canvas.yview_scroll(-1, "units")
    
        def scroll_down(event):
            global canvas_height_change
            canvas_height_change += canvas_height / 10 
            self.canvas.yview_scroll(1, "units")
            
        def worker_empty(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = ('empty')

        def worker_left(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.NORMAL, Side.LEFT)

        def worker_right(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.NORMAL, Side.RIGHT)

        def worker_top(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.NORMAL, Side.TOP)
    
        def worker_bottom(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.NORMAL, Side.BOTTOM)

        def worker_centr(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.NORMAL, Side.CENTER)

        def farmer_top_left(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.FARMER, Side.TOP_LEFT)

        def farmer_bottom_left(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.FARMER, Side.BOTTOM_LEFT)

        def farmer_top_right(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.FARMER, Side.TOP_RIGHT)

        def farmer_bottom_right(dummy=None):
            global meeple_tipe_action
            meeple_tipe_action = (MeepleType.FARMER, Side.BOTTOM_RIGHT)
    

        root = Tk()
        root.configure(bg='#CDB79E')
        
        self.canvas = Canvas(root, bg = 'white', scrollregion=(0, 0, 70000, 7000))
        self.canvas.pack(fill = BOTH, expand = True)
           
        self.tile_frame = Frame(root, bg='#CDB79E')
        self.tile_frame.pack()

        worker_frame = Frame(root, relief=RIDGE, bg='#CDB79E')
        worker_frame.pack(side=BOTTOM)
        Button(worker_frame, text='Робітник: Ліво', bg='#E3CF57', command=worker_left).pack(side=LEFT, padx=5, pady=5)
        Button(worker_frame, text='Робітник: Право', bg='#E3CF57', command=worker_right).pack(side=LEFT, padx=5, pady=5)
        Button(worker_frame, text='Робітник: Низ', bg='#E3CF57', command=worker_bottom).pack(side=LEFT, padx=5, pady=5)
        Button(worker_frame, text='Робітник: Верх', bg='#E3CF57', command=worker_top).pack(side=LEFT, padx=5, pady=5)
        Button(worker_frame, text='Робітник: Центр', bg='#E3CF57', command=worker_centr).pack(side=LEFT, padx=5, pady=5)
        Button(worker_frame, text='Пропустити хід', bg='#E3CF57', command=worker_empty).pack(side=LEFT, padx=5, pady=5)
    

        farmer_frame = Frame(root, relief=RIDGE, bg='#CDB79E')
        farmer_frame.pack(side=BOTTOM) 
        Button(farmer_frame, text='Фермер: Ліво низ', bg='#7FFFD4', command=farmer_bottom_left).pack(side=LEFT, padx=5, pady=5)
        Button(farmer_frame, text='Фермер: Ліво верх', bg='#7FFFD4', command=farmer_top_left).pack(side=LEFT, padx=5, pady=5)
        Button(farmer_frame, text='Фермер: Право низ', bg='#7FFFD4', command=farmer_bottom_right).pack(side=LEFT, padx=5, pady=5)
        Button(farmer_frame, text='Фермер: Право верх', bg='#7FFFD4', command=farmer_top_right).pack(side=LEFT, padx=5, pady=5)

        root.state('zoomed')
        root.attributes('-fullscreen', True)

        root.bind('<Escape>', toggle_fs)
        root.bind('<Button-3>', getorigin)
        root.bind('<space>', get_turns)
        self.canvas.bind("<Configure>", configure_scroll_region)
        root.bind("<Left>",  scroll_left)
        root.bind("<Right>", scroll_right)
        root.bind("<Up>",    scroll_up)
        root.bind("<Down>",  scroll_down)

        self.images_path = os.path.join(carcassonne_code2.__path__[0], 'resources', 'images')
        self.meeple_image_refs = {}
        self.tile_image_refs = {}

    
    def draw_game_state(self, game_state: CarcassonneGameState):
        self.canvas.delete('all')

        for widget in self.tile_frame.winfo_children():
            widget.destroy()

        maket = ImageTk.PhotoImage(Image.open('carcassonne_code2\\resources\images\makets\carcassonne_maket_2.jpg')) 
        self.canvas.create_image( 0, 0, image = maket, anchor = "nw") 
    
        for row_index, row in enumerate(game_state.board):
            for column_index, tile in enumerate(row):
                tile: Tile
                if tile is not None:
                    self.__draw_tile(column_index, row_index, tile)

        for player, placed_meeples in enumerate(game_state.placed_meeples):
            meeple_position: MeeplePosition
            for meeple_position in placed_meeples:
                self.__draw_meeple(player, meeple_position)

        if game_state.next_tile is not None:
            self.__draw_next_tile(game_state, game_state.next_tile)
        else:
            Label(self.tile_frame, text=f'Player 1 : Player2 >> SCORES {game_state.scores[0]} : {game_state.scores[1]} >> MEEPLE {game_state.meeples[0]} : {game_state.meeples[1]} >> DECK {len(game_state.deck)}', 
                              font=('Times New Roman', 14, 'bold'), bg='#CDB79E', padx=5).pack(side=LEFT)

        self.tile_frame.update()
        self.canvas.update()
 
    def __draw_next_tile(self, state: CarcassonneGameState, tile):
        image_filename = tile.image
        reference = f"{image_filename}_{str(next_tile_turns)}"
        if reference in self.tile_image_refs:
            photo_image = self.tile_image_refs[reference]
        else:
            abs_file_path = os.path.join(self.images_path, image_filename)
            image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size), Image.ANTIALIAS).rotate(
                -90 * next_tile_turns)
            image = self.__flattenAlpha(image)
            height = image.height
            width = image.width
            crop_width = max(0, width - height) / 2
            crop_height = max(0, height - width) / 2
            image.crop((crop_width, crop_height, crop_width, crop_height))
            photo_image = ImageTk.PhotoImage(image)
        self.tile_image_refs[f"{image_filename}_{str(next_tile_turns)}"] = photo_image

        Label(self.tile_frame, text=f'Player 1 : Player2 >> SCORES {state.scores[0]} : {state.scores[1]} >> MEEPLE {state.meeples[0]} : {state.meeples[1]} >> DECK {len(state.deck)}', 
                              font=('Times New Roman', 14, 'bold'), bg='#CDB79E', padx=5).pack(side=LEFT)
        Label(self.tile_frame, image = photo_image, bg='#CDB79E') .pack(side=LEFT)

    def __draw_meeple(self, player_index: int, meeple_position: MeeplePosition):
        image = self.__get_meeple_image(player=player_index, meeple_type=meeple_position.meeple_type)

        if meeple_position.meeple_type == MeepleType.BIG:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size + self.big_meeple_position_offsets[meeple_position.coordinate_with_side.side][1]
        else:
            x = meeple_position.coordinate_with_side.coordinate.column * self.tile_size + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][0]
            y = meeple_position.coordinate_with_side.coordinate.row * self.tile_size + self.meeple_position_offsets[meeple_position.coordinate_with_side.side][1]

        self.canvas.create_image(
            x,
            y,
            anchor=CENTER,
            image=image
        )

    def __flattenAlpha(self, img):
        alpha = img.split()[-1]  # Pull off the alpha layer
        ab = alpha.tobytes()  # Original 8-bit alpha

        checked = []  # Create a new array to store the cleaned up alpha layer bytes

        # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
        transparent = 50  # change to suit your tolerance for what is and is not transparent

        p = 0
        for pixel in range(0, len(ab)):
            if ab[pixel] < transparent:
                checked.append(0)  # Transparent
            else:
                checked.append(255)  # Opaque
            p += 1

        mask = Image.frombytes('L', img.size, bytes(checked))

        img.putalpha(mask)

        return img

    def __draw_tile(self, column_index, row_index, tile):
        image_filename = tile.image
        reference = f"{image_filename}_{str(tile.turns)}"
        if reference in self.tile_image_refs:
            photo_image = self.tile_image_refs[reference]
        else:
            abs_file_path = os.path.join(self.images_path, image_filename)
            image = Image.open(abs_file_path).resize((self.tile_size, self.tile_size), Image.ANTIALIAS).rotate(
                -90 * tile.turns)
            image = self.__flattenAlpha(image)
            height = image.height
            width = image.width
            crop_width = max(0, width - height) / 2
            crop_height = max(0, height - width) / 2
            image.crop((crop_width, crop_height, crop_width, crop_height))
            photo_image = ImageTk.PhotoImage(image)
        self.tile_image_refs[f"{image_filename}_{str(tile.turns)}"] = photo_image
        self.canvas.create_image(column_index * self.tile_size, row_index * self.tile_size, anchor=NW, image=photo_image)

    def __get_meeple_image(self, player: int, meeple_type: MeepleType):
        reference = f"{str(player)}_{str(meeple_type)}"

        if reference in self.meeple_image_refs:
            return self.meeple_image_refs[reference]

        icon_type = MeepleType.NORMAL
        if meeple_type == MeepleType.ABBOT:
            icon_type = meeple_type

        image_filename = self.meeple_icons[icon_type][player]
        abs_file_path = os.path.join(self.images_path, image_filename)

        photo_image = None
        if meeple_type == MeepleType.NORMAL or meeple_type == MeepleType.ABBOT:
            image = Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS)
            image = self.__flattenAlpha(image)
            photo_image = ImageTk.PhotoImage(image)
        elif meeple_type == MeepleType.BIG:
            image = Image.open(abs_file_path).resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS)
            image = self.__flattenAlpha(image)
            photo_image = ImageTk.PhotoImage(image)
        elif meeple_type == MeepleType.FARMER:
            image = Image.open(abs_file_path).resize((self.meeple_size, self.meeple_size), Image.ANTIALIAS).rotate(-90)
            image = self.__flattenAlpha(image)
            photo_image = ImageTk.PhotoImage(image)
        elif meeple_type == MeepleType.BIG_FARMER:
            image = Image.open(abs_file_path).resize((self.big_meeple_size, self.big_meeple_size), Image.ANTIALIAS).rotate(-90)
            image = self.__flattenAlpha(image)
            photo_image = ImageTk.PhotoImage(image)
        else:
            print(f"ERROR LOADING IMAGE {abs_file_path}!")
            exit(1)

        self.meeple_image_refs[f"{str(player)}_{str(meeple_type)}"] = photo_image
        return photo_image