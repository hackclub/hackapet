# cemetery crawler
cemetery crawler is my submission for hack club's hackapet ysws. it's a small pixel-art arcade game that's set in the abandoned cemetery on a dimly lit night. my "pet" is a grim reaper present in the cemetery and the player is supposed to control him and **collect wandering souls** while **avoiding vengeful spirits.**
<br><br>
im still working on improving the game so it can reach a stage where its actually enjoyable for ppl but rn here's what the game should look like:

![image](https://github.com/user-attachments/assets/f813879e-275c-46cc-b8be-7e59e7769748)
<br>
btw, setting up circuitpython on windows was a PAIN because there were so many installations that were all over the place + running the code on the vscode terminal just didn't work and we had to use windows powershell for a few steps and the command prompt for others.

## controls 
- left – move left <br>
- right – move right <br>
- reap – swing scythe to collect souls & banish hostile spirits <br>

## gameplay
- view: third-person, side-scrolling cemetery (reaper in the center, background scrolls). 
- game setting base: the cemetery scrolls infinitely, with obstacles like tombstones and fog patches to avoid. 
- souls float across the screen—walk into them to collect. 
- hostile spirits charge at you—use the reap button to dispel them before they hit! 
- occasionally, a golden soul appears—catching it slows time or grants temporary invincibility. 
- the game speeds up as time progresses, making dodging and reaping more challenging as you move up levels.

## win/loss condition
- win: high score based on the number of souls collected.
- lose: if hit by hostile spirits too many times.

## graphics
the game has a low-res pixel art style and the pixel art for this was made with a combination of aseprite (windows) and resprite (android)
- background: dark, misty cemetery with shifting weather.
- reaper: small hooded figure seen from behind, scythe swinging in hand.
- souls: wispy blue/white; golden for power-ups.
- hostile spirits: red/purple glowing figures with sharp, jagged outlines.

## credits
used art from pinterest as inspo for the graveyard, the show [grimm](https://www.imdb.com/title/tt1830617/) for the game idea & claude ai for debugging
