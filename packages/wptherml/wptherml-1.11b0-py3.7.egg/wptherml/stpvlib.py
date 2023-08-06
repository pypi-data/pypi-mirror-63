from wptherml.numlib import numlib
from wptherml.datalib import datalib
from wptherml import tmm
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

q = 1.60217662e-19
c=299792458
h=6.626e-34
k=1.38064852e-23


''' An idealized efficiency figure of merit with a numerator 
    that is proportional to short circuit current and a denominator proporitonal
    to incident power... the light-source can be thermal emission or can be solar.  '''
def multi_spectral_efficiency(lam, light, lbg1, lbg2):
    ### upper-bound of light-source
    upper = np.amax(lam)
    ### integrand for PV 1
    num_integrand_1 = light * lam/lbg1
    ### integrand for PV 2
    num_integrand_2 = light * lam/lbg2
    ### numerator 1
    numerator_1 = numlib.Integrate(num_integrand_1, lam, 1e-9, lbg1)
    ### numerator 2 
    numerator_2 = numlib.Integrate(num_integrand_2, lam, lbg1, lbg2)
    ### denominator
    denominator = numlib.Integrate(light, lam, 1e-9, upper)
    
    return numerator_1, numerator_2, denominator
    
### Trial objective function for multi-junction STPV with a single emitter!
def jsc_multi(lam, TE, eps_pv1, eps_pv2, T_pv1):
    upper = np.amax(lam)
    ### get the spectral response of Silicon and store it to an array called sr1
    sr1 = datalib.SR_Si(lam)
    ### get the spectral response of GaSb and store it to an array called sr1
    sr2 = datalib.SR_GaSb(lam)
    
    ### create integrand for jsc1
    int_1 = sr1 * eps_pv1 * TE
    
    ### create integrand for jsc2
    int_2 = sr2 * eps_pv2 * TE * T_pv1
    
    ### integrate the integrands!
    jsc1 = numlib.Integrate(int_1, lam, 1e-9, upper )
    
    jsc2 = numlib.Integrate(int_2, lam, 1e-9, upper )
    
    plt.plot(lam, int_1, 'red', label='Integrand 1')
    plt.plot(lam, int_2, 'blue', label='Integrand 2')

    plt.legend()
    plt.show()
    return jsc1, jsc2

### computes spectral efficiency given no
### angular dependence of emissivity
def SpectralEfficiency(TE,lam,lbg):
    ynum = TE*lam/lbg  
    upper = np.amax(lam)
    num = numlib.Integrate(ynum, lam, 1e-9, lbg)
    den = numlib.Integrate(TE, lam, 1e-9, upper)
    SE = num/den
    return SE

def stpv_pv_filter_fom(trans, ref, lam):
    ### set lambda_bg to 750 nm
    lbg = 750e-9
    ### get AM1.5 spectrum
    AM = datalib.AM(lam)
    ### get BB spectrum at 440 K
    BBs = datalib.BB(lam, 440)
    
    ### There are three different integrands for numerator 
    num_integrand_1 = np.copy(AM * trans * lam/lbg)
    num_integrand_2 = np.copy(AM * trans)
    num_integrand_3 = np.copy(BBs * ref)
    
    num1 = numlib.Integrate(num_integrand_1, lam, 300e-9, lbg)
    num2 = numlib.Integrate(num_integrand_2, lam, lbg, 3200e-9)
    num3 = numlib.Integrate(num_integrand_3, lam, 3200e-9, 3700e-9)
    
    ### denominator 1 comes from lam/lbg * AM1.5
    den_integrand_1 = np.copy(AM * lam/lbg)
    den1 = numlib.Integrate(den_integrand_1, lam, 300e-9, lbg)
    
    ### denominator 2 comes from AM1.5
    den2 = numlib.Integrate(AM, lam, lbg, 3200e-9)
    
    ### denominator 3 comes from BB spectrum
    return 0.5*num1/den1+0.5*num2/den2+2*num2/den2


def stpv_pv_filter_grad(dim, trans_prime, ref_prime, lam):
    lbg = 750e-9
    grad = np.zeros(dim)
    AM = datalib.AM(lam)
    BBs = datalib.BB(lam, 440)
    
    den_integrand_1 = np.copy(AM * lam/lbg)
    den1 = numlib.Integrate(den_integrand_1, lam, 300e-9, lbg)
    den2 = numlib.Integrate(AM, lam, lbg, 3200e-9)
    den3 = numlib.Integrate(BBs, lam, 3200e-9, 3700e-9)
    
    
    for i in range(0,dim):
        integrand_1 = np.copy(trans_prime[i,:]*AM*lam/lbg)
        integrand_2 = np.copy(trans_prime[i,:]*AM)
        integrand_3 = np.copy(ref_prime[i,:]*BBs)
        num_prime_1 = numlib.Integrate(integrand_1, lam, 300e-9, lbg)
        num_prime_2 = numlib.Integrate(integrand_2, lam, lbg, 3200e-9)
        num_prime_3 = numlib.Integrate(integrand_3, lam, 3200e-9, 3700e-9)

        grad[i] = 0.5*num_prime_1/den1 + 0.5*num_prime_2/den2 + 2*num_prime_3/den3
        
    return grad


### Computes spectral efficiency explicitly
### taking angular dependence into account
def SpectralEfficiency_EA(TE_p, TE_s, lam, lbg, t, w):
    num = 0.
    den = 0.
    dl = abs(lam[1]-lam[0])
    for i in range(0,len(w)):
        num_isom = 0.
        den_isom = 0.
        for j in range(0,len(lam)):
            den_isom = den_isom + 0.5*TE_p[i][j]*dl 
            den_isom = den_isom + 0.5*TE_s[i][j]*dl
            
            if lam[j]<=lbg:
                num_isom = num_isom + 0.5*lam[j]/lbg*TE_p[i][j]*dl 
                num_isom = num_isom + 0.5*lam[j]/lbg*TE_s[i][j]*dl
            
        num = num + w[i] * num_isom * np.sin(t[i]) * 2 * np.pi
        den = den + w[i] * den_isom * np.sin(t[i]) * 2 * np.pi 
    return num/den

### Computes useful power density assuming no
### angular dependence of emissivity
def Pwr_den(TE, lam, lbg):
    PDA = (lam/lbg)*TE
    PD  = numlib.Integrate(PDA,lam, 1e-9, lbg)
    return PD*np.pi



### Computes useful power density explicitly
### taking angular dependence of emissivity into account
def Pwr_den_EA(TE_p, TE_s, lam, lbg, t, w):
    PD = 0.
    dl = np.abs(lam[1] - lam[0])
    for i in range(0,len(w)):
        isom = 0.
        for j in range(0,len(lam)):
            if lam[j]>=lbg:
                break
            isom = isom + 0.5*lam[j]/lbg*TE_p[i][j]*dl 
            isom = isom + 0.5*lam[j]/lbg*TE_s[i][j]*dl
            
        PD = PD + w[i] * isom * np.sin(t[i])
    
    return PD*2*np.pi


### computes total power falling upon the PV cell given
### assuming no angular dependence of emissivity
def p_in(TE, lam):
    integrand = TE*np.pi
    upper = np.amax(lam)
    p = numlib.Integrate(integrand, lam, 1e-9,upper)
    return p

### Computes total power falling upon the PV cell 
### explicitly accounting for angular dependence
### of emitter... assumes emitter emits into a full 
### hemisphere
def p_in_ea(TE_p, TE_s, lam, t, w):
    pin = 0.
    dl = np.abs(lam[1]-lam[0])
    for i in range(0,len(w)):
        isom = 0.
        for j in range(0,len(lam)):
            isom = isom + 0.5*TE_p[i][j]*dl
            isom = isom + 0.5*TE_s[i][j]*dl
        pin = pin + w[i] * isom * np.sin(t[i])
    return pin * 2 * np.pi

### ideal estimate of short circuit current of PV in sun based on 
### its emissivity * AM1.5... should be updated with SR of PV data
def ambient_jsc(eps, lam, lbg):
    ### get upper bound of integral
    upper = np.amax(lam)
    ### get AM1.5 spectrum
    AM = datalib.AM(lam)
    ### get spectral response function (currently only Si supported for 
    ### traditional PV... more to come soon)
    SR = datalib.SR_Si(lam)
    ### jsc integrand
    integrand = AM*SR*eps
    ### integrate it!
    jsc = numlib.Integrate(integrand, lam, 1e-9, upper)
    return jsc
        
    
### reasonable approximation for Jsc given 
### you accept the view factor of 0.85... ignores 
### explicit angle dependence of emissivity
def JSC(TE, lam, PV):
    ### hard-coding view factor for now!
    F = 0.84
    ### get spectral response function for appropriate PV material
    if (PV=='InGaAsSb'):
        SR = datalib.SR_InGaAsSb(lam)
    elif (PV=='GaSb'):
        SR = datalib.SR_GaSb(lam)
    else:
        SR = datalib.SR_InGaAsSb(lam)
    ### get upper limit of lambda array... will integrate over entire
    ### range, in principle spectral response function will vanish at the
    ### appropriate boundaries of lambda
    upper = np.amax(lam)
    integrand = TE*SR*F*np.pi
    jshc = numlib.Integrate(integrand, lam, 1e-9, upper)
    return jshc

### reasonable approximation for Jsc given 
### you accept the view factor of 0.85... includes 
### explicit angle dependence of emissivity
def JSC_EA(TE_p, TE_s, lam, PV, t, w):
    ### hard-coding view factor for now!
    F = 0.84
    ### get spectral response function for appropriate PV material
    if (PV=='InGaAsSb'):
        SP = datalib.SR_InGaAsSb(lam)
    elif (PV=='GaSb'):
        SP = datalib.SR_GaSb(lam)
    else:
        SP = datalib.SR_InGaAsSb(lam)

    jsch = 0.
    dl = np.abs(lam[1]-lam[0])
    for i in range(0,len(t)):
        isom = 0.
        for j in range(0,len(lam)):
            isom = isom + 0.5 * TE_p[i][j] * SP[j] * F * dl
            isom = isom + 0.5 * TE_s[i][j] * SP[j] * F * dl
        jsch = jsch + w[i] * isom * np.sin(t[i])

    return jsch * 2 * np.pi

### Function to compute Voc given 
### a particular Jsc and T_cell
def Voc(Jsc, T_cell):
    ### just hard-coding J0 for now... will depend on the PV of course, and need
    ### to determine reasonable values for different cases...
    ### the following is appropriate for InGaAsSb
    lbg = 2254e-9
    ebg = h*c/lbg
    J0 = 1.5e5 * np.exp(-ebg/(k*T_cell))
    vopc = k*T_cell * np.log(Jsc/J0) / q
    return vopc

### function to compute the fill factor
### given a particular Voc and T_cell
def FF(Voc, T_cell):
    red_v = q*Voc/(k*T_cell)
    ### hard-coding beta for now
    beta  = 0.96
    ### this FF is appropriate for InGaAsSb... needs to become more general.
    fillf = beta * (red_v - np.log(red_v + 0.72))/(red_v + 1)
    return fillf

### Computs Jsc, Voc, FF, and Pin 
### and then computes eta_tpv from Jsc*Voc*FF/Pin
### ignores explicit angle dependence of emissivity
def Eta_TPV(TE, lam, PV, T_cell):
    jsc = JSC(TE, lam, PV)
    voc = Voc(jsc, T_cell)
    ff = FF(voc, T_cell)
    pin = p_in(TE, lam)
    
    eta = jsc*voc*ff/pin
    return eta

### Computes Jsc, Voc, FF, and Pin
### using explicit angle dependence for
### Jsc and Pin
def Eta_TPV_EA(TE_p, TE_s, lam, PV, T_cell, t, w):
    jsc = JSC_EA(TE_p, TE_s, lam, PV, t, w)
    voc = Voc(jsc, T_cell)
    ff = FF(voc, T_cell)
    pin = p_in_ea(TE_p, TE_s, lam, t, w)
    eta = jsc*voc*ff/pin
    return eta

def integrated_solar_power(lam):
    AM = datalib.AM(lam)
    upper = np.amax(lam)
    
    p_in = numlib.Integrate(AM, lam, 1e-9, upper)
    return p_in

### The absorbed power has some angle dependence in the case
### of concentrated solar - 
### see Eq. (2) in Raphaeli and Fan, Optics Express Vol 17, 2009, on page 15148
def absorbed_power_ea(lam, n, d, solarconc):
    ### get AM1.5 spectrum ... scale by concentration factor
    ### Note that Eq. (2) in Raphaeli and Fan does not explicitly indicate
    ### the AM1.5 spectrum should be scaled by the concentration factor, they 
    ### only explicitly indicate that it should impact the angle integration range
    ### through the relation thetaC = asin( sqrt ( Ns * Omega_S / pi) )
    ### where Ns is concentration factor (number of suns), Omega_S is solid
    ### angle subtended by sun (68.5 microsteridians) 
    ### However, if one does not scale the AM1.5 spectrum by Ns, then
    ### The absorbed power is far too low to make any sense.
    ### Some sanity checks are as follows:
    ### Assuming Absorber and Emitter are both blackbodies and have the same area, 
    ### The following equilibrium temperatures are found as a function of concentration
    ### when the AM1.5 is scaled (unscaled) by Ns, respectively:
    '''
    Ns     Temp_in_K   (Temp_in_K)
    100    694         (219)
    200    901         (239)   
    300    1048        (252)
    400    1168        (261)
    500    1270        (268)
    600    1359        (274)
    700    1440        (280)
    800    1514        (284)
    900    1582        (288)
    1000   1646        (292)
    
    from the above, 
    '''
    AM = datalib.AM(lam)*solarconc
    
    ### array for storing refractive index values
    nc = np.zeros(len(d),dtype=complex)
    ### get maximum angle for theta integration
    thetaC = np.arcsin(np.sqrt(solarconc * 68.5e-6/np.pi))
    #print("thetaC is ",thetaC)
    ### in essence we want to generate the absorbance for s- and p-
    ### polarized light between theta=0 and theta=thetaC
    ### and integrate over those absorbances to get total absorbed power
    
    ### set degree of polynomial - 7 seems to work well for 0 - pi/2
    ### should be very adequate here as well
    deg = 7
    ### range is 0 to thetaC
    a = 0
    b = thetaC
    x, w = np.polynomial.legendre.leggauss(deg)
    t = 0.5*(x + 1)*(b - a) + a
    w = w * 0.5 * (b-a)
    #print(t, w)
    osom = 0
    ### outter loop to integrate over theta
    dl = abs(lam[1]-lam[0])
    for th, we in zip(t,w):
        
        ###
        isom = 0.
        #for l, inc in zip(lam,AM):
        for i in range(0,len(lam)):
            ### wavenumber at current lambda
            k0= np.pi*2/lam[i]
            
            for j in range(0,len(d)):
                nc[j] = n[j][i]
            ### get s and p absorbance at current wavelength
            As = tmm.Abs(k0, th, 's', nc, d)
            Ap = tmm.Abs(k0, th, 'p', nc, d)
            ### add contributions from s- and p-polarization
            isom = isom + 0.5 * As * AM[i] * dl + 0.5 * Ap * AM[i] * dl
            ### Uncomment below for BB absorbed power
            #isom = isom + 0.5 * 1 * AM[i] * dl + 0.5 * 1 * AM[i] * dl
        ### add inner sum to outter sum
        osom = osom + we * isom * np.sin(th) * np.cos(th) 
        
    ### the integral over phi can be taken analytically since it will not impact emissivity
    ### and just gives a factor of 2*pi
    return 2*np.pi * osom

### Computes absorber efficiency - basically the ratio of net power absorbed
### gross absorbed power (currently)... JJF Note: Should it actually just
### be incident power in the denomenator?  Otherwise this FOM could 
### favor structures with low emissivity
def Abs_eff(lam, EM, solarconc, T):
    AM = datalib.AM(lam)
    upper = np.amax(lam)
    BBs = datalib.BB(lam, T)
    TE = BBs*EM
    alpha = solarconc * (numlib.Integrate(AM*EM , lam, 100e-9, upper)) 
    beta = np.pi*numlib.Integrate(TE , lam,  100e-9, upper)
    return (alpha - beta)/(alpha)


def ambient_jsc_grad(dim, eps_prime, lam, lbg):
    ### allocate grad!
    grad = np.zeros(dim)
    ### get upper bound of integral
    upper = np.amax(lam)
    ### get the AM1.5 spectrum
    AM = datalib.AM(lam)
    ### get the spectral response of Si
    SR = datalib.SR_Si(lam)
    ### Loop over the layers in gradient_list... compute jsc_prime for each one and store in grad!
    for i in range(0,dim):
        integrand = AM * SR * eps_prime[i,:]
        jsc_prime = numlib.Integrate(integrand, lam, 1e-9, upper)
        #print(" just computed Jsc' ... is is ",jsc_prime)
        grad[i] = jsc_prime
    
    return grad

### This gradient function needs to be tested!
def SpectralEfficiency_grad(dim, lam, lbg, emissivity, emissivity_prime, BBs):
    ### ininitalize gradient vector
    grad = np.zeros(dim)
    TE = emissivity * BBs
    ynum = TE*lam/lbg  
    upper = np.amax(lam)
    ### normal numerator (rho)
    rho = numlib.Integrate(ynum, lam, 1e-9, lbg)
    ### normal denomenator (P)
    P = numlib.Integrate(TE, lam, 1e-9, upper)
    
    ### loop over degrees of freedom and get gradient elements
    for i in range(0,dim):
        ### derivative of thermal emission wrt layer thickness, also integrand for P_prime
        TE_prime = BBs * emissivity_prime[i,:]
        ### integrand for  rho_prime
        num_prime = TE_prime * lam/lbg
        ### rho_prime
        rho_prime = numlib.Integrate(num_prime, lam, 1e-9, lbg)
        ### P_prime
        P_prime = numlib.Integrate(TE_prime, lam, 1e-9, upper)
        ### compute gradient element
        grad[i] = (rho_prime * P - P_prime * rho)/(P**2) 
    ### return gradient
    return grad




def ambient_jsc_grad(dim, eps_prime, lam, lbg):
    ### allocate grad!
    grad = np.zeros(dim)
    ### get upper bound of integral
    upper = np.amax(lam)
    ### get the AM1.5 spectrum
    AM = datalib.AM(lam)
    ### get the spectral response of Si
    SR = datalib.SR_Si(lam)
    ### Loop over the layers in gradient_list... compute jsc_prime for each one and store in grad!
    for i in range(0,dim):
        integrand = AM * SR * eps_prime[i,:]
        jsc_prime = numlib.Integrate(integrand, lam, 1e-9, upper)
        #print(" just computed Jsc' ... is is ",jsc_prime)
        grad[i] = jsc_prime
    
    return grad



def multi_junction_Jsc_1(lam, TE_1, TE_2, PV_1):
    #PV device 1 choice
    if (PV_1=='InGaAsSb'):
        SR = datalib.SR_InGaAsSb(lam)
    elif (PV_1=='GaSb'):
        SR = datalib.SR_GaSb(lam)
    else:
        SR = datalib.SR_InGaAsSb(lam)
   
        
 #start Integrals       
    Integrand_1 = TE_1*SR
    Integrand_2 = TE_2*SR
    upper = np.amax(lam)
    
    a = numlib.integrate(Integrand_1, lam, 100e-9, upper)
    b = numlib.integrate(Integrand_2, lam, 100e-9, upper)
    Jsc_1 = a+b
    return Jsc_1

#def multi_junction_Jsc_2(lam, TE_1, TE_2, PV_2, T_pv2):
    #PV device 2   choice
 #   if (PV_2=='InGaAsSb'):
  #      SR = datalib.SR_InGaAsSb(lam)
   # elif (PV_2=='GaSb'):
     #   SR = datalib.SR_GaSb(lam)
    #else:
      #  SR = datalib.SR_InGaAsSb(lam)
   
        
 #start Integrals       
#    Integrand_1 = TE_1*SR
 #   Integrand_2 = TE_2*SR
  #  upper = np.amax(lam)
    
#    a = numlib.integrate(Integrand_1, lam, 100e-9, upper)
 #   b = numlib.integrate(Integrand_2, lam, 100e-9, upper)
  #  Jsc_1 = a+b
   # return Jsc_1

