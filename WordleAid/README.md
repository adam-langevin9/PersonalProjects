# WordleAid

A simple yet effective terminal tool to help your average wordle player. No AI involve; program simply narrows down the possible answers given your guesses and received hints.

## Example Run
```
$ python3.10 /WordleHelper.py
Start by entering your first 5 letter guess. 
Then enter the corresponding hints you receive using the following key 
(g = green, y = yellow,   = wrong, guess = re-enter guess). 
The system will show you a list of possible words given your guess and hints. 
Repeat this process to get closser to the mystery word. 
Be smart about your choices because you only have 6 tries.
Good Starter words are slice, tried, or crane
Enter your guess: slice
Enter your hints: g  yg
scope   score   scone   scuse   scare   scene
Enter your guess: scope
Enter your hints: gg  g
scuse   scare   scene
Enter your guess: scare
Enter your hints: ggggg
scare
Well Done!
```

