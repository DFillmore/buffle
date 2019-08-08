# Copyright (C) 2001 - 2019 David Fillmore
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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


import blorb

#filename = 'arthur.blb'
#filename = 'journey.blb'
#filename = 'shogun.blb'
filename = 'zorkzero.blb'


blorbfile = blorb.Blorb(filename)

chunks = blorbfile.listChunks()

pictures = blorbfile.resindex[b'Pict']
sounds = blorbfile.resindex[b'Snd ']
executables = blorbfile.resindex[b'Exec']

screen = dict(zip(('px', 'py', 'minx', 'miny', 'maxx', 'maxy'), blorbfile.getWinSizes()))

pictures = {}
for picnum in blorbfile.resindex[b'Pict']:
    p = {}
    p['data'] = blorbfile.getPict(picnum)
    p['size'] = len(p['data'])
    p['scale'] =  blorbfile.getScaleData(picnum)
    pictures[picnum] = p



#print('PICTURES!')
#for a in pictures:
#    p = pictures[a]
#    print('Picture', a)
#    print(' - Size:', p['size'])
#    print(' - Scale')
#    print('   - numerator of standard ratio:', p['scale']['ratnum'])
#    print('   - numerator of standard ratio:', p['scale']['ratnum'])
#    print('   - denominator of standard ratio:', p['scale']['ratden'])
#    print('   - numerator of minimum ratio:', p['scale']['minnum'])
#    print('   - denominator of minimum ratio:', p['scale']['minden'])
#    print('   - numerator of maximum ratio:', p['scale']['maxnum'])
#    print('   - denominator of maximum ratio:', p['scale']['maxden'])

#print('Picture\tSize\tnumerator of standard ratio\tnumerator of standard ratio\tdenominator of standard ratio\tnumerator of minimum ratio\tdenominator of minimum ratio\tnumerator of maximum ratio\tdenominator of maximum ratio')
#for a in pictures:
#    p = pictures[a]
#    
#    print(str(a) + '\t' + str(p['size']) + '\t' + str(p['scale']['ratnum']) + '\t' + str(p['scale']['ratnum']) + '\t' + str(p['scale']['ratden']) + '\t' + str(p['scale']['minnum']) + '\t' + str(p['scale']['minden']) + '\t' + str(p['scale']['maxnum']) + '\t' + str(p['scale']['maxden']))



#print('SOUNDS!')
#for a in sounds:
#    print(a)

#print('GAMES!')
#for a in executables:
 #   print(a)




def addScreenInfo(tree_view, screen):
    root_node = tree_view.add_node(TreeViewLabel(text='Screen', is_open=False))
    for a in screen:
        t = str(a) + ': ' + str(screen[a])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), root_node)

def addPictures(tree_view, pictures):
    root_node = tree_view.add_node(TreeViewLabel(text='Pictures', is_open=True))
    for a in pictures: # data, size, scale
        t = 'Image Number: ' + str(a)
        p = tree_view.add_node(TreeViewLabel(text=t, is_open=False, on_node_expand=showpicture), root_node)
        #p.bind(on_node_expand=lambda instance: showpicture(pictures[a]['data']))
        picsize = len(pictures[a]['data'])
        
        t = 'Size: ' +str(picsize) + ' bytes'
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), p)
        
        r = tree_view.add_node(TreeViewLabel(text='Scale Information', is_open=False), p)
        t = 'numerator of standard ratio: ' + str(pictures[a]['scale']['ratnum'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)
        t = 'denominator of standard ratio: ' + str(pictures[a]['scale']['ratden'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)
        t = 'numerator of minimum ratio: ' + str(pictures[a]['scale']['minnum'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)
        t = 'denominator of minimum ratio:: ' + str(pictures[a]['scale']['minden'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)
        t = 'numerator of maximum ratio ' + str(pictures[a]['scale']['maxnum'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)
        t = 'denominator of maximum ratio: ' + str(pictures[a]['scale']['maxden'])
        tree_view.add_node(TreeViewLabel(text=t, is_open=False), r)



def showpicture():
    #im = CoreImage(data, ext="png")
    pass




class MainApp(App):

    def build(self):
        

        #layout.bind(size=self._update_rect, pos=self._update_rect)

        tree = TreeView(root_options=dict(text=filename),
                        hide_root=False,
                        indent_level=4, size_hint_y=None)
        tree.bind(minimum_height = tree.setter('height'))
        addScreenInfo(tree, screen)
        addPictures(tree, pictures)
        #layout.add_widget(tree)
       

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), bar_width=10, scroll_type=['bars', 'content'])
        root.add_widget(tree)
        layout=GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.add_widget

        return root

if __name__ == '__main__':
    MainApp().run()










# ZorkZero.blb
# - screen
#   - standard width: 600
#   - standard height: 400
#   - minimum width: no limit
#   - maxmimum width: no limit
#   - minimum height: no limit
#   - maximum height: no limit
# - images
#   - 1 
#   - 2
#   - 3
#     - 69kb
#     - scale: blah blah blah
#     - format: PNG
# - sounds
#   - 3
#     - 58463kb
#     - type: music
#     - format: Ogg Vorbis