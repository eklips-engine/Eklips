Oops! Eklips just crashed;
Here's this crash log!

Quick Fix for users: N/A (Not Available)
Cause of error: bad coding skillz

Error Type: EOFError
Error: Audio is empty. This may mean the file is corrupted. If your video has no audio track, try initializing it with no_audio=True. If it has several tracks, make sure the correct one is selected with the audio_track parameter.

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
| Line: self.vid._update()
| Line #: 117
FrameSummary #5:
| Filename: C:\Users\ZeeAy\AppData\Local\Programs\Python\Python313\Lib\site-packages\pyvidplayer2\video.py
| Line: self._audio.load(tmp)
| Line #: 630
FrameSummary #6:
| Filename: C:\Users\ZeeAy\AppData\Local\Programs\Python\Python313\Lib\site-packages\pyvidplayer2\pyaudio_handler.py
| Line: raise EOFError(
| Line #: 142

Please send this file to the developers of Eklips at https://github.com/Za9-118/Eklips/issues. 
Your feedback is important!