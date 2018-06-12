#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 08:25:07 2018

@author: macbook
"""

import sqlite3

conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS scene")
c.execute("CREATE TABLE scene ( \
  id INTEGER PRIMARY KEY, \
  name TEXT, \
  serial TEXT, \
  width INTEGER, \
  height INTEGER,\
  ptime REAL)")

conn.commit()






from raytracer import *

class Pyramid(ComposedArtifact):

    # base est un Polygone
    # S est un vec3 correspondant au sommet
    def __init__(self, base, S, *args, **kwargs):

        # La pyramide est composée de n+1 facettes
        npoints = len(base.vertices)
        ComposedArtifact.__init__(self, npoints+1, *args, **kwargs)

        # La première facette de la pyramide est sa base
        self[0] = base
        
        # Si la base est un Polygon2 on dispose déjà des coordonnées 3D
        # des sommets, sinon on les calcule
        vertices3D = base.vertices3D if hasattr(base,'vertices3D') else \
          [base.P + base.U * v[0] + base.V * v[1] for v in base.vertices]

        # Chacune des facettes s'appuie sur le sommet et un segment de la base
        for n in range(npoints):
            P1 = S
            P2 = (vertices3D[n-1] if n > 0 else vertices3D[npoints-1])
            P3 = vertices3D[n]
            self[n+1] = Polygon2((P1,P2,P3), -base.ns, **self.kwargs(n))

        self.vertices3D = [*vertices3D, S]
        self.base = base
        self.S = S

    @classmethod
    def keys(cls):
        return ['base', 'S'] + Artifact.keys()

    def getattr(self,k):
        return getattr(self,k) if k in self.keys() else ComposedArtifact.getattr(self,k)
scene = Scene('pyramid', 0, 1)
scene.append(LightSource(vec3(-1., 2, 0), 1))

S = vec3(0,0.5,0.5)
vertices = [vec3(-0.5,0,0), vec3(0.5,0,0), vec3(0.5,0,1), vec3(-0.5,0,1)]
base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0), mirror=0, specular=0)

scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
scene.append(Pyramid(base, S, diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0))

scene.initialize(E=vec3(0,2,-10)).trace().save_image()
pass


# ouverture d'une connexion avec la base de données
conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

# liste des valeurs enregistrées, dans l'ordre des champs de la table scene
# N.B. on s'attend ici à disposer d'une scène dans la variable "scene" 
data = [
    scene.name,
    scene.serialize(),
    scene.w,
    scene.h
]

# enregistrement des informations par soumission d'une requête SQL INSERT
c.execute("INSERT INTO scene VALUES (NULL, ?, ?, ?, ?, 0)", data)
conn.commit()





#################################################################

#Maison

#################################################################

class Maison(ComposedArtifact):
    def __init__(self,x0,y0,z0,*args,**kwargs):
        
        ComposedArtifact.__init__(self,11,*args,**kwargs)
        U = vec3(1,0,0)
        V = vec3(0,1,0) # axe sur lequel il sera projété
        C = vec3(x0+0,y0+0,z0+0)
        l = 0.3
        
        cube = Cube(C, U, V, l, diffuse=rgb(0.65,0.27,0.25), mirror=0, specular=0)
        S = vec3(0+x0,y0+0.5,z0+0.5) # Coordonnées entre -1 et 1 (x = horizontal, y = verticale, z = sens de la page)
        vertices = [vec3(x0-0.2,y0+0.2,z0-0.2), vec3(x0+0.2,y0+0.2,z0-0.2), vec3(x0+0.2,y0+0.2,z0+0.2), vec3(x0-0.2,y0+0.2,z0+0.2)]
        base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0), mirror=0, specular=0)
        
        pyr = Pyramid(base, S, diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0)
        
        for j in range (6):
            self[j]=cube[j]
        for j in range (5):
            self[j+6]=pyr[j]
            
scene = Scene('Maison', 0, 1)
scene.append(LightSource(vec3(-1., 2, -3), 1))
scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
scene.append(Maison(0,0,0,diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0))

scene.initialize(E=vec3(0,2,-10)).trace().save_image()
pass

conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

# liste des valeurs enregistrées, dans l'ordre des champs de la table scene
# N.B. on s'attend ici à disposer d'une scène dans la variable "scene" 
data = [
    scene.name,
    scene.serialize(),
    scene.w,
    scene.h
]

# enregistrement des informations par soumission d'une requête SQL INSERT
c.execute("INSERT INTO scene VALUES (NULL, ?, ?, ?, ?, 0)", data)
conn.commit()
#################################################################

#Voiture

#################################################################

class Voiture(ComposedArtifact):
    def __init__(self,x0,y0,z0,*args,**kwargs):
        
        ComposedArtifact.__init__(self,42,*args,**kwargs)

        P = [vec3(-0.3+x0,0.1+y0,-0.2+z0), vec3(0.3+x0,0.1+y0,-0.2+z0), vec3(x0-0.3,y0+0.1,z0+0.2), vec3(x0+0.3,y0+0.1,z0+0.2)]
        V = vec3(0,0,1) # axe sur lequel il sera projété
        r = 0.1
        h1 = 0.1
        h2 = -0.1

        roue0 = Cylinder(P[0], V, r, h2, diffuse=rgb(124,117,117), mirror=0, specular=0)
        roue1 = Cylinder(P[1], V, r, h2, diffuse=rgb(124,117,117), mirror=0, specular=0)
        roue2 = Cylinder(P[2], V, r, h1, diffuse=rgb(124,117,117), mirror=0, specular=0)
        roue3 = Cylinder(P[3], V, r, h1, diffuse=rgb(124,117,117), mirror=0, specular=0)

        U = vec3(1,0,0)
        V = vec3(0,0,1) # axe sur lequel il sera projété
        C1 = vec3(x0+0,y0+0.3,z0+0)
        l1 = 0.4

        C2 = vec3(0.3+x0,y0+0.2,z0-0.1)
        l2 = 0.2
        C3 = vec3(x0+0.3,y0+0.2,z0+0.1)
        C4 = vec3(x0-0.3,y0+0.2,z0+0.1)
        C5 = vec3(x0-0.3,y0+0.2,z0-0.1)
        
        cube1 = Cube(C1, U, V, l1, diffuse=rgb(1,0,0), mirror=0, specular=0)
        cube2 = Cube(C2, U, V, l2, diffuse=rgb(1,0,0), mirror=0, specular=0)
        cube3 = Cube(C3, U, V, l2, diffuse=rgb(1,0,0), mirror=0, specular=0)
        cube4 = Cube(C4, U, V, l2, diffuse=rgb(1,0,0), mirror=0, specular=0)
        cube5 = Cube(C5, U, V, l2, diffuse=rgb(1,0,0), mirror=0, specular=0)

        for j in range(3):
            self[j]=roue0[j]
        for j in range(3):
            self[j+3]=roue1[j]
        for j in range(3):
            self[j+6]=roue2[j]        
        for j in range(3):
            self[j+9]=roue3[j]
        for j in range(6):
            self[j+12]=cube1[j]
        for j in range(6):
            self[j+18]=cube2[j]
        for j in range (6):
            self[j+24]=cube3[j]
        for j in range (6):
            self[j+30]=cube4[j]
        for j in range (6):
            self[j+36]=cube5[j]
        
scene = Scene('Voiture', 0, 1)
scene.append(LightSource(vec3(-1., 2, -3), 1))
scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
scene.append(Voiture(0,0,0,diffuse=rgb(0.95,0.73,0.43), mirror=0, specular=0))
scene.initialize(E=vec3(0,2,-10)).trace().save_image()
pass

conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

# liste des valeurs enregistrées, dans l'ordre des champs de la table scene
# N.B. on s'attend ici à disposer d'une scène dans la variable "scene" 
data = [
    scene.name,
    scene.serialize(),
    scene.w,
    scene.h
]

# enregistrement des informations par soumission d'une requête SQL INSERT
c.execute("INSERT INTO scene VALUES (NULL, ?, ?, ?, ?, 0)", data)
conn.commit()

#################################################################

#Arbre

#################################################################

class Arbre(ComposedArtifact):
    def __init__(self,x0,y0,z0,*args,**kwargs):
        ComposedArtifact.__init__(self,4,*args,**kwargs)
        # Coordonnées entre -1 et 1 (x = horizontal, y = verticale, z = sens de la page)
        V = vec3(0,1,0) # axe sur lequel il sera projété
        r = 0.1
        h = 4*r
        P = vec3(x0,y0-0.05,z0)
        
        cyl = Cylinder(P, V, r, h, diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0)
        
        center = P + vec3(0,h,0) # Coordonnées entre -1 et 1 (x = horizontal, y = verticale, z = sens de la page)
        radius = 2*r
        sph = Sphere(center, radius, diffuse=rgb(0.1,0.9,0.1), mirror=0, specular=0)

        for j in range(3):
            self[j]= cyl[j]
        self[3] = sph
    
scene = Scene('Arbre', 0, 1)
scene.append(LightSource(vec3(-2., 1, -2), 1))
scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
scene.append(Arbre(0,0,0,diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0))

scene.initialize(E=vec3(0,2,-10)).trace().save_image()
pass

conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

# liste des valeurs enregistrées, dans l'ordre des champs de la table scene
# N.B. on s'attend ici à disposer d'une scène dans la variable "scene" 
data = [
    scene.name,
    scene.serialize(),
    scene.w,
    scene.h
]

# enregistrement des informations par soumission d'une requête SQL INSERT
c.execute("INSERT INTO scene VALUES (NULL, ?, ?, ?, ?, 0)", data)
conn.commit()

#################################################################

#Sapin

#################################################################

class Sapin(ComposedArtifact):
    def __init__(self, x0, y0, z0, taille, *args,**kwargs):
        
        ComposedArtifact.__init__(self,4,*args,**kwargs)
        cyl = Cylinder(vec3(x0,y0,z0), vec3(0,1,0).rotate_x(-0.15),taille/3,1.3*taille, diffuse=rgb(184,115,51), mirror=0, specular=0)
        cone = ConeTrunk(vec3(x0,y0+3*taille,z0),vec3(0,-1,0), 2.5*taille, 2*taille, rgb(0,255,0))
        
        for j in range (3):
            self[j] = cyl[j]
        self[3] = cone

scene = Scene('Sapin', 0, 1)
scene.append(LightSource(vec3(-1., 2, -3), 1))
scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
scene.append(Sapin(0, -0.1, 0, 0.15, diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0))

scene.initialize(E=vec3(0,2,-10)).trace().save_image()
pass

conn = sqlite3.connect('raytracing.sqlite')
c = conn.cursor()

# liste des valeurs enregistrées, dans l'ordre des champs de la table scene
# N.B. on s'attend ici à disposer d'une scène dans la variable "scene" 
data = [
    scene.name,
    scene.serialize(),
    scene.w,
    scene.h
]

# enregistrement des informations par soumission d'une requête SQL INSERT
c.execute("INSERT INTO scene VALUES (NULL, ?, ?, ?, ?, 0)", data)
conn.commit()