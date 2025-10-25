Oops! Eklips just crashed;
Here's this crash log!

Quick Fix for users: N/A (Not Available)
Cause of error: bad coding skillz

Error Type: AttributeError
Error: 'VideoPlayer' object has no attribute 'rot'. Did you mean: 'root'?

FrameSummary #1:
| Filename: D:\Code\Eklips\current\src\Eklips.py
| Line: engine.scene.update(engine.delta)
| Line #: 61
FrameSummary #2:
| Filename: D:\Code\Eklips\current\src\classes\Scene.py
| Line: raise error
| Line #: 152
FrameSummary #3:
| Filename: D:\Code\Eklips\current\src\classes\Scene.py
| Line: node.update(delta)
| Line #: 147
FrameSummary #4:
| Filename: D:\Code\Eklips\current\src\classes\node\gui\media\video_player.py
| Line: self.draw()
| Line #: 119
FrameSummary #5:
| Filename: D:\Code\Eklips\current\src\classes\node\gui\media\video_player.py
| Line: self._draw_onto_screen(use_img)
| Line #: 140
FrameSummary #6:
| Filename: D:\Code\Eklips\current\src\classes\node\gui\media\video_player.py
| Line: rot                          = self.rot,
| Line #: 149

Please send this file to the developers of Eklips at https://github.com/Za9-118/Eklips/issues. 
Your feedback is important!