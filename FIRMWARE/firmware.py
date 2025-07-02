import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.layers import Layers
from kmk.extensions.display import Display, SSD1306, TextEntry, ImageEntry

i2c_bus = busio.I2C(board.GP21, board.GP20)
display_driver = SSD1306(
    i2c=i2c_bus,
    # Optional device_addres argument. Default is 0x3C.
    # device_address=0x3C,
)

display = Display(
    display=display_driver,
    entries=[
        TextEntry(text='DM Pad:', x=0, y=16, y_anchor='T'),
        TextEntry(text='AMBIENCE', x=0, y=32, y_anchor='B', layer=0),
        TextEntry(text='COMBAT', x=0, y=32, y_anchor='B', layer=1),
        TextEntry(text='UTILITY', x=0, y=32, y_anchor='B', layer=2),
    ],
    height=64,
    dim_time=10,
    dim_target=0.2,
    off_time=1200,
    brightness=1,
)

keyboard = KMKKeyboard()
layers = Layers()
encoder_handler = EncoderHandler()
keyboard.modules.append(layers)
keyboard.modules.append(encoder_handler)
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(display)

# Define matrix pins based on the schematic, using GP pins
keyboard.col_pins = (board.GP0, board.GP1, board.GP2)  # COLUMN_1, COLUMN_2, COLUMN_3
keyboard.row_pins = (board.GP3, board.GP4, board.GP5)  # ROW_A, ROW_B, ROW_C
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# D&D Dungeon Master Macros

# Ambience and Lighting Controls
TAVERN_AMBIENCE = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("https://mynoise.net/NoiseMachines/tavern.php"), KC.ENTER))
FOREST_AMBIENCE = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("https://mynoise.net/NoiseMachines/darkWorld.php"), KC.ENTER))
DUNGEON_AMBIENCE = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("https://mynoise.net/NoiseMachines/caveNoiseGenerator.php"), KC.ENTER))

# Combat Sound Effects
SWORD_CLASH = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("freesound.org/people/Hybrid_V/sounds/321215/"), KC.ENTER))
SPELL_CAST = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("freesound.org/people/qubodup/sounds/219568/"), KC.ENTER))
DRAGON_ROAR = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("freesound.org/people/Marianne_Gagnon/sounds/131961/"), KC.ENTER))

# Quick Utility Macros
ROLL_D20 = simple_key_sequence((KC.COPY("/roll 1d20"), KC.ENTER))
INITIATIVE_TRACKER = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("https://www.improved-initiative.com/"), KC.ENTER))
DND_BEYOND = simple_key_sequence((KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(100), KC.COPY("https://www.dndbeyond.com/"), KC.ENTER))

# Lighting Controls (assuming smart lights or OBS scenes)
DIM_LIGHTS = simple_key_sequence((KC.LALT(KC.F1)))  # OBS Scene hotkey
BRIGHT_LIGHTS = simple_key_sequence((KC.LALT(KC.F2)))  # OBS Scene hotkey
RED_COMBAT_LIGHTS = simple_key_sequence((KC.LALT(KC.F3)))  # OBS Scene hotkey

# Define multi-layer keymap for different DM functions
keyboard.keymap = [
    # Layer 0: Ambience & Environment
    [
        TAVERN_AMBIENCE,    FOREST_AMBIENCE,     DUNGEON_AMBIENCE,
        DIM_LIGHTS,         BRIGHT_LIGHTS,       KC.MO(1),  # Hold for Layer 1
        KC.MUTE,            KC.VOLD,             KC.TO(2)   # To Layer 2
    ],
    # Layer 1: Combat & Effects
    [
        SWORD_CLASH,        SPELL_CAST,          DRAGON_ROAR,
        RED_COMBAT_LIGHTS,  ROLL_D20,            KC.TRNS,   # Transparent (back to base)
        KC.MEDIA_PLAY_PAUSE, KC.MEDIA_PREV_TRACK, KC.TO(0)   # Back to Layer 0
    ],
    # Layer 2: Utilities & Tools
    [
        INITIATIVE_TRACKER, DND_BEYOND,          KC.LGUI(KC.L),  # Lock screen
        KC.LCTL(KC.T),      KC.LCTL(KC.W),       KC.LCTL(KC.LSHIFT(KC.T)),  # Browser tabs
        KC.LALT(KC.TAB),    KC.LCTL(KC.C),       KC.TO(0)   # Back to Layer 0
    ]
]

# Configure encoder for volume/music control
encoder_handler.pins = ((board.GP6, board.GP7, board.GP8),)  # ENCA, ENCB, ENC_SWITCH
# Encoder map - volume control and mute
encoder_handler.map = [(
    (KC.VOLU, KC.VOLD),  # Rotate for volume
    KC.MUTE              # Press to mute
)]

if __name__ == '__main__':
    keyboard.go()