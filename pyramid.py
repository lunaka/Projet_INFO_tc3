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
