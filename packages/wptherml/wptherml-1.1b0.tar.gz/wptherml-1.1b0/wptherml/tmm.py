# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:05:59 2018
@author: varnerj
"""

###Transfer Matrix Method
import numpy as np
from matplotlib import pyplot as plt
from numpy.linalg import inv


### this function will compute the P matrix for a given layer l
### this function expects you have pre-calculated phil for that layer
def BuildP(phil):
    P = np.zeros((2,2),dtype=complex)
    ci = 0+1j

    a = -1*ci*phil
    b = ci*phil
    
    P[0][1] = 0+0j
    P[1][0] = 0+0j
    P[0][0] = np.exp(a)
    P[1][1] = np.exp(b)
    return P

### this function will compute the derivative of the P matrix for a given
### layer l with respect to the thickness of layer l

def BuildD(nl, ctheta,pol):
    D = np.zeros((2,2),dtype=complex)

    
    if (pol=="s" or pol=="S"):
        D[0][0] = 1.+0j
        D[0][1] = 1.+0j
        D[1][0] = nl*ctheta
        D[1][1] = -1*nl*ctheta
        
        
    elif (pol=="p" or pol=="P"):
        D[0][0] = ctheta+0j
        D[0][1] = ctheta+0j
        D[1][0] = nl
        D[1][1] = -1*nl

    ### defaulting to P polarization 
    else: 
        print("Polarization not chosen... defaulting to p-polarization")
        D[0][0] = ctheta+0j
        D[0][1] = ctheta+0j
        D[1][0] = nl
        D[1][1] = -1*nl
        
    return D

### main driver function for the transfer matrix method
### TMM should do the following:
### This assumes that nA and tA are both arrays of length equal
### to the number of layers
### 1. Calculate D_1^-1, which requires n[0] and theta0
### 2. Calculate D_2, D_2^-1, P_2 ... D_L-1, D_L-1^-1, P_L-1, which requires
###    phi_2 ... phi_L-1, k_z_2 ... k_z_L-1, d[1]...d[L-2]
### 3. Calculate D_L
### 4. Multiply all matrices together in order to form M
### 5. Return relevant quantity(s)... maybe M itself, maybe 1 - R - T... TBD

def tmm(k0, theta0, pol, nA, tA):
    t1 = np.zeros((2,2),dtype=complex)
    t2 = np.zeros((2,2),dtype=complex)
    D1 = np.zeros((2,2),dtype=complex)
    Dl = np.zeros((2,2),dtype=complex)
    Dli = np.zeros((2,2),dtype=complex)
    Pl = np.zeros((2,2),dtype=complex)
    M  = np.zeros((2,2),dtype=complex)
    L = len(nA)
    kz = np.zeros(L,dtype=complex)
    phil = np.zeros(L,dtype=complex)
    ctheta = np.zeros(L,dtype=complex)
    theta = np.zeros(L,dtype=complex)
    ctheta[0] = np.cos(theta0)
    
    D1 = BuildD(nA[0], ctheta[0], pol)
    ### Note it is actually faster to invert the 2x2 matrix
    ### "By Hand" than it is to use linalg.inv
    ### and this inv step seems to be the bottleneck for the TMM function
    tmp = D1[0,0]*D1[1,1]-D1[0,1]*D1[1,0]
    det = 1/tmp
    M[0,0] = det*D1[1,1]
    M[0,1] = -det*D1[0,1]
    M[1,0] = -det*D1[1,0]
    M[1,1] = det*D1[0,0]
    #D1i = inv(D1)
   #print("D1i is ")
   #print(D1i)
    
    
    ### This is the number of layers in the structure

    
    ### since kx is conserved through all layers, just compute it
    ### in the upper layer (layer 1), for which you already known
    ### the angle of incidence
    kx = nA[0]*k0*np.sin(theta0)
    kz[0] = np.sqrt((nA[0]*k0)**2 - kx**2)
    kz[L-1] = np.sqrt((nA[L-1]*k0)**2 - kx**2)
    
    ### keeping consistent with K-R excitation
    if np.real(kz[0])<0:
        kz[0] = -1*kz[0]
    if np.imag(kz[L-1])<0:
        kz[L-1] = -1*kz[L-1]
    ### loop through all layers 2 through L-1 and compute kz and cos(theta)...
    ### note that when i = 1, we are dealing with layer 2... when 
    ### i = L-2, we are dealing with layer L-1... this loop only goes through
    ### intermediate layers!
    for i in range(1,(L-1)):
        kz[i] = np.sqrt((nA[i]*k0)**2 - kx**2)
        if np.imag(kz[i])<0:
            kz[i] = -1*kz[i]
        
        ctheta[i] = kz[i]/(nA[i]*k0)
        theta[i] = np.arccos(ctheta[i])

        phil[i] = kz[i]*tA[i]

        Dl = BuildD(nA[i],ctheta[i], pol)
        ## Invert Dl
        tmp = Dl[0,0]*Dl[1,1]-Dl[0,1]*Dl[1,0]
        det = 1/tmp
        Dli[0,0] = det*Dl[1,1]
        Dli[0,1] = -det*Dl[0,1]
        Dli[1,0] = -det*Dl[1,0]
        Dli[1,1] = det*Dl[0,0]
        #Dli = inv(Dl)
        ## form Pl
        Pl = BuildP(phil[i])

        t1 = np.matmul(M,Dl)
        t2 = np.matmul(t1,Pl)
        M  = np.matmul(t2,Dli)
        
    ### M is now the product of D_1^-1 .... D_l-1^-1... just need to 
    ### compute D_L and multiply M*D_L
    kz[L-1] = np.sqrt((nA[L-1]*k0)**2 - kx**2)
    ctheta[L-1]= kz[L-1]/(nA[L-1]*k0)
    DL = BuildD(nA[L-1], ctheta[L-1], pol)
    t1 = np.matmul(M,DL)
    ### going to create a dictionary called M which will 
    ### contain the matrix elements of M as well as 
    ### other important quantities like incoming and outgoing angles
    theta[0] = theta0
    theta[L-1] = np.arccos(ctheta[L-1])
    ctheta[0] = np.cos(theta0)
    M = {"M11": t1[0,0], 
         "M12": t1[0,1], 
         "M21": t1[1,0], 
         "M22": t1[1,1],
         "theta_i": theta0,
         "theta_L": np.real(np.arccos(ctheta[L-1])),
         "kz": kz,
         "phil": phil,
         "ctheta": ctheta,
         "theta": theta
         }

    return M



### This function will take a thickness array
### and a scalar thickness and will return
### the index of the layer in which you are in
### at that thickness
### analytically differentiates the transfer matrix
### with respect to the thickness of a layer li to be specified by 
### the user!
def tmm_grad(k0, theta0, pol, nA, tA, layers):
    n = len(layers)
    N = len(tA)
    ### Initialize arrays!
    Dli = np.zeros((N,2,2), dtype = complex)
    Dl = np.zeros((N,2,2), dtype = complex)
    D1 = np.zeros((2,2),dtype=complex)
    Pl = np.zeros((N, 2, 2), dtype = complex)
    Plp = np.zeros((n,2,2), dtype = complex)
    Mp = np.zeros((n, 2,2), dtype = complex)
    t1 = np.zeros((2,2), dtype = complex)
    t2 = np.zeros((2,2), dtype = complex)
    kz = np.zeros(N, dtype = complex)
    phil = np.zeros(N, dtype = complex)
    ctheta = np.zeros(N, dtype = complex)
    theta = np.zeros(N, dtype = complex)
    M = np.zeros((2,2), dtype = complex)
    ### compute kx
    kx = nA[0]*np.sin(theta0)*k0
    ### compute D1
    ctheta[0] = np.cos(theta0)
    D1 = BuildD(nA[0],ctheta[0], pol)
    ### compute D1^-1
    tmp = D1[0,0]*D1[1,1]-D1[0,1]*D1[1,0]
    det = 1/tmp
    M[0,0] = det*D1[1,1]
    M[0,1] = -det*D1[0,1]
    M[1,0] = -det*D1[1,0]
    M[1,1] = det*D1[0,0]
    Dli[0,:,:] = np.copy(M)
    ### Initialize gradient of M with D1^-1
    for i in range(0,n):
        Mp[i,:,:] = np.copy(M)
    ### Compute kz0
    kz[0] = np.sqrt(nA[0]*k0)**2-kx**2
    ### Compute kz, phil, D, P, D^-1 quantities for all  finite layers!
    for i in range (1,(N-1)):
        kz[i] = np.sqrt((nA[i]*k0)**2-kx**2)
        if np.imag(kz[i]) < 0:
            kz[i] = -1 * kz[i]
        ctheta[i] = kz[i]/(nA[i]*k0)
        theta[i] = np.arccos(ctheta[i])
        phil[i] = kz[i]*tA[i]
        Dl[i,:,:] = BuildD(nA[i], ctheta[i], pol)
        tmp = Dl[i,0,0]*Dl[i,1,1]-Dl[i,0,1]*Dl[i,1,0]
        det = 1/tmp
        Dli[i,0,0] = det*Dl[i,1,1]
        Dli[i,0,1] = -det*Dl[i,0,1]
        Dli[i,1,0] = -det*Dl[i,1,0]
        Dli[i,1,1] = det*Dl[i,0,0]
        Pl[i,:,:] = BuildP(phil[i])
        t1 = np.dot(M,Dl[i,:,:])
        t2 = np.dot(t1, Pl[i,:,:])
        M = np.dot(t2,Dli[i,:,:])
        
    ### kz, Dl for final layer!
    kz[N-1] = np.sqrt((nA[N-1]*k0)**2-kx**2)
    ctheta[N-1] = kz[N-1]/(nA[N-1]*k0)
    Dl[N-1,:,:] = BuildD(nA[N-1],ctheta[N-1], pol)
    t1 = np.dot(M,Dl[N-1,:,:])
    ### This is the transfer matrix!
    M = np.copy(t1)
    ### for all layers we want to differentiate with respect to, 
    ### form Plp matrices
    for l in range(0,n):
        Plp[l,:,:] = Build_dP_ds(kz[layers[l]],tA[layers[l]])
    ### for all those layers, compute associated matrix products!
    idx = 0
    for i in layers:
        for l in range(1,i):
            t1 = np.dot(Mp[idx,:,:], Dl[l,:,:])
            t2 = np.dot(t1, Pl[l,:,:])
            Mp[idx,:,:] = np.dot(t2,Dli[l,:,:])
        t1 = np.dot(Mp[idx,:,:],Dl[i,:,:])
        t2 = np.dot(t1,Plp[idx,:,:])
        Mp[idx,:,:] = np.dot(t2,Dli[i,:,:])
        for l in range(i+1,N-1):
            t1 = np.dot(Mp[idx,:,:], Dl[l,:,:])
            t2 = np.dot(t1, Pl[l,:,:])
            Mp[idx,:,:] = np.dot(t2,Dli[l,:,:])
        t1 = np.dot(Mp[idx,:,:],Dl[N-1,:,:])
        Mp[idx,:,:] = np.copy(t1)
        idx = idx+1
    
    M = {
         "Mp": Mp,   
         "M11": M[0,0], 
         "M12": M[0,1], 
         "M21": M[1,0], 
         "M22": M[1,1],
         "theta_i": theta0,
         "theta_L": np.real(np.arccos(ctheta[N-1])),
         "kz": kz,
         "phil": phil,
         "ctheta": ctheta,
         "theta": theta
            
            
            }
    return M



def whichLayer(t, d):
    ### empty array for cumulative thickness array
    dc = cumulativeD(d)

    ### default is that you are in the final layer
    l = len(d)-1
    ### check the actual thickness against the cumulative
    ### thickness array to see if you aren't actually in the final layer
    for i in range(0,len(dc)):
        if (dc[i]>=t):
            l = i
            break
        
    return l

### This function forms an array dc of cumulative thicknesses from 
### the array of thicknesses of each layer...
### e.g. if d = [0, 200e-9, 300e-9, 0] then dc = [0, 200e-9, 500e-9, 500e-9]
def cumulativeD(d):
    dc = []
    som = 0
    for i in range(0,len(d)):
        som = som+d[i]
        dc.append(som)
    
    return dc

def Ex(z, k0, theta0, pol, n, d):
    ### declare an array that will hold Ex
    Ex = np.zeros(len(z),dtype=complex)
    ### complex unit
    ci = 0+1j
    ### Get M dictionary with various TMM outputs
    M = tmm(k0, theta0, 'p', n, d)
    ### t amplitude 
    t = 1./M['M11']
    ### r amplitude
    r = M['M21']/M['M11']
    ### array of kz components
    kz = M['kz']
    ### array of phil values
    phil = M['phil']
    ### array of cos(theta)
    ctheta = M['ctheta']
    ### fill out initial and final field components
    Ef = np.zeros(2,dtype=complex)
    Ei = np.zeros(2,dtype=complex)
    ### arrays for all field amplitudes
    Ep = np.zeros(len(n),dtype=complex)
    Em = np.zeros(len(n),dtype=complex)
    ### temporary arrays
    T1 = np.zeros(2,dtype=complex)
    T2 = np.zeros(2,dtype=complex)
    D = np.zeros((2,2),dtype=complex)
    Di = np.zeros((2,2),dtype=complex)
    P = np.zeros((2,2),dtype=complex)
    ### initial and final field amplitudes
    Ef[0] = t
    Ef[1] = 0
    Ei[0] = 1
    Ei[1] = r
    Ep[0] = 1
    Em[0] = r
    lm1 = len(n)-1
    Ep[lm1] = t
    Em[lm1] = 0
    T2 = Ef
    D = BuildD(n[lm1],ctheta[lm1],'p')
    for i in range(1,lm1):
        l = lm1-i
        T1 = np.dot(D,T2)
        D = BuildD(n[l],ctheta[l],'p')
        Di = inv(D)
        T2 = np.dot(Di,T1)
        P = BuildP(phil[l])
        T1 = np.dot(P,T2)
        Ep[l] = T1[0]
        Em[l] = T1[1]
        T2 = T1  #np.dot(D,T1)
    
    ### now we have the field amplitudes in each layer... just need to 
    ### evaluate the fields in each layer and store as a vector
    
    ### hard-code layer 0:
    l = 0
    doff = 0
    dc = cumulativeD(d)
    for i in range(0,len(z)):
        l = whichLayer(z[i],d)
        if (l==0):
            doff = 0
        else:
            doff = dc[l-1]
        
        Ex[i] = Ep[l]*np.exp(ci*kz[l]*(z[i]-doff))+Em[l]*np.exp(-ci*kz[l]*(z[i]-doff))
    
    return {'Ex': Ex, 'v_list': Ep, 'w_list': -1*Em}

### returns absorption as a function of distance into a multilayer
def AbsAlongz(z, k0, theta0, pol, n, d):
    
    alpha = np.zeros(len(z),dtype=complex)
    ### Get M dictionary with various TMM outputs
    M = tmm(k0, theta0, 'p', n, d)
   
    ### Get dictionary aassociated with field amplitudes for v and w vectors
    Ef = Ex(z, k0, theta0, pol, n, d)
    v = Ef['v_list']
    ### w amplitude - it is r
    w = Ef['w_list']
    ### get array of kz
    kz = M['kz']
    print("v is ",v)
    print("w is ",w)
    ### get array of cos(theta) values
    ctheta = M['ctheta']
    
    ### get array of theta values
    theta = M['theta']
    
    ### need four different arrays... A3c is the complex conjugate of A3
    #A1 = np.zeros_like(kz)
    #A2 = np.zeros_like(kz)
    #A3  = np.zeros_like(kz)
    #A3c = np.zeros_like(kz)
    
    ### this evaluates Ai for p-polarization
    ci = 0+1j
    for i in range(0,len(z)):
        temp = 0+0j
        ### which layer are we in?
        l = whichLayer(z[i],d)
        if (l>0):
            ### will need these quantities for each layer
            Ef = v[l] * np.exp(1j * kz[l] * z[i])
            Eb = w[l] * np.exp(-1j * kz[l] * z[i])

            thc = np.conj(theta[l])
            cth = np.cos(thc)
            cth0 = ctheta[0]
            imkz = np.imag(kz[l])
            rekz = np.real(kz[l])
            ni = n[l]
            n0 = n[0]
            num = ni*np.conj(cth)*(kz[l]*abs(Ef-Eb)**2-np.conj(kz[l])*abs(Ef+Eb)**2)
            denom = n0*np.conj(cth0)
            alpha[i]  = np.imag(num)/np.real(denom)
            #alpha[i] = np.imag(ni*np.conj(costh)*(kz[l]*abs(Ef-Eb)**2-np.conj(kz[l])*abs(Ef+Eb)**2)) / (n0*conj(costh0.real)
                
            #            absor = (n*conj(cos(th))*
            #     (kz*abs(Ef-Eb)**2-conj(kz)*abs(Ef+Eb)**2)
            #    ).imag / (n_0*conj(cos(th_0))).real

        
            #A1[l] = 2*imkz * np.real(ni * cth) * w[l]*np.conj(w[l]) / (np.real(n0*cth0))
            #A2[l] = 2*imkz * np.real(ni * cth) * v[l]*np.conj(v[l]) / (np.real(n0*cth0))
            #A3[l] = 2*rekz * np.imag(ni * cth) * v[l]*np.conj(w[l]) / (np.real(n0*cth0))
            #A3c[l] = np.conj(A3[l])
        
            #alpha[i] = A1[l]*np.exp(2*z[i]*imkz) + A2[l]*np.exp(-2*z[i]*imkz) + A3[l]*np.exp(2*ci*z[i]*rekz) + A3c[l]*np.exp(-2*ci*z[i]*rekz)
    return alpha
    
    
def Trans(k0, theta0, pol, nA, tA):
    L = len(nA)
    nL = nA[L-1]
    ni = nA[0]
    M = tmm(k0, theta0, pol, nA, tA)
    t = 1/M["M11"]
    ti = M["theta_i"]
    tL = M["theta_L"]
    fac = nL*np.cos(tL)/(ni*np.cos(ti))
    T = np.real(t*np.conj(t)*fac)
    return T

def Reflect(k0, theta0, pol, nA, tA):
    M = tmm(k0, theta0, pol, nA, tA)
    r = M["M21"]/M["M11"]
    R = np.real(r * np.conj(r))
    return R

def Abs(k0, theta0, pol, nA, tA):
    L = len(nA)
    nL = nA[L-1]
    ni = nA[0]
    M = tmm(k0, theta0, pol, nA, tA)
    r = M["M21"]/M["M11"]
    t = 1/M["M11"]
    ti = M["theta_i"]
    tL = M["theta_L"]
    fac = nL*np.cos(tL)/(ni*np.cos(ti))
    R = np.real(r*np.conj(r))
    T = np.real(t*np.conj(t)*fac)
    A = 1 - R - T
    return A

### This version of TMM will be used for finding the SPP and PA
### modes - the direct input to it is the x-component
### of the (complex) incident wavevector
def tmm_ab(k0, kx, pol, nA, tA):
    
    ### allocate various arrays
    t1 = np.zeros((2,2),dtype=complex)
    t2 = np.zeros((2,2),dtype=complex)
    Dl = np.zeros((2,2),dtype=complex)
    Dli = np.zeros((2,2),dtype=complex)
    Pl = np.zeros((2,2),dtype=complex)
    M  = np.zeros((2,2),dtype=complex)
    L = len(nA)
    kz = np.zeros(L,dtype=complex)
    phil = np.zeros(L,dtype=complex)
    ctheta = np.zeros(L,dtype=complex)
    theta = np.zeros(L,dtype=complex)

    ### get z-component of wave-vector in each layer
    ### and cos(theta_L) for each layer
    
    ### first layer has positive real part of kz
    kz[0] = np.sqrt( (nA[0]*k0)**2 - kx**2 )
    if (np.real(kz[0])<0):
        kz[0] = -1*kz[0]
    ctheta[0] = kz[0]/(nA[0]*k0)
    ### all other layers have positive imaginary parts... are evanescent
    for i in range(1,L):
        kz[i] = np.sqrt( (nA[i]*k0)**2 - kx**2 )
        if (np.imag(kz[i])<0):
            kz[i] = -1*kz[i]
        ctheta[i] = kz[i]/(nA[i]*k0)
    
    D1 = BuildD(nA[0], ctheta[0], pol)
    ### Note it is actually faster to invert the 2x2 matrix
    ### "By Hand" than it is to use linalg.inv
    ### and this inv step seems to be the bottleneck for the TMM function
    tmp = D1[0,0]*D1[1,1]-D1[0,1]*D1[1,0]
    det = 1/tmp
    M[0,0] = det*D1[1,1]
    M[0,1] = -det*D1[0,1]
    M[1,0] = -det*D1[1,0]
    M[1,1] = det*D1[0,0]


    ### loop through all layers 2 through L-1 and compute kz and cos(theta)...
    ### note that when i = 1, we are dealing with layer 2... when 
    ### i = L-2, we are dealing with layer L-1... this loop only goes through
    ### intermediate layers!
    for i in range(1,(L-1)):

        theta[i] = np.arccos(ctheta[i])
        phil[i] = kz[i]*tA[i]

        Dl = BuildD(nA[i],ctheta[i], pol)
        ## Invert Dl
        tmp = Dl[0,0]*Dl[1,1]-Dl[0,1]*Dl[1,0]
        det = 1/tmp
        Dli[0,0] = det*Dl[1,1]
        Dli[0,1] = -det*Dl[0,1]
        Dli[1,0] = -det*Dl[1,0]
        Dli[1,1] = det*Dl[0,0]
        #Dli = inv(Dl)
        ## form Pl
        Pl = BuildP(phil[i])

        t1 = np.matmul(M,Dl)
        t2 = np.matmul(t1,Pl)
        M  = np.matmul(t2,Dli)
        

    DL = BuildD(nA[L-1], ctheta[L-1], pol)
    t1 = np.matmul(M,DL)


    ### we only need |r|^2
    r = t1[1,0]/t1[0,0]
    return np.real(np.conj(r)*r)


