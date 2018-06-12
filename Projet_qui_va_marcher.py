# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:40:59 2018

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:56:41 2018

@author: Marine utilisateur
"""



from raytracer import *
from numpy import *
from random import *

x0=0.2
y0=0.2
z0=-0.1
taille=0.8


#______________________________________________________________________________

#P = vec3(0,0,0.5)
#r = 0.05
#C = vec3(0,8*r - 0.05,0.5)
#scene.append(Arbre_chene(P, vec3(0, 1, 0), r, C, diffuse = rgb(0.4, 0.5, 0.1), mirror = 0, specular = 0))
#vertices = [vec3(-0.5,0,0), vec3(0.5,0,0), vec3(0.5,0,1), vec3(-0.5,0,1)]
#base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0), mirror=0, specular=0)

P1 =vec3(0, 0, 0.5)
P2 =vec3(0, 0.5, 0.5)
#scene.append(Arbre_sapin(P1, vec3(0, 1, 0), 0.05, P2, diffuse = rgb(0.4, 0.5, 0.1), mirror = 0, specular = 0))
#scene.append(ConeTrunk(P2, vec3(0, -1, 0), 0.2,0.5, diffuse = rgb(0.4, 0.5, 0.1), mirror = 0, specular = 0))

#scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))
#scene.append(Cube(C, vec3(0, 0, 1), vec3(1, 0, 0), 0.5, diffuse=rgb(0.5,0.5,0), mirror=0, specular=0))

#scene.append(Sphere(vec3(0,5,10), 5))

def ajouter_pyramide(scene,x0,y0,z0,taille):
        Sommet = vec3(x0,z0+taille,y0)
        vertices = [vec3(x0-taille/sqrt(2),z0,y0-taille/sqrt(2)), vec3(x0+taille/sqrt(2),z0,y0-taille/sqrt(2)), vec3(x0+taille/sqrt(2),z0,y0+taille/sqrt(2)), vec3(x0-taille/sqrt(2),z0,y0+taille/sqrt(2))]
        base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0))
        
        scene.append(Pyramid(base, Sommet, diffuse=rgb(random(),random(),random()), mirror=0, specular=0))
        
        pass
    

def ajouter_sphere(scene,x0,y0,z0,taille):
    scene.append(Sphere(vec3(x0,y0,z0),taille,diffuse=rgb(randint(0,1),randint(0,1),randint(0,1))))
    #scene.initialize(E = vec3(0, 2, -10)).trace().save_image()
    pass

def ajouter_cylindre(scene,x0,y0,z0,taille):
    
    scene.append(Cylinder(vec3(x0,y0,z0), vec3(0,1,0).rotate_x(-0.15),taille/4,taille/2, mirror=0.25, specular=0.6, phong=140))


def ajouter_chene(scene,x0,y0,z0,taille):
    scene.append(Cylinder(vec3(x0,y0-taille,z0), vec3(0,1,0).rotate_x(-0.15),taille/3,2*taille, mirror=0.25, specular=0.6, phong=140))
    scene.append(Sphere(vec3(x0,y0+taille,z0),taille, diffuse=rgb(0,0.9,0)))
    
def ajouter_sapin(scene,x0,y0,z0,taille):
    scene.append(Cylinder(vec3(x0,y0,z0), vec3(0,1,0).rotate_x(-0.15),taille/3,1.3*taille, mirror=0.25, specular=0.6, phong=140))
    scene.append(ConeTrunk(vec3(x0,y0+3*taille,z0),vec3(0,-1,0), 2.5*taille, 2*taille, rgb(0.1,0.8,0.3)))

def ajouter_maison(scene,x0,y0,z0,taille):
    
    Sommet = vec3(x0,y0,z0)
    taille=1.5*taille
    c=taille
    d=taille/2
    vertices = [vec3(x0-c/sqrt(2),y0-d,z0-c/sqrt(2)), vec3(x0+c/sqrt(2),y0-d,z0-c/sqrt(2)), vec3(x0+c/sqrt(2),y0-d,z0+c/sqrt(2)), vec3(x0-c/sqrt(2),y0-d,z0+c/sqrt(2))]
    base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0))
#    
    scene.append(Pyramid(base, Sommet, diffuse=rgb(0.5,0.3,0), mirror=0, specular=0))
    scene.append(Cube(vec3(x0,y0-taille,z0),vec3(0,1,0),vec3(1,0,0), taille,diffuse=rgb(0,0.6,0.7), mirror=0, specular=0))





    
#scene.append(Cone(vec3(2.5,0.5,4),vec3(0,1,0),0.2,rgb(1.,0.75,0.5), mirror=0, specular=0.6, phong=140))
#scene1= Scene('essai',0,1)
#scene1.append(LightSource(vec3(-1., 2, 0), 1))
#scene1.append(Cylinder(vec3(0,-0.5,3),vec3(0,1,0).rotate_x(-0.15),1,0.25,colors, mirror=0.25, specular=0.6, phong=140))

#scene1.initialize(E=vec3(0,2,-10)).trace().save_image()
#pass  
    
#colors = [rgb(0,0,0),rgb(0.75,0.75,0.75),rgb(0.75,0.75,0.75)]
#scene.append(Cylinder(vec3(0,-0.5,3),vec3(0,1,0).rotate_x(-0.15),1,0.25,colors, mirror=0.25, specular=0.6, phong=140))   
#self.__tronc=Cylinder.__init__(self,vec3(x0-0.6,y0,z0), vec3(0,1,0), r/10, 8*r/10, *args, **kwargs)

l=[['sapin',0.9,-0.6,1,0.16],['chene',-0.2,-0.6,0.4,0.17],['chene',-0.2,-0.6,0.4,0.17],['sphere',-0.8,0.65,0.2,0.1],['maison',0.42,-0.1,0,0.25],['sapin',-0.8,-0.6,0.2,0.17]]
g=[['maison',0.5,0.2,0,0.08]]
v=[]

def creer_scene(liste):
    #,serial): #liste=[ [pyramide,x0,y0,z0,taille], [sphere,x0,y0,z0,taille], ....]
    name=str(randint(0,10000))
    scene = Scene(name, 0, 1)
    
    scene.append(LightSource(vec3(-1., 2, 1), 1))
    scene.append(LightSource(vec3(0,0,0), rgb(0.94,1,0.94)))
    scene.append(LightSource(vec3(-30, 10, 0), rgb(0.6,0.2,1)))
    scene.append(LightSource(vec3(0., 40, 0), rgb(0.6,0.13,0)))
    
   
    scene.append(Plane(vec3(0,-0.8,0), vec3(0,1,0)))
    for k in (liste):
        if k[0]=='Pyramide':
            ajouter_pyramide(scene,k[1],k[2],k[3],k[4])
        
        if k[0]=='Sphère':
            ajouter_sphere(scene,k[1],k[2],k[3],k[4])
        
        if k[0]=='Cylindre':
            ajouter_cylindre(scene,k[1],k[2],k[3],k[4])
        
        if k[0]=='Chêne':
            ajouter_chene(scene,k[1],k[2],k[3],k[4])
            
        if k[0]=='Sapin':
            ajouter_sapin(scene,k[1],k[2],k[3],k[4])
        
        if k[0]=='Maison':
            ajouter_maison(scene,k[1],k[2],k[3],k[4])
    
    scene.initialize(E = vec3(0, 2, -10)).trace().save_image()
    #scene.serialize()
    
    import sqlite3

    conn= sqlite3.connect('raytracing.sqlite')
    c=conn.cursor()
    w=400
    h=300
    data=['scene '+name,str(liste),w, h, scene.ptime, scene.name]
    c.execute("INSERT INTO scene VALUES (NULL,?,?,?,?,?,?)",data)
    
    conn.commit()
    return (name)








#scene = Scene('test', 0, 1)
#scene.append(LightSource(vec3(-0.9, 1.5, -0.5), 1))






#centre=vec3(x0,y0,z0)
#Sommet = vec3(x0,z0+taille,y0)
#vertices = [vec3(x0-taille/sqrt(2),z0,y0-taille/sqrt(2)), vec3(x0+taille/sqrt(2),z0,y0-taille/sqrt(2)), vec3(x0+taille/sqrt(2),z0,y0+taille/sqrt(2)), vec3(x0-taille/sqrt(2),z0,y0+taille/sqrt(2))]
#base = Polygon2(vertices, 1, diffuse=rgb(0.5,0.5,0))
##
#scene.append(Plane(vec3(0,-0.1,0), vec3(0,1,0)))


#scene.append(Pyramid1(x0,y0,z0,taille-0.7, diffuse=rgb(0.9,0.5,0.1), mirror=0, specular=0))
#scene.append(Sphere1(x0,y0+0.3,z0,0.09,diffuse=rgb(0.9,0.1,0.1), mirror=0, specular=0))
#scene.append(Arbre_chene(x0+0.3,y0,z0,taille,diffuse=rgb(0.9,0.1,0.1), mirror=0, specular=0))
#
#scene.initialize(E = vec3(0, 2, -10)).trace().save_image()
#pass

#==============================================================================
    
#==============================================================================

#scene = Scene('pyramid', 0, 1)
#scene.append(LightSource(vec3(-1., 2, 0), 1))
#

#
#scene.initialize(E=vec3(0,2,-10)).trace().save_image()
#pass