===========================================================
ZX Pokemaster 1.2 README
===========================================================

CONTENTS.

I. Introduction.
1. What is it?
2. What is it for?
II. How to use ZX Pokemaster.
III. How ZX Pokemaster works.
IV. FAQ.
V. Version history.
VI. Planned features.
VII. Contacts.

===========================================================
I. Introduction.
===========================================================

1. What is it?
ZX Pokemaster is a file management tool for ZX Spectrum. Not only it can unzip and filter out single files, it is a powerful renaming tool, which will help you name your files according to TOSEC convention.
After sorting files, a corresponding .POK file will be copied into POKES subfolder (default) or alongside the file - hence the name Pokemaster.
.POK is the format for storing cheat codes. Currently Pokemaster is aware of every Multiface cheat code mentioned on http://www.the-tipshop.co.uk/.
I've compiled the AllTipshopPokes database, which can be separately found here:
https://github.com/eklipse2009/all-tipshop-pokes
You do not have to download it, because it is already stored in Pokemaster's database.
Sorting files is very clever - it knows MD5 hashsum of nearly every ZX Spectrum file in existence.

2. What is it for?
The main reason I wrote this software is because sorting ZX Spectrum files manually is very hard. You have more than 20000 software titles, distributed in over 50000 files in different formats, under different names. 
This becomes a problem, if you want to have the most full collection of ZX Spectrum software for PC emulators, Raspberry Pi solutions or real hardware with DivMMC interface (which allows you to load software on ZX Spectrum from SD card, skipping messing with disks and tapes).
Here is the list of typical use cases of ZX Pokemaster:
	 - Assembling your collection: you can have all your games in one place;
	 - Getting rid of duplicates: alternate dumps (which are not identical files, but identical dumps of the same game), alternate formats (if you have TZX, you can leave TAP and Z80 aside or vice versa) and re-releases (original releases will be retained if available);
	 - Creating .POK files for each game you have: now that the .POK files are named according to executable emulator files they are meant for, they will be loaded automatically by emulators which support those;
	 - Sorting games by genre: now when you browse your collection thinking what to play, you won't stumble upon text adventure games, unless you specifically want to play those;
	 - Sorting games by publisher and year: assemble all Activision games, all Codemasters games, all Durell games etc. - and see how the games evolved throughout the years;
	 - Sorting games by number of players and genre: now when you have a Speccy-party and don't know what to play, you have all 2-player action games in one place;
	 - Simply unpacking zipped games and giving them meaningful names.

===========================================================
II. How to use ZX Pokemaster.
===========================================================

1. Download the games. Currently the best place to get both largest collections of ZX Spectrum software is:
http://archive.org/
Search it for "World of Spectrum mirror" and "Sinclair ZX Spectrum TOSEC". I'm not providing the exact URLs here, because those may change in the future.

2. Unpack the downloaded archive. It is OK to have individual games in .zip files, Pokemaster will unpack those itself. But if you have only one large ZIP or RAR file with the whole collection, please unpack it manually first.

3. Launch pokemaster.exe

4. Add folders where you have your games collections stored to Input paths.

5. Replace Output path with the location you want to have your files in. You might want to use Pokemaster to fill an SD card with games - and nothing can stop you.

6. If you want to include only specific formats or exclude copies of files in different formats, make sure to fill out Formats preference order field. Formats are specified by the comma-separated list of file extensions.
Example 1:
Formats preference order: tzx, tap, dsk
"Include alternate file formats" IS NOT checked.
Expected result:
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tap - this file will be copied.
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tzx - this file will be copied.
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).z80 - this file will NOT be copied (Z80 is not in format preference order).
Example 2:
Formats preference order: tzx, tap, dsk
"Include alternate file formats" IS checked.
Expected result:
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tzx - this file will be copied.
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tap - this file will NOT be copied (similar file with TZX extension exists).
Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).z80 - this file will NOT be copied (Z80 is not in format preference order).
Abadia del Crimen, La (1988)(Opera Soft)(ES)(48K).tap - this file will be copied.

7. If you want to make sure you have each and every file available, check all the the checkboxes.
For better understanding what each of them does, here is the description:
 
 - Include alternate files: all "alternate dumps" will be copied under different names. 100% identical files (identical bit by bit inside) will be represented by just one file in the output.
 
 - Include re-releases: all re-releases will be copied along with original releases if checked.
 Example (checked):
 Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tzx - this file will be copied.
 Abadia del Crimen, La (1988)(MCM Software)(ES)(128K)[re-release].tzx - this file will be copied.
 Example (unchecked):
 Abadia del Crimen, La (1988)(Opera Soft)(ES)(128K).tzx - this file will be copied.
 Abadia del Crimen, La (1988)(MCM Software)(ES)(128K)[re-release].tzx - this file will NOT be copied.
 
 - Include alternate file formats: see p. 6 (above).
 
 - Include files marked as cracked, hacked or modded: if checked, all files which have one or more of the following markers in TOSEC, will be ignored:
 [cr] - cracked
 [m] - modified
 [h] - hacked
 [f] - fixed for emulators.
 Example (checked):
 Abadia del Crimen, La (1988)(Opera Soft)(ES)[h Perestroika].trd - this file will be copied.
 Example (unchecked):
 Abadia del Crimen, La (1988)(Opera Soft)(ES)[h Perestroika].trd - this file will NOT be copied.
 
8. If you want .POK files to be placed alongside executable files instead of POKES subfolder, please uncheck "Place .POK files into POKES subfolder".

9. If you don't want to exclude games in languages you don't know, type comma-separated 2-letter ISO codes in "Languages" text box on "File filtering" tab.
Example:
en,ru,pl - will exclude games in Spanish and other languages, but will include games in English, Russian and Polish.

10. Select desired Output path structure pattern or create your own by pressing "Add pattern" button or edit an existing one using "Edit pattern" button.
Creating your own pattern should be straightforward. Either type it in, or use buttons and see how the example changes.
You can edit both folder structure and filename structure using the buttons. Just make sure the focus is on the appropriate text box - press "Tab" on keyboard or click on it with a mouse to change.
Each time you press a button, a "Slash" is added automatically. But you can replace it with another symbol, then the result will be different.

10.1. Creating output folder structure pattern.
Example:
{Publisher}\{NumberOfPlayers}
The files will be nested in two subfolders: first into publisher folder, then a folder for each possible number of players will be created.
{Publisher} - {NumberOfPlayers}
This will create several folders for each publisher in the same parent folder.

Example:
"Ariolasoft - 1P" will store 1 player games by Ariolasoft.
"Ariolasoft - 2P" will store 2 player games by Ariolasoft. This folder will be created only if at least one game exists, which matches the criteria.

10.2. Creating file name structure pattern.
By default your files will have long names, according to TOSEC convention. This is the best option, because it ensures that you will be able to easily distinguish different files between each other.

Internally, TOSEC-based filename is written like this:
{GameName} ({Year})({Publisher})({Language})({Part})({Side})[{MachineType}]{ModFlags}{Notes}

You may add/remove parameters, use different types of brackets.
For instance, you will be able to include ZXDB ID in the file name or make each file name start with release year, so your files are sorted by year inside the folder they reside in, like this:
1986 - Tujad (Ariolasoft) [ID=5448].tap
The file naming scheme would look like this:
{Year} - {GameName} - ({Publisher}) [ID={ZXDB_ID}.{Format}

11. Restricting amount of files per folders.
Sorting by letters or by year doesn't always work right, because you will have a couple of files in "1996" folder and thousands of them in "1984" folder. Or thousands in "S" folder and tens in "Y" folder.
Implementing the option to have not more than X files per folder will make it possible to make sorting files more equally. Besides I've heard of the systems which currently support not more than 256 files per folder, and it can take a while to load 2000 file names on real ZX Spectrum hardware.
The folders will be named like volumes of huge dictionaries: e. g. if first game in bundle is "Saboteur and the last is "Tujad", the folder name will be "sab-tuj".

12. Including supplementary files.
ZX Pokemaster can find and rename files which go along with your executables, but are not in its database. 
Beware that this may significantly slow down the redistribution of files.
Example:
You have a file named "TUJAD.TZX".
It has got a manual in the same folder called "TUJAD.TXT".
And it has a screenshot in the subfolder "SCRSHOT" called "TUJAD.SCR".
If "Include supplementary files" is checked, all 3 files will be copied into Output Path with these names by default:
"Tujad (1986)(Ariolasoft UK).tzx"
"Tujad (1986)(Ariolasoft UK).txt"
and
"Tujad (1986)(Ariolasoft UK).scr" in "SCRSHOT" subfolder inside Output Path.

13. Press "Sort" button and wait several minutes - this time is enough to sort 70000+ files (WoS and TOSEC dumps combined).

===========================================================
III. How ZX Pokemaster works.
===========================================================
ZX Pokemaster is bundled with SQLite database, which contains information about games, releases and files from WoS InfoSeek database, scraped from ZXDB - the fork of InfoSeek database with huge improvements, the most open and up-to-date source of information about ZX Spectrum software.
For each file from FTP, the MD5 hashsum is calculated and stored.
Then the latest version of TOSEC ZX Spectrum archive was looked through, files from TOSEC hooked to corresponding games according to a set of specific rules. Here is the rough description of the algorithm responsible for hooking TOSEC files to games and releases:
1. Get MD5 checksums of all unpacked WoS files.
2. Get MD5 checksums of all unpacked TOSEC files.
3. If TOSEC file MD5 == wos file MD5 --> attach WOS id to TOSEC file.
4. If TOSEC file starts with name of the game which is in WOS database AND there is no game with the same name --> attach that game to that TOSEC file.
6. If more than 1 game with the same name AND only one game with the same game and year found --> attach game to TOSEC file.
7. If more than one game with the same game and year found AND only one game with the same game, year and publisher found --> attach game to TOSEC file.

Regarding .POK files, those were created semi-automatically by scraping the biggest source of Multiface pokes - www.the-tipshop.co.uk - and manual checking and editing. They are contained inside the database and unpacked upon sorting files, because each .POK file should have the same name as the name of game file it is attached to, otherwise it will not be loaded automatically in emulators.

When ZX Pokemaster sorts your files, it looks into zip archives and non-archived ZX Spectrum executables and checks whether MD5 hashsum of each file is in database. If yes, then the file description is retrieved from database, if no - from the file name itself. Thus, if MD5 is known, it will recreate valid name and extension for each file, whatever naming scheme was used (even "myfavoritegame1.tap", "idontknowwhatthisgameis.tzx" etc.)

===========================================================
IV. FAQ.
===========================================================

Q: It doesn't work!
A: I've tested it thoroughly, but I cannot guarantee that ZX Pokemaster will work on your machine or meet the requirements of your use case. Please scroll down to the end of this file, there are many ways to contact me. We will figure something out and you will be the first to receive the patched version of ZX Pokemaster!

Q: How to exclude files based on criteria (e. g. copy all games except text adventures)?
A: This might be a feature for future releases, but it's far on my list - there are way too many features already planned.
Currently you can makes this semi-automatically:
1. Sort games by Genre using ZX Pokemaster.
2. Delete "Adventure - Text" folder from the output folder
3. Sort the files in output folder using ZX Pokemaster, if you were not initially planning to sort games by genre.
The same applies for other criteria: language, number of players etc.

Q: How to stop ZX Pokemaster from creating .POK files?
A: This easily could be an option, but it will never ever be. ZX Pokemaster is called that for a reason. I've devoted a huge amount of time to make AllTipshopPokes database and I REALLY want people to use it instead of entering pokes manually in emulators. I want people who use ZX Pokemaster and don't know what .POK files are at least look it up and maybe then they will take advantage of this awesome but very underused feature of many emulators and even DivIDE/DivMMC firmwares.
So if you're not interested in pokes, just ignore those files - they are less than 1MB in size combined. Or you can find and remove them by the means of your operating system.

Q: I know that this game is an Action game, but it went into "Unknown Games" folder when sorted by genre.
A: The database of ZX Pokemaster is yet to be perfected and it's my primary goal for future versions. If you know for sure what that game is, you can help me by finding it on some of ZXDB-based sides, e. g. http://spectrumcomputing.co.uk/ and send me a link to it.

Q: What does the logo of ZX Pokemaster mean?
A: This is a part of a screenshot from TUJAD by Ariolasoft - the first ZX Spectrum game I played, the game I played most, the first and only game I've beaten on ZX Spectrum without POKEs. This is also the best ZX Spectrum game of all time. It is much more known in xUSSR, than in Great Britain and Spain, probably because it was widely distributed on cassettes and sometimes even bundled with ZX Spectrum clones (mine was among them).
Alas, my British friends seem to be oblivious of this awesome game, probably because it was not well received by the media back in 1986. So this is sort of a message to them - you ought to give it a try, it's an awesome game! I dare say that it's much better than Manic Miner: better graphics, more elaborate and easier gameplay and the game is actually beatable.

===========================================================
V. Version history
===========================================================
1.2.
 - Full TOSEC-compliance achieved.
 - This release fully matches the October 31st TOSEC release.
 - Files from the following sources have been added to the database:
	http://indieretronews.com
	http://itch.io
	http://spectrum4ever.org
	http://speccy21.tk
	http://pouet.net
	http://zxaaa.net
	http://zxbg.blogspot.com
	http://www.yoursinclair.co.uk/csscgc
 - Added files with non-common extensions (.mgt, .ipf, .dck and others)
 - Proper logging added. Don't hesitate to send me logs if anything feels weird.
 - 8.3 naming scheme perfected.
 - Sorting by folders with equal amount of files improved (still not perfect).
 - Help tab added to GUI.
	

1.1. 
 - Improved filenames. Now they are more TOSEC-compliant.
 - Improved GUI interface.
 - Fixed bug: stumbling upon malformed zip file will not stop sorting other files.
 - Filter files by languages.
 - Making all files and folders CamelCased (to fit more information on screen).
 - Renaming files and folders to 8.3 standart for esxDOS.
 - Excluding x-rated games.
 - Custom naming schemes for files.
 - Restricting amount of files per folder.

1.01. Fixed major bugs:
 - Game names are restricted to 50 characters (currently hardcoded constant) to avoid 256 chars per path restriction in most operating systems.
 - Output path can now be equal to one of the input paths - this use case is now handled properly.
 - Proper error messages when output path or output folder structure pattern is entered incorrectly.
 - Corrected one of the predefined output folder structure patterns, which was broken.
 
1.0. First version.

VI. Planned features.
===========================================================

- Adding more MD5 hashes to the database. 
Currently around 3000 files in TOSEC have no corresponding entry in ZXDB and it requires manual checking of each one.

- Taking over updating TOSEC using ZX Pokemaster itself to add files from WoS FTP, which are not currently in TOSEC, to the latter, thus creating a unified source of files, so you can download a single archive and be sure you have everything that is out there on the Net.

- Deploy ZX Pokemaster for Ubuntu/Debian and OSX. 
This is relatively easy, if not the fact that I have to install those operating systems on virtual machines. I use Windows 7 exclusively for all the work I'm doing.

===========================================================
VII. Contacts.
===========================================================
You can always download the latest version of ZX Pokemaster from Sourceforge:
https://sourceforge.net/projects/zx-pokemaster/
Or visit the project's website (currently in development):
https://zx-pokemaster.sourceforge.io/
You're welcome to join the Facebook group and post bug reports.
All questions will be answered.
https://www.facebook.com/groups/zxpokemaster/
Follow me on Twitter:
https://twitter.com/lady_eklipse
You are welcome to contact me personally via email:
mailto:eklipse2009@gmail.com
or write to me on Facebook:
https://www.facebook.com/ladyeklipsegamer
or on VK.com:
https://vk.com/lady_eklipse
I speak Russian, English and German.

If you're interested in hiring me as a programmer, you're welcome to contact me via Upwork:
https://www.upwork.com/freelancers/~01621f640af26c1cb3

Sincerely yours,
Helga Iliashenko aka Lady Eklipse.
