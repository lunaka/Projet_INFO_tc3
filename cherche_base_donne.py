#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 23:38:22 2018

@author: macbook
"""

import sqlite3




def Cherche_Base_Donnees(L):
    
    #'''Lorsqu'on veut vérifier que l'image est dans la base de données ou pas'''
    #'''Prend en entrée L une liste de liste des objets'''

    # ouverture d'une connexion avec la base de données
    conn = sqlite3.connect('raytracing.sqlite')
    c = conn.cursor()
    
    if L == []:
        return "scene_vide"
    
    for i in range(len(L)):
        for j in range(1, len(L[0])):
            L[i][j] = float(L[i][j])
        
    
    #On trie la liste pour être sûr qu'elle est définie selon un ordre logique
    L_triee = trie(L)
    
    #On cherche le fichier dans la base de données
    c.execute('SELECT filename FROM scene WHERE serial = "{}"'.format(L_triee))
    reponse = c.fetchone()
    
    if reponse == None:
        return creer_scene(L_triee)
    (filename, )= reponse
    return filename

   

        
def trie(L):
    
    '''trie une liste de listes dans l'ordre alphabétique et/ou ordre croissant'''
    
    def split(L, M, i):
        
        # prend en entree un liste L de listes triee selon sa i-eme colonne et
        # une liste M deja entierement triee et renvoie la liste M concatenee 
        # avec la liste L entierement triee
        
        n = len(L)
        x = L[0][i]
        j = 0
        while j < n and L[j][i] == x:
            j += 1
        if j == n:
            return M + aux(L, i+1)
        else:
            return split(L[j:], M + aux(L[:j], i+1), i)
        
    def aux(L, i):
        
        #trie la liste L selon sa i-eme colonne puis appelle split dessus
        
        T = sorted(L, key = lambda colonnes: colonnes[i])
        if i == len(L[0])-1:
            return T
        else:
            return split(T, [], i)
            
        
    return aux(L, 0)



