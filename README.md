## Known bugs
- Music doesn't update when save is loaded.
- Game doesn't work on MacOS 10.11 (El Capitan) thanks to bad pygame.


## TODO

1. Implement options screen
- Mute music
- Resolutions


2. Impelement branching
- Transfer from one file to another based on branch
- Present choices to user


3. Visual effects?
- Rain?
- Sun glare?
- Shake?
- Make all text fade rather than just appear?


4. "Game verification"
- Check all story text files for correct formatting. Warn if anything would break the game.
- Check file resolutions to suggest if any are too small
- Check music duration to suggest if any are too short


5. Sprites
- Resize images to fit
- Face only option on side
- Three-quarters option behind textbox
- Let user configure each option


6. Implement credits screen
- Support some form of text parsing?
- Scrolling credits?


7. Handle text overflow. When a story text paragraph overflows the textbox, the program should handle the "continue" of text.
- Down arrow?
- Page flip?
- Ellipses?


8. Add font switching.
- Global font switching
- Config to associate fonts with characters!
- Be able to set narration font (no voice).


9. Update saving.
- Copy files?
- Multiple saves?