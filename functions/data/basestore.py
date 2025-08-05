import sqlite3
from functions.data.baseclear import baseclear
from functions.data.baseinsert import baseinsert
import os

def basestore(Model, name='Truss_DataBase.db'):

    X = Model.X
    C = Model.C
    mprop = Model.mprop
    bound = Model.bound
    spring_support = Model.spring_support

    ldof = Model.ldof
    nno = Model.nno
    nne = Model.nne
    ndof = Model.ndof

    var = (1, ldof, nno, nne, ndof)

    Kmat = Model.K
    Mmat = Model.M
    omega = Model.omega
    U = Model.U

    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = dir + '/' + name

    # Clear the database if it already exists
    if os.path.exists(file_path):
        baseclear(file_path)

    con = sqlite3.connect(file_path)
    cur = con.cursor()

    # Define tables for structure
    cur.execute("""
    CREATE TABLE IF NOT EXISTS var (
        id   INTEGER PRIMARY KEY,
        ldof INTEGER NOT NULL,
        nno  INTEGER NOT NULL,
        nne  INTEGER NOT NULL,
        ndof INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS node (
        id INTEGER PRIMARY KEY,
        x REAL NOT NULL,
        y REAL NOT NULL,
        z REAL NOT NULL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS connectivity (
        id INTEGER PRIMARY KEY,
        node1 INTEGER NOT NULL,
        node2 INTEGER NOT NULL,
        propno INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS material (
        propno INTEGER PRIMARY KEY,
        E REAL NOT NULL,
        A REAL NOT NULL,
        rho REAL NOT NULL,
        Iy REAL NOT NULL,
        Iz REAL NOT NULL,
        J REAL NOT NULL,
        G REAL NOT NULL,
        type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bound (
        node INTEGER NOT NULL,
        ldof INTEGER NOT NULL,
        disp REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS spring (
        node INTEGER NOT NULL,
        ldof INTEGER NOT NULL,
        Kk REAL NOT NULL
    )
    """)

    # Define tables for Mass
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Mass (
        i INTEGER NOT NULL,
        j INTEGER NOT NULL,
        m REAL NOT NULL
    )
    """)

    # Define tables for stiffness
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Stiffness (
        i INTEGER NOT NULL,
        j INTEGER NOT NULL,
        k REAL NOT NULL
    )
    """)

    # Define tables for eigenvalues
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Eigenvalues (
        id INTEGER PRIMARY KEY,
        omega REAL
    )
    """)

    # Define tables for eigenvectors
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Eigenvectors (
        i INTEGER NOT NULL,
        j INTEGER NOT NULL,
        U REAL NOT NULL
    )
    """)

    baseinsert(X, C, mprop, bound, spring_support, var, Mmat, Kmat, omega, U, cur)
    
    # Add indexes for faster queries
    cur.execute("CREATE INDEX IF NOT EXISTS idx_mass_ij ON Mass(i, j);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stiffness_ij ON Stiffness(i, j);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_eigenvec_ij ON Eigenvectors(i, j);")

    con.commit()
    con.close()