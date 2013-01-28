PySLGalMaker
============

A light-weighted python tool to make youself's Galgame

The Chinese help_doc is README file.You can read it.

Depending on python(2.6.5) and pygame.The aim of the tool is made it easer to who want to make himself's galgame.

In my example code,both sounds and pictrues are Infringement.If you think it was not good behavior,PM me and I were deleting it.

This tool can run on both Windows and Linux.

I define some gammers,so you can write you script just like complete the blank.The script is script.sanae.You can change the content,Never rename it and Obey the Gammers,Please!

But,in fact,I'm not complete it.Some import functions have not added.I will update it.

Term:
  I use the term "frame" to refer each time things on you game_screen.What content sound,background,text maybe buttons.

Gammers

  you can also read the script.sanae ---- author.
  
  0.FRAME
  
  we split two frame by whiteline
  
  1.INDEX
  
  which is the frame's index,
  always number,be careful,you must write index one by one,no jump----except choice-button
  
  2.BACKGROUND
  
  referring the background of you game_screen
  always like this:
  [background = 'xxxx.xxx']
  xxxx.xxx is a picture's name,always in BG folder.
  
  3.BGM
  
  the bgm of the game
  [BGM = 'xxxx.xxx']
  xxxx.xxx is a sound's name.In windows,the format are .mp3 or .wav.In Linux are .ogg or .wav
  
  4.TEXT
  
  the text show on the screen
  gammer like this:
  <xxxxxx>
  Be care.you can write it like this:
  <John:What's a good day!>
  or
  <What's good day!>
  program will split the sentence by :,and pre-half will show on the first line,post-half start showing on second line.
  
  5.Choice_Butthons
  you can write it like this:
  [choice]
  xxxx->xxx
  xxxx->xxx
  [/choice]
  the xxxx is the label show on the button,and xxx is the index refers a special frame.
  
  That's all.
  Show some frame for examply.
  
  0
  [background = 'sanae.jpg']
  [BGM = 'uuz.wav']
  <I want to sleep>
  
  1
  [background = 'koinamaid.png']
  <Sanae San wa dai su ki>
  
  2
  [choices]
  choose munohana->50
  choose aoi->60
  [/choices]
  
