Oops! Eklips just crashed;
Here's this crash log!

Quick Fix for users: N/A (Not Available)
Cause of error: bad coding skillz

Error Type: TypeError
Error: get_curr_project_data() missing 1 required positional argument: 'info'

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
| Filename: D:\Code\Eklips\current\src\classes\node\gui\button.py
| Line: super().update(delta)
| Line #: 39
FrameSummary #5:
| Filename: D:\Code\Eklips\current\src\classes\node\gui\canvasitem.py
| Line: self.call_signal("_clicked")
| Line #: 136
FrameSummary #6:
| Filename: D:\Code\Eklips\current\src\classes\Object.py
| Line: return mobj()
| Line #: 66
FrameSummary #7:
| Filename: <string>
| Line: 
| Line #: 178

Please send this file to the developers of Eklips at https://github.com/Za9-118/Eklips/issues. 
Your feedback is important!