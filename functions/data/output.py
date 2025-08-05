from math import pi
import time

def output(model,filename):
    file1 = open(filename, "w")
    # Natural frequencies & subset
    omega = model.omega
    solve_subset = model.solve_subset
    
    ### Output ###
    file1.write(f'Output from vibration analysis \n')
    curr_time = time.strftime("%D - %H:%M:%S", time.localtime())
    file1.write(f'{curr_time}\n')

    ### Print natural frequencies ####
    file1.write(f'\n')
    file1.write('****************** Natural frequencies (SI-units) ******************\n')
    file1.write(f'      Mode number         Natural circular frequency [rad/s]\n')
    file1.write(f'____________________________________________________________________\n')
    if solve_subset == None:
        for i in range(len(omega)):
            if omega[i] < 1.0:
                file1.write(f'      {i+1}                        {omega[i]:12.3e}\n')
            else:
                file1.write(f'      {i+1}                        {omega[i]:12.3f}\n')
    else:
        for i in range(len(omega)):
            j = solve_subset[0] + i
            if omega[i] < 1.0:
                file1.write(f'      {j+1}                        {omega[i]:12.3e}\n')
            else:
                file1.write(f'      {j+1}                        {omega[i]:12.3f}\n')
    file1.write(f'\n')
    
    file1.write(f'      Mode number         Natural cyclic frequency [1/s]\n')
    file1.write(f'____________________________________________________________________\n')
    if solve_subset == None:
        for i in range(len(omega)):
            if omega[i]/(2*pi) < 1.0:
                file1.write(f'      {i+1}                        {omega[i]/(2*pi):12.3e}\n')
            else:
                file1.write(f'      {i+1}                        {omega[i]/(2*pi):12.3f}\n')
    else:    
        for i in range(len(omega)):
            j = solve_subset[0] + i
            if omega[i]/(2*pi) < 1.0:
                file1.write(f'      {j+1}                        {omega[i]/(2*pi):12.3e}\n')
            else:
                file1.write(f'      {j+1}                        {omega[i]/(2*pi):12.3f}\n')     
    file1.close()