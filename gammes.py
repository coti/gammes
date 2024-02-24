#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Camille Coti
# Subject to GPL v3.0

from random import randrange
import tkinter as tk
from functools import partial
from PIL import ImageTk, Image

import webbrowser

r = -1

## Missing:
# D# G# A# wtf???

SCALES_EN = [ 'C', 'C#', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'Cb' ]
SCALES_FR = [ 'Do', 'Do #', 'Ré b', 'Ré', 'Mi b', 'Mi', 'Fa', 'Fa #', 'Sol b', 'Sol', 'La b', 'La', 'Si b', 'Si', 'Do b' ]
SCALES = SCALES_EN

SIGNATURES = { 'C': ( 's', '' ), 'G': ( 's', 'F' ), 'D': ( 's', 'FC' ), 'A': ( 's', 'FCG' ),
               'E': ( 's', 'FCGD' ), 'B': ( 's', 'FCGDA' ), 'F#': ( 's', 'FCGDAE' ),
               'C#': ( 's', 'FCGDAEB' ), 
               'F': ( 'f', 'B' ), 'Bb': ( 'f', 'BE' ), 'Eb': ( 'f', 'BEA' ), 
               'Ab': ( 'f', 'BEAD' ), 'Db': ( 'f', 'BEADG' ),  'Gb': ( 'f', 'BEADGC' ), 
               'Cb':  ( 'f', 'BEADGCF' )
              }

IMGDIR = 'img/'
TREBLECLEFFILE = "treble_empty.png"

SHARPLOC = { 'F': ( 104, 33 ),
             'C': ( 114, 51 ),
             'G': ( 124, 28 ),
             'D': ( 134, 45 ),
             'A': ( 144, 61 ),
             'E': ( 154, 40 ),
             'B': ( 165, 55 ),
            }

FLATLOC = { 'B': ( 97, 43 ),
            'E': ( 107, 26 ),
            'A': ( 117, 47 ),
            'D': ( 127, 32 ),
            'G': ( 137, 54 ),
            'C': ( 147, 37 ),
            'F': ( 157, 59 ),
}

SIGBUTTON_EN = "Show signature"
SIGBUTTON_FR = "Voir l'armure"

BACKGROUND_COLOR = "white"
BUTTON_COLOR = "#7f9ea4"
BUTTON_COLOR_ACT = "#b0898b"

#########################################################################
## Random selection
#########################################################################

def selectScale():
    global r
    r = randrange( len( SCALES ) )
    return SCALES[r]

#########################################################################
## Drawing functions
#########################################################################

def drawsharp( canvas, locations ):
    tilt = 3
    sharplen = - 14
    sharphei = 12
    sharpspacex = - 6
    sharpspacey = 8
    vertshift = -3
    lw = 3
    fillcolor = '#555'
    
    canvas.create_line( locations[0], locations[1],
                        locations[0] + sharplen + tilt, locations[1] + tilt,
                        width = lw, fill=fillcolor )
    canvas.create_line( locations[0], locations[1]+sharpspacey,
                        locations[0] + sharplen + tilt, locations[1] + sharpspacey + tilt,
                        width = lw, fill=fillcolor)

    canvas.create_line( locations[0] + vertshift - tilt/2, locations[1] - tilt,
                        locations[0] + vertshift - tilt/2, locations[1] + sharphei + tilt/2,
                        width = lw, fill=fillcolor)
    canvas.create_line( locations[0] + vertshift + sharpspacex, locations[1] - tilt,
                        locations[0] + vertshift + sharpspacex, locations[1] + sharphei + tilt/2,
                        width = lw, fill=fillcolor)

def drawflat( canvas, locations ):
    vertlen = 26
    belly = 11
    lw = 3
    fillcolor = '#555'
    
    canvas.create_line( locations[0], locations[1],
                        locations[0], locations[1] + vertlen,
                        width = lw, fill=fillcolor )

    canvas.create_line( locations[0], locations[1] + vertlen,
                        locations[0] + belly, locations[1] + vertlen - belly,
                        locations[0], locations[1] + vertlen - 6 * belly / 5,
                        smooth = 1, width = lw, fill=fillcolor )

def drawScale( canvas ):
    if r < 0: return
    sig = SIGNATURES[ SCALES_EN[ r ] ]
    for letter in sig[1]:
        if sig[0] == 'f':
            drawflat( canvas, FLATLOC[letter] )
        else:
            drawsharp( canvas, SHARPLOC[letter] )

def printScale( window, label, signature, canvas ):
    scale = selectScale()
    label.config( text=scale )
    if signature.get():
        refreshSignature( window, canvas )

def drawStaff( canvas ):
    totalheight = canvas.winfo_height()
    totalwidth = canvas.winfo_width()
    trebleclef = ImageTk.PhotoImage( Image.open( IMGDIR + TREBLECLEFFILE ) )

    SW = ( totalwidth / 2, totalheight / 2 )
    
    canvas.create_image( SW[0], SW[1], anchor = tk.CENTER, image = trebleclef )
    canvas.image = trebleclef

#########################################################################
## Functions called when a new scale is drawn
#########################################################################

def refreshScale( label ):
    if r < 0:
        scale = ''
    else:
        scale = SCALES[r]
    label.pack_forget()
    label.config(text=scale)
    label.pack()
    
def refreshSignature( window, canvas ):
    canvas.delete("all")
    window.update()
    drawStaff( canvas )
    drawScale( canvas )

#########################################################################
## Triggered when the signature option is ticked
#########################################################################

def toggleSignature( window, signature, canvas ):
    if signature.get():
        canvas.pack()
        refreshSignature( window, canvas )
    else:
        canvas.pack_forget()

#########################################################################
## Triggered when a language selection button is clicked
#########################################################################

def languageSel( lang, label, sigbutton, signature, sigbutton_text, sign ):
    global SCALES
    if lang.get() == "en":
        SCALES = SCALES_EN
        sigbutton_text.set( SIGBUTTON_EN )
    if lang.get() == "fr":
        SCALES = SCALES_FR
        sigbutton_text.set( SIGBUTTON_FR )
    sigbutton.pack()
    refreshScale( label )
    if signature.get():
        # keep the signature at the bottom
        sign.pack_forget()
        sign.pack()
    
#########################################################################
## Credits in a new window
#########################################################################

def showcredits():
    newwindow = tk.Tk()
    newwindow.configure( background = "white" )
    newwindow.title( "About this program" )
    cred = tk.Label( newwindow, text = "Credits", background = BACKGROUND_COLOR, highlightthickness = 0, font=("Arial", 25) )

    text = tk.Text( newwindow, width=35, height=6 )
    text.insert("end", "(c) Camille Coti, 2024\n\n" )
    text.insert("end", "Find the source code on GitHub:\n")
    text.insert("end", "www.github.com/coti/gammes\n")
    text.insert("end", "Released under the GPL v3 licence.\n\n")
    text.insert("end", "Now go practice.\n")
    
    htmllink = tk.Label( newwindow, text = "Visit GitHub", background = BACKGROUND_COLOR, highlightthickness = 0, font=("Arial", 18), fg="blue", cursor="hand2")
    htmllink.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://www.github.com/coti/gammes"))

    exit_button = tk.Button( newwindow, text="Exit", command=newwindow.destroy)  

    cred.pack()
    text.pack(expand=True, fill=tk.BOTH)
    htmllink.pack()
    exit_button.pack() 

#########################################################################
## Main function
#########################################################################

def main():
    
    window = tk.Tk()
    window.configure( background = "white" )
    window.title( "Random scales" )
    signature = tk.BooleanVar( value = False )
    language = tk.StringVar( value = "en" )

    # Button at the top of the window that spawns a new window to display credits.
    aboutbut = tk.Button( text="About",
                          width=25, height=1,
                          bg=BACKGROUND_COLOR, fg="black", activebackground="gray",
                          command = showcredits )


    # Label that will be changed for the scale name
    scale = tk.Label( text = "", background = BACKGROUND_COLOR, highlightthickness = 0, font=("Arial", 25) )

    # Key signature, not visible yet
    sigcanvas = tk.Canvas( background = BACKGROUND_COLOR, width=225, height=120 )

    # Toggle key signature display
    sigbutton_text = tk.StringVar()
    sigbutton_text.set( SIGBUTTON_EN )
    opt_sign = tk.Checkbutton ( text = sigbutton_text.get(),
                                variable = signature,
                                textvariable = sigbutton_text, 
                                background = BACKGROUND_COLOR, highlightthickness = 0,
                                onvalue = True, offvalue = False,
                                command = partial( toggleSignature, window, signature, sigcanvas ) )

    # Language
    lang_en = tk.Radiobutton( text = "Français", background = BACKGROUND_COLOR, highlightthickness = 0,
                              variable = language, value = "fr",
                              command = partial( languageSel, language, scale, opt_sign, signature, sigbutton_text, sigcanvas ) )
    lang_fr = tk.Radiobutton( text = "English", background = BACKGROUND_COLOR, highlightthickness = 0,
                              variable = language, value = "en",
                              command = partial( languageSel, language, scale, opt_sign, signature, sigbutton_text, sigcanvas ) )
    
    # This is where we click
    button = tk.Button( text="Click me!",
                        width=25, height=5,
                        bg=BUTTON_COLOR, fg="yellow", activebackground=BUTTON_COLOR_ACT,
                        command = partial( printScale, window, scale, signature, sigcanvas ) )

    # Here we go
    aboutbut.pack()
    lang_fr.pack()
    lang_en.pack()
    button.pack()
    opt_sign.pack()
    scale.pack()

    window.mainloop()
    
if __name__ == "__main__":
    main()
