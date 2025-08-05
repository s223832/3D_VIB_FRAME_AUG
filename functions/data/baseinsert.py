def baseinsert(X, C, mprop, bound, spring_support, var, Mmat, Kmat, omega, U, cur):

    cur.execute("INSERT INTO var (id, ldof, nno, nne, ndof) VALUES (?, ?, ?, ?, ?)", 
                (int(var[0]), int(var[1]), int(var[2]), int(var[3]), int(var[4])))

    cur.executemany("INSERT INTO node (id, x, y, z) VALUES (?, ?, ?, ?)", 
                    [(int(i), float(x), float(y), float(z)) for i, (x, y, z) in enumerate(X, start=1)])

    cur.executemany("INSERT INTO connectivity (id, node1, node2, propno) VALUES (?, ?, ?, ?)", 
                    [(int(i), int(n1), int(n2), int(p)) for i, (n1, n2, p) in enumerate(C, start=1)])

    cur.executemany("INSERT INTO material (propno, E, A, rho, Iy, Iz, J, G, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    [(int(propno), mat['E'], mat['A'], mat['rho'], mat['Iy'], mat['Iz'], mat['J'], mat['G'], mat['type']) 
                     for propno, mat in mprop.items()])

    cur.executemany("INSERT INTO bound (node, ldof, disp) VALUES (?, ?, ?)", 
                    [(int(node), int(ldof), float(disp)) for node, ldof, disp in bound])

    cur.executemany("INSERT INTO spring (node, ldof, Kk) VALUES (?, ?, ?)", 
                    [(int(node), int(ldof), float(Kk)) for node, ldof, Kk in spring_support])

    mass_data = [(int(i+1), int(j+1), float(Mmat[i, j])) 
                 for i in range(Mmat.shape[0]) for j in range(Mmat.shape[1]) if Mmat[i, j] != 0.0]
    cur.executemany("INSERT INTO Mass (i, j, m) VALUES (?, ?, ?)", mass_data)

    stiff_data = [(int(i+1), int(j+1), float(Kmat[i, j])) 
                  for i in range(Kmat.shape[0]) for j in range(Kmat.shape[1]) if Kmat[i, j] != 0.0]
    cur.executemany("INSERT INTO Stiffness (i, j, k) VALUES (?, ?, ?)", stiff_data)

    cur.executemany("INSERT INTO Eigenvalues (id, omega) VALUES (?, ?)", 
                    [(int(i), float(o)) for i, o in enumerate(omega, start=1)])

    U_data = [(int(i+1), int(j+1), float(U[i, j])) 
              for i in range(U.shape[0]) for j in range(U.shape[1]) if U[i, j] != 0.0]
    cur.executemany("INSERT INTO Eigenvectors (i, j, U) VALUES (?, ?, ?)", U_data)
