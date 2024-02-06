#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Camille Coti
# Subject to GPL v3.0

from random import randrange
import tkinter as tk
from functools import partial
from PIL import ImageTk, Image

r = -1

## Missing:
# D# G# A# wtf???

SCALES_EN = [ 'C', 'C#', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'Cb' ]
SCALES_FR = [ 'Do', 'Do #', 'Ré b', 'Ré', 'Mi b', 'Mi', 'Fa', 'Fa #', 'Sol b', 'Sol', 'La b', 'La', 'Si b', 'Si', 'Do b' ]
SCALES = SCALES_EN

SIGNATURES = { 'Cb': 'dob.png', 'C': 'do.png', 'C#': 'dod.png', 
               'Db': 'reb.png', 'D': 're.png', 
               'Eb': 'mib.png', 'E': 'mi.png',
               'F': 'fa.png', 'F#': 'fad.png',
               'Gb': 'solb.png', 'G': 'sol.png', 
               'Ab': 'lab.png', 'A': 'la.png', 
               'Bb': 'sib.png', 'B': 'si.png'
               }

IMGDIR = 'img/'

SIGBUTTON_EN = "Show signature"
SIGBUTTON_FR = "Voir l'armure"

def selectScale():
    global r
    r = randrange( len( SCALES ) )
    return SCALES[r]

def printScale( label, signature, img ):
    scale = selectScale()
    label.config( text=scale )
    if signature.get():
        refreshSignature( img )

def refreshScale( label ):
    if r < 0:
        scale = ''
    else:
        scale = SCALES[r]
    label.pack_forget()
    label.config(text=scale)
    label.pack()
    
def refreshSignature( label ):
    label.pack_forget()
    newimg = ImageTk.PhotoImage( Image.open( IMGDIR + SIGNATURES[SCALES_EN[r]] ) )
    label.configure( image = newimg )
    label.image = newimg
    label.pack( side = tk.BOTTOM )

def toggleSignature( tk, signature, label ):
    if signature.get():
        newimg = ImageTk.PhotoImage( Image.open( IMGDIR + SIGNATURES[SCALES_EN[r]] ) )
        label.configure( image = newimg )
        label.image = newimg
        label.pack( side = tk.BOTTOM )
    else:
        label.pack_forget()

def languageSel( lang, label, sigbutton, sigbutton_text ):
    global SCALES
    if lang.get() == "en":
        SCALES = SCALES_EN
        sigbutton_text.set( SIGBUTTON_EN )
    if lang.get() == "fr":
        SCALES = SCALES_FR
        sigbutton_text.set( SIGBUTTON_FR )
    sigbutton.pack()
    refreshScale( label )
    
def main():
    
    window = tk.Tk()
    signature = tk.BooleanVar( value = False )
    language = tk.StringVar( value = "en" )

    # Label that will be changed for the scale name
#    scale = tk.Label( text = "Hello, Tkinter", width=25, height=5, font=("Arial", 25) )
    scale = tk.Label( text = "", font=("Arial", 25) )

    # Key signature, not visible yet
    labelsig = tk.Label( )

    # Toggle key signature display
    sigbutton_text = tk.StringVar()
    sigbutton_text.set( SIGBUTTON_EN )
    opt_sign = tk.Checkbutton ( text = sigbutton_text.get(),
                                variable = signature,
                                textvariable = sigbutton_text,
                                onvalue = True, offvalue = False,
                                command = partial( toggleSignature, tk, signature, labelsig ) )

    # Language
    lang_en = tk.Radiobutton( text = "Français", variable = language, value = "fr",
                              command = partial( languageSel, language, scale, opt_sign, sigbutton_text ) )
    lang_fr = tk.Radiobutton( text = "English", variable = language, value = "en",
                              command = partial( languageSel, language, scale, opt_sign, sigbutton_text ) )
    
    # This is where we click
    button = tk.Button( text="Click me!",
                        width=25, height=5,
                        bg="blue", fg="yellow",
                        command = partial( printScale, scale, signature, labelsig ) )

    # Here we go
    lang_fr.pack()
    lang_en.pack()
    button.pack()
    opt_sign.pack()
    scale.pack()

    window.mainloop()
    
if __name__ == "__main__":
    main()
