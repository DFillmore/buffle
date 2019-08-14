# Copyright (C) 2019 David Fillmore
#
# This file is part of buffle.
#
# buffle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# buffle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as Image
from kivy.uix.widget import Widget


import blorb
import babel
import os
import sys
import io

def addScreenInfo(tree_view, screen):
    if not screen:
        return False
    root_node = tree_view.add_node(TreeViewLabel(text='Screen', is_open=False))

    t = 'Standard window width: ' + str(screen['px'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)
    t = 'Standard window height: ' + str(screen['py'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)
    
    if screen['minx'] == 0:
        t = 'Minimum window width: no limit'
    else:
        t = 'Minimum window width: ' + str(screen['minx'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)

    if screen['maxx'] == 0:
        t = 'Maximum window width: no limit'
    else:
        t = 'Maxmimum window width: ' + str(screen['maxy'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)

    if screen['minx'] == 0:
        t = 'Minimum window height: no limit'
    else:
        t = 'Minimum window height: ' + str(screen['miny'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)

    if screen['maxy'] == 0:
        t = 'Maximum window height: no limit'
    else:
        t = 'Maxmimum window height: ' + str(screen['maxy'])
    tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)






        

exec_format = {'ZCOD':'Z-code',
               'GLUL':'Glulx',
               'TAD2':'TADS 2',
               'TAD3':'TADS 3', 
               'HUGO':'Hugo', 
               'ALAN':'Alan', 
               'ADRI':'ADRIFT', 
               'LEVE':'Level 9', 
               'AGT ':'AGT', 
               'MAGS':'Magnetic Scrolls', 
               'ADVS':'AdvSys', 
               'EXEC':'Native executable' 
              }


def overviewContent():
    layout = GridLayout(cols=1)
    filenameLabel = Label(text=filename, font_size=20)
    layout.add_widget(filenameLabel)
    
    t = 'Games: ' + str(len(execindex))
    gameLabel = Label(text=t, font_size=20)
    layout.add_widget(gameLabel)

    t = 'Images: ' + str(len(picindex))
    imagesLabel = Label(text=t, font_size=20)
    layout.add_widget(imagesLabel)

    t = 'Sounds: ' + str(len(sndindex))
    soundsLabel = Label(text=t, font_size=20)
    layout.add_widget(soundsLabel)
    
    return layout

def gameContent():

    executables = {}
    for execnum in execindex:
        e = {}
        e['data'] = blorbfile.getExec(execnum)
        e['format'] = blorbfile.getExecFormat(execnum)
        executables[execnum] = e
    if len(executables) > 0:
        try:
            gameFormat = exec_format[executables[0]['format'].decode('latin-1')]
        except:
            gameFormat = "Unknown game format (" + executables[0]['format'].decode('latin-1') + ")"
    else:
        gameFormat = None
        

    iFiction = blorbfile.getMetaData()
    if iFiction:
        gameTitle = babel.getTitle(iFiction)
        gameHeadline = babel.getHeadline(iFiction)
        gameAuthor = babel.getAuthor(iFiction)
        gameDescription = babel.getDescription(iFiction)
        gameCoverPicture = babel.getCoverPicture(iFiction)
    else:
        gameTitle = None
        gameHeadline = None
        gameAuthor = None
        gameDescription = None
        gameCoverPicture = None

    if not iFiction and not gameFormat:
        return None

    
    layout = GridLayout(cols=1)

    if gameTitle:
        titleLabel = Label(text=gameTitle)
        layout.add_widget(titleLabel)

    if gameHeadline:
        headlineLabel = Label(text=gameHeadline)
        layout.add_widget(headlineLabel)

    if gameAuthor:
        authorLabel = Label(text=gameAuthor)
        layout.add_widget(authorLabel)

    if gameFormat:
        formatLabel = Label(text=gameFormat)
        layout.add_widget(formatLabel)

    #if gameDescription:
    #    descriptionLabel = Label(text=gameDescription)
    #    layout.add_widget(descriptionLabel)

    return layout

def picturesContent():
    pictures = {}
    for picnum in picindex:
        p = {}
        p['data'] = blorbfile.getPict(picnum)
        p['size'] = len(p['data'])
        p['scale'] =  blorbfile.getScaleData(picnum)
        p['format'] = blorbfile.getPictFormat(picnum)
        pictures[picnum] = p
        
    if len(pictures) == 0:
        return None

    if blorbfile.getExecFormat(0) == b'ZCOD':
        zcode = True
    else:
        zcode = False
    
    if blorbfile.findChunk(b'Reso') == 0:
        reso = False
    else:
        reso = True

    titles = ['Number', 'Format', 'Size']
    if zcode or reso:
        titles.extend(['Standard Ratio', 'Minimum Ratio', 'Maximum Ratio'])
    titles.extend(['Preview'])
    details = GridLayout(cols=len(titles), size_hint_y=None)
    details.bind(minimum_height=details.setter('height'))
    picnums = list(pictures.keys())
    picnums.sort()

    for t in titles:
        l = Label(text=t, size_hint_y=None)
        details.add_widget(l)


    for p in picnums:
        numberLabel = Label(text=str(p), size_hint_y=None)

        formatLabel = Label(text=pictures[p]['format'].decode('latin-1'), size_hint_y=None)
        
        sizeLabel = Label(text=str(pictures[p]['size']), size_hint_y=None)

        details.add_widget(numberLabel)
        details.add_widget(formatLabel)
        details.add_widget(sizeLabel)        

        if zcode or reso:
            stdrat = str(pictures[p]['scale']['ratnum']) + '/' + str(pictures[p]['scale']['ratden'])
            stdratLabel = Label(text=stdrat, size_hint_y=None)

            minrat = str(pictures[p]['scale']['minnum']) + '/' + str(pictures[p]['scale']['minden'])
            minratLabel = Label(text=minrat, size_hint_y=None)

            maxrat = str(pictures[p]['scale']['maxnum']) + '/' + str(pictures[p]['scale']['maxden'])
            maxratLabel = Label(text=maxrat, size_hint_y=None)
        
            details.add_widget(stdratLabel)
            details.add_widget(minratLabel)
            details.add_widget(maxratLabel)

        previewImage = getImage(p)
        details.add_widget(previewImage)
        
    return details

def getImage(imageNum):
    data = io.BytesIO(blorbfile.getPict(imageNum))
    ex = blorbfile.getPictFormat(imageNum).decode('latin-1').strip().lower()
    if ex != 'rect':
        cimage=CoreImage(data, ext=ex).texture
        image = Image(texture=cimage)
    else:
        r = blorb.rect(data.read())
        image = Image(texture=Rectangle(size=(r.getWidth(), r.getHeight())).texture)
    return image

def soundsContent():
    sounds = {}
    for sndnum in sndindex:
        s = {}
        s['data'] = blorbfile.getSnd(sndnum)
        s['format'] = blorbfile.getSndFormat(sndnum)
        s['type'] = blorbfile.getSndType(sndnum)
        sounds[sndnum] = s
    
    if len(sounds) == 0:
        return None

    if blorbfile.getExecFormat(0) == b'ZCOD':
        zcode = True
    else:
        zcode = False
    
    titles = ['Sound Number', 'Format']
    if zcode:
        title.extend(['Type'])
    layout = GridLayout(cols=len(titles), size_hint_y=None)
    layout.bind(minimum_height=layout.setter('height'))
    sndnums = list(sounds.keys())
    sndnums.sort()

    for t in titles:
        l = Label(text=t, size_hint_y=None)
        layout.add_widget(l)


    for s in sndnums:
        numberLabel = Label(text=str(s), size_hint_y=None)

        formatLabel = Label(text=sounds[s]['format'].decode('latin-1'), size_hint_y=None)
        
        layout.add_widget(numberLabel)
        layout.add_widget(formatLabel)

        if zcode:
            if sounds[s]['type'] == 0:
                sndtype = 'Sample'
            else:
                sndtype = 'Music'
            typeLabel = Label(text=sndtype, size_hint_y=None)
        
            layout.add_widget(typeLabel)

    return layout

class MainApp(App):

    def build(self):
        tp = TabbedPanel(do_default_tab=False)
        overviewTab = TabbedPanelHeader(text='Overview')
        gameTab = TabbedPanelHeader(text='Game')
        imageTab = TabbedPanelHeader(text='Images')
        soundTab = TabbedPanelHeader(text='Sounds')
        tp.add_widget(overviewTab)
        
        overviewTab.content = overviewContent()

        c = gameContent()
        if c:
            tp.add_widget(gameTab)
            gameTab.content = c

        c = picturesContent()
        if c:
            tp.add_widget(imageTab)
            scroll = ScrollView(size_hint=(1, None), size=(tp.width, Window.height - tp.height), bar_width=10, scroll_type=['bars', 'content'])
            scroll.add_widget(c)
            imageTab.content = scroll

        c = soundsContent()
        if c:
            tp.add_widget(soundTab)
            scroll = ScrollView(size_hint=(1, None), size=(tp.width, Window.height - tp.height), bar_width=10, scroll_type=['bars', 'content'])
            scroll.add_widget(c)
            soundTab.content = scroll


        #layout.bind(size=self._update_rect, pos=self._update_rect)


        #addScreenInfo(tree, screen)
        #addPictures(tree, pictures)
        #addSounds(tree, sounds)
        #addExecutables(tree, executables)
       

        #root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), bar_width=10, scroll_type=['bars', 'content'])
        #root.add_widget(tree)

        #gameTab.add_widget(root)

        return tp

import sys, getopt

def parameters(argv):
    if len(argv) != 2:
        print('usage: buffle.py <blorbfile>')
        sys.exit()
    return argv[1]
    
if __name__ == '__main__':
    filename = parameters(sys.argv)
    blorbfile = blorb.Blorb(filename)

    #chunks = blorbfile.listChunks()

    picindex = blorbfile.resindex[b'Pict']
    sndindex = blorbfile.resindex[b'Snd ']
    execindex = blorbfile.resindex[b'Exec']
    
    MainApp().run()











