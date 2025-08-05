import numpy as np
import sqlite3
import os
from scipy.sparse import lil_matrix

class VIBdata:
    def __init__(self, name):
        self.db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/' + name
        self.X = None
        self.C = None
        self.mprop = None
        self.bound = None
        self.spring_support = None
        self.ldof = None
        self.nno = None
        self.nne = None
        self.ndof = None
        self.Mmat = None
        self.Kmat = None
        self.omega = None
        self.U = None
        
        self._fetch_data()

    def _fetch_data(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            self.X = self._fetch_nodes(cur)
            self.C = self._fetch_connectivity(cur)
            self.mprop = self._fetch_materials(cur)
            self.bound = self._fetch_bound(cur)
            self.spring_support = self._fetch_spring(cur)
            var = self._fetch_var(cur)
            self.ldof, self.nno, self.nne, self.ndof = var
            self.Mmat = self._fetch_Mass(cur)
            self.Kmat = self._fetch_Stiffness(cur)
            self.omega = self._fetch_omega(cur)
            self.U = self._fetch_Displacements(cur)

    def _fetch_nodes(self, cur):
        cur.execute("SELECT x, y, z FROM node")
        return np.array(cur.fetchall(), dtype=float)

    def _fetch_connectivity(self, cur):
        cur.execute("SELECT node1, node2, propno FROM connectivity")
        return np.array(cur.fetchall(), dtype=int)

    def _fetch_materials(self, cur):
        cur.execute("SELECT propno, E, A, rho, Iy, Iz, J, G, type FROM material")
        return {
            row[0]: {
                'E': row[1], 'A': row[2], 'rho': row[3],
                'Iy': row[4], 'Iz': row[5], 'J': row[6],
                'G': row[7], 'type': row[8]
            }
            for row in cur.fetchall()
        }

    def _fetch_bound(self, cur):
        cur.execute("SELECT node, ldof, disp FROM bound")
        return np.array(cur.fetchall(), dtype=float)

    def _fetch_spring(self, cur):
        cur.execute("SELECT node, ldof, Kk FROM spring")
        return np.array(cur.fetchall(), dtype=float)

    def _fetch_var(self, cur):
        cur.execute("SELECT ldof, nno, nne, ndof FROM var")
        return cur.fetchone()

    def _fetch_Mass(self, cur):
        cur.execute("SELECT i, j, m FROM Mass")
        rows = cur.fetchall()
        size = max(max(i, j) for i, j, _ in rows)
        Mmat = lil_matrix((size, size), dtype=float)
        for i, j, m in rows:
            Mmat[i - 1, j - 1] = m
        return Mmat.toarray()

    def _fetch_Stiffness(self, cur):
        cur.execute("SELECT i, j, k FROM Stiffness")
        rows = cur.fetchall()
        size = max(max(i, j) for i, j, _ in rows)
        Kmat = lil_matrix((size, size), dtype=float)
        for i, j, k in rows:
            Kmat[i - 1, j - 1] = k
        return Kmat.toarray()

    def _fetch_omega(self, cur):
        cur.execute("SELECT omega FROM Eigenvalues ORDER BY id")
        return np.array([row[0] for row in cur.fetchall()], dtype=float)

    def _fetch_Displacements(self, cur):
        cur.execute("SELECT i, j, U FROM Eigenvectors")
        rows = cur.fetchall()
        max_i = max(i for i, _, _ in rows)
        max_j = max(j for _, j, _ in rows)
        U = lil_matrix((max_i, max_j), dtype=float)
        for i, j, u in rows:
            U[i - 1, j - 1] = u
        return U.toarray()