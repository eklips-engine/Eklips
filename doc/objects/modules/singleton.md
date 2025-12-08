# classes/singleton.py

Singleton, exposed in Eklips script files as `engine`, is the main Singleton class of Eklips. It holds everything, such as the renderer, savefile, languages, scene, etc..

It also holds some necessary functions, too, such as `is_action_pressed`, or `load_engine`.

## Methods

| Name                | Type                             |
|---------------------|----------------------------------|
| is_action_pressed   | function                         |
| is_anything_pressed | function                         |
| load_engine         | function                         |
| handle_closing      | function                         |
| clock               | pg.clock.Clock                   |
| display             | ui.Display                       |
| cvars               | cvar.CvarCollection              |
| game                | customprops.GameData             |
| loader              | resources.Loader                 |
| lang                | customprops.Language             |
| savefile            | saving.Savefile                  |
| mouse               | (struct class) customprops.Mouse |
| keyboard            | customprops.Keyboard             |
| icon                | pg.image.AbstractImage           |
| scene               | resources.Scene                  |

## Variables
### `bool running`
If the engine is running or not.

### `float delta`
The deltaTime variable.

### `float uptime`
The amount of seconds that has passed since the engine has opened.

## Constants
### `USE_GAME_PARENT = "UseFileParent"`
Used in `settings.json` to determine if the path of the project should be `game.json`'s parent folder.

### `USE_GAME_CV_DIR = "UseFileCVar"`
Used in `settings.json` to determine if the path of the project should be dictated by `game.json`.

### `BDATE = [3, 12, 2025]`
Build date.

### `MAJOR = "5"`
Major part of the version string (`5`.0A)

### `MINOR = "0"`
Minor part of the version string (5.`0`A)

### `HOTFIX = "A"`
Hotfix part of the version string (5.0`A`)

### `VERSION = "5.0A"`
Version string.

### `VERSION_FULL = "v5.0A (3/12/2025)"`
Version string with build date.

### `AUTOMATICALLY_CREATE = 1`
Used in `ui.Display.add_window` to automatically pick a Window ID.

### `DETECT = 2`
??

### `MAIN_WINDOW = 0`
Window ID of the Main Window.

### `MAIN_BATCH = 0`
Main Batch ID for a Window.

### `MAIN_VIEWPORT = 0`
Main Viewport ID for a Window.

### `DEFAULT_NAME = "Window"`
Default title for a Window.

### `VIEWPORT_EQUAL_WINDOW = 3`
Used in `ui.Display.add_window` to automatically make the Viewport's dimensions equal to the Window.

### `DEFAULT_FONT_SIZE = 12.5`
The default font size.

### `DEFAULT_FONT_NAME = "Arial"`
The default font's name.

### `USE_SCENE_TREE = 4`
Used in `engine.scene.get_nodes` to get the node paths for every Node in the scene tree.

### `MOUSE_LEFT = 1`
### `MOUSE_MIDDLE = 2`
### `MOUSE_RIGHT = 3`
ID of a Mouse button.

### `MOUSE_BUTTONS = [MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT]`
List of mouse buttons.

## Method Descriptions
### `void load_engine()`
Load every component necessary to run the engine.

### `bool is_action_pressed(entry : str)`
Returns true if action `entry` is pressed. Might return False if the entry's settings have `holdable` disabled.

### `bool is_anything_pressed()`
Returns true if any key is pressed or held down.

### `void handle_closing()`
Handles freeing every component of the engine and saving the savefile.