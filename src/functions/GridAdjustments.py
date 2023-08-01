def adjustWCT(h_new,zice_new,h_alter,zice_alter,eta,xi):
    """
    function adjustWCT(h,zice,h_alter,zice_alter,eta,xi
    
    usage:
    h_new, zice_new=adjustWCT(h,zice,h_alter,zice_alter,eta,xi)
    
    This function adjust h[eta,xi] + h_alter and zice[eta,xi]+zice_alter. The intended use would be to 
    thicken the water column at a set location. Given rx1 is a function of steepness, depth and wct,
    the intended use would be, for example:
    h_alter=200 #lower the bathymetry by 200 m
    zice_alter=-150 #lower (neg zice is lower) zice by only 150m
    So resultant water column here starts 200m lower and is 50m thicker than previously. 
    
    To pass a range, use the slice literal:
    eta=slice(100,132)

    """
    h_new[eta,xi] = h_new[eta,xi] + h_alter
    zice_new[eta,xi] = zice_new[eta,xi] + zice_alter
    return h_new, zice_new

def adjustMask(mask_new,mask_alter,eta,xi):
    """
    function adjustMask(mask_new,mask_alter,eta,xi)
    
    usage:
    mask_new=adjustMask(mask_new,mask_alter,eta,xi)
    
    This function adjusts mask at[eta,xi] to the new value mask_alter.
    e.g.
    mask[eta,xi] = mask_new,
    will change the value of a mask at [eta,xi] to the new value 
    mask_alter.

    """    
    mask_new[eta,xi]=mask_alter
    return mask_new

def setBathy(h_new,h_alter,eta,xi):
    """
    function setBathy(h,h_alter,eta,xi
    
    usage:
    h_new = setBathy(h,h_alter,eta,xi)
    
    This function adjusts h[eta,xi] to h_alter.
    To pass a range, use the slice literal:
    eta=slice(100,132)

    """
    h_new[eta,xi] = h_alter
    return h_new


def smoothBathyPatch(h_new,eta,xi):
    """
    function smoothBathyPatch(h_new,eta,xi)
    
    usage:
    h_new = smoothBathyPatch(h_new,eta,xi)
    
    

    """
        # define inpaint_nans
    from scipy.signal import convolve2d
    import numpy as np
    def inpaint_nans(inField):
        im = inField.copy()
        import scipy
        ipn_kernel = np.array([[1,1,1],[1,0,1],[1,1,1]]) # kernel for inpaint_nans
        nans = np.isnan(im)
        while np.sum(nans)>0:
            im[nans] = 0
            vNeighbors = convolve2d((nans==False),ipn_kernel,mode='same',boundary='symm')
            im2 = convolve2d(im,ipn_kernel,mode='same',boundary='symm')
            im2[vNeighbors>0] = im2[vNeighbors>0]/vNeighbors[vNeighbors>0]
            im2[vNeighbors==0] = np.nan
            im2[(nans==False)] = im[(nans==False)]
            im = im2
            nans = np.isnan(im)
        return im


    h_new[eta,xi] = np.NaN
    h_new = inpaint_nans(h_new)
    
    return h_new

