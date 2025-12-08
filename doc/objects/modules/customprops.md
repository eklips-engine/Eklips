# classes/customprops.py

This module has the classes for all the custom properties (`export`, `GameData` (aka `engine.game`), and `Transform`) and structs for IO.

## Methods

| Name      | Type   | Exposed as      |
|-----------|--------|-----------------|
| export    | class  | export          |
| Transform | class  | Transform       |
| GameData  | struct | engine.game     |
| Mouse     | struct | engine.mouse    |
| Keyboard  | struct | engine.keyboard |

<hr>

# Classes

## `class export(default=None, type_=None, hint=None)`
Use this decorator to expose a value as a property in the editor.
This decorator is similar to the `property` decorator in Python.

The syntax to use this is:
```python
self._test = 0
@export(default=True, type_="bool", hint="bool")
def test(self):
    return self._test
@test.setter
def test(self, value):
    self._test = value
```

This decorator has arguments, and they are:

#### `Any default`
The default value to use

#### `str type_`
The name of the type that the value should be (int, str, list, bool...)

#### `str hint`
How to display this property in the editor (int, float, int/float, float/int, str, file_path/xxx, color, slider, font, bool), here is a list of hint name:

| Hint Name               | How it renders                                                          |
|-------------------------|-------------------------------------------------------------------------|
| `int`                   | A slider with an integer-only textbox.                                  |
| `int/float`, `float/int`| A slider.                                                               |
| `str`                   | A textbox.                                                              |
| `file_path/xxx`         | A box that when pressed asks for a file of type XXX.                    |
| `color`                 | A color picker.                                                         |
| `font`                  | A box that when pressed asks for a font file and shows a preview of it. |
| `bool`                  | A checkbox.                                                             |

<hr>

### Methods

#### `void export.setter(fget)`
See python `property.setter`.

#### `void export.getter(fget)`
See python `property.getter`.

<hr>

## `struct WindowProperties`
This struct is for the properties for the main window. It is exposed as `engine.game.win`.

#### `Sequence[int, int] WindowProperties.vsize`
The Window's size.

#### `Sequence[int, int, int] WindowProperties.color`
The Window's background color.

#### `bool WindowProperties.resizable`
If the Window can be resized.

#### `Sequence[int, int] WindowProperties.minsize`
The Window's minimum size.

#### `Sequence[int, int] WindowProperties.maxsize`
The Window's maximum size.

<hr>

## `struct GameData(settings="settings.json")`
This class contains information about what project the engine should run.

A project is a data directory with a `game.json` file and more data, this class
tells the engine what project to run with the help of a settings file.

#### `dict GameData.file_data`
A dictionary acquired from loading the settings JSON file.

#### `dict GameData.metadata`
A dictionary acquired from getting the `project` attribute from the root of the settings JSON file.

#### `str GameData.project_file`
The filepath of the projects `game.json` file.

#### `dict GameData.project_data`
A dictionary acquired from loading the projects `game.json` file.

#### `str GameData.project_dir`
The path of the project's data directory.

#### `str GameData.name`
The project's name.

#### `str GameData.version`
The project's version.

#### `str GameData.version_ekl`
The project's supported Eklips version (could include only major, major+minor, or the whole version).

#### `WindowProperties GameData.win`
Properties for the main Window (size, viewport color, etc...)

#### `str GameData.master_scene`
The project's main scene to be loaded after `loading_scene`.

#### `str GameData.loading_scene`
The project's first scene to be ever loaded, before `master_scene`. This can be used to initialize
any part of your project, make a Singleton, whatever.

By default, it is `root://_assets/loading.scn`, which is a scene file that shows a little animation
of the Eklips logo and its ring rotating until fading out and transitioning into the main scene.

<hr>

## `struct Mouse`
This struct class is a class that contains 3 values for mouse input.
It is recommended to call `engine.is_action_pressed()` instead of accessing
mouse button directly from here.

### `Sequence[int, int] Mouse.pos`
The cursor's position.

### `Sequence[int, int] Mouse.dpos`
How far the cursor has moved since the previous tick.

### `Sequence[bool, bool, bool] Mouse.buttons`
The list of mouse buttons (LMB, scroll wheel, RMB). Each value can be True or False if they have been pressed/held down or not.

### `list Mouse.paths`
A list of filepaths that have been dragged to any window.

<hr>

## `struct Keyboard`
This struct class is a class that contains 3 values for keyboard input.
It is recommended to call `engine.is_action_pressed()` instead of accessing input
directly from here.

### `int Keyboard.modifiers`
This value contains all the modifiers held down in the keyboard. See pyglet's documentation for more info.

### `list Keyboard.held`
This value is a list of keys that have been held down and pressed.

### `list Keyboard.pressed`
This value is a list of keys that have been pressed. This list gets emptied every frame to not contain keys that have been held down.