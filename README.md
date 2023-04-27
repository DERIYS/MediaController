# MediaController
Control your PC's media through customizable hand gestures

Have you ever wanted to controll your PC's media with your hand gestures just like Tony Stark?
![tinkering-tony-stark](https://user-images.githubusercontent.com/48392479/234363659-7e270b55-8d9e-49e7-93c8-df442d2f0fd6.gif)

Then you might have found something that will fulfill your dream!

![demo](https://user-images.githubusercontent.com/48392479/234905463-317b7f7d-f7c7-46f2-ad4a-f0ae40e70c7f.gif)

With your own prefered gestures or using a default one, this program allows you to change the following aspects of your PC's media:
- Volume. There's 3 ways to change it
  1. Manually. This will set system volume to the calculated distance between your index finger and thumb as shown on a gif above.
  2. Set 50%. This will set system volume to 50% when gesture is made.
  3. Set 0%. This will set system volume to 0% when gesture is active. If you make a fully open hand just afterwards, it will return the previous volume.
- Play/Pause. This will play/pause currently/recently playing/played media. If you make a fully open hand just afterwards, it will return the previous state (if paused, playing, if playing, paused).

As soon as you open the app, a GUI will appear where you can set up custom gestures. 
In order to start changing the gesture, you need to click on one of the buttons that is responsible for a specific gesture, and close or open your fingers. 
The state of the fingers is assigned to the gesture as soon as you change it. To return the gesture to default settings - click the Reset button on the top left of the window.

Here's the demonstration of the GUI:

![demo-gif](https://user-images.githubusercontent.com/48392479/234918753-441fbfc3-97e0-4a90-b5e4-35cfabb4a05c.gif)


As soon as you ready to start, make sure your webcam is connected, click the Start button, and enjoy!


NOTE:
Due to the nature of gesture recognition, the index finger is considered closed when its tip is below its middle (see HM.py for a better understanding), so sometimes recognition of the default manual volume control gesture can be interrupted due to the fact that the finger is considered closed.
