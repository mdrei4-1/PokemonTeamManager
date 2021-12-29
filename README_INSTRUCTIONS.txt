There shouldn't be any third-party libraries that need installed, but just in case your computer doesn't have them preinstalled, the 2 libraries I did use were sqlite3 and tkinter.

If something isn't working on your end, try checking the capitalization. The data in this program is case-sensitive.


Notes on specific data:
-If you want to use Ho-Oh either in the legality checker or the data search, the second O is lowercased. If you want to use Mr. Mime or Mime Jr, they are Mr-mime and Mime-jr.
-Note that Pichu will return a value of illegal when checking its moves if it knows Volt Tackle, and Smeargle will return illegal if it knows anything other than Sketch, due to the way the database works.

