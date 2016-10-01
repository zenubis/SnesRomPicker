# SnesRomPicker

[Usage] snes_rom_picker.py [rom directory]

[rom directory] - directory which contains all the roms

Rom files for games sometimes has many version and they are labelled in
their filenames. Check out the link below to see what those tags are and what they mean:

https://64bitorless.wordpress.com/rom-suffix-explanations/

While different people have different criteria on what is a good rom, I have decided to 
list out what is mine and as such, is how the script will pick a rom base on it. 
(Please feel free to modify the script to suit yours.)

I am interested in both English and Japanese roms, so I have made the script
to select both an English and a Japanese roms if the game have both version. And for
each rom, the selection criteria are (in order):-
1. Verified roms '[!]'
2. Fixed roms '[f]'
3. Alternate roms '[a]'
4. Roms without any flag

Additionally, roms marked with '[b]' will be avoided.

Selected roms will be copied out to a folder call `filtered`, created at the same
folder that was passed in.

## TODO
Features that I plan to add in the future
1. Able to specify output directory.
2. Able to recongize more than 1 langage for a rom
3. Specify criteria.
