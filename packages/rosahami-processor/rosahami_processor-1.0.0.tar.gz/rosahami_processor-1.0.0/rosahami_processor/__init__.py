"""
@author: Michal Smid, HZDR 2020
Rosahami_processor

Rossendorfer
  Saxs
    HAPG
      Mirror 
"""

import pickle
import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import sys
import math
import os
#import numba as nb
### Utils & small

def init():
    """
    Initializes the mmmpxrt dictionary of parameters.
    
    Retrurns:
        dict: dictionary of dictionaries with default values of all parameters.
    """    
    #pyversion('/usr/bin/python3.6')
    crystal={}
    geometry={}
    source={}
    simulation={}
    
### Simulation parameters

    simulation['name']='someMMpXRTsimulation' #Defines the output filename of results.
    simulation['version']="1.3"
    simulation['comment']='someMMpXRTsimulation' #This is just written in the figure as subtitle for convinience.
    simulation['num_processes']=1 #Number of processors to be used by the simulation.
    simulation['out_data_directory']='./datafiles/' #Where the ouptupt data are stored.

    #How much rays should be calculated. The more the better, but longer.
    simulation['numraysB']=1e5 #Number of rays for the broadband simulation.
    simulation['numraysM']=1e5 #Number of rays for the monocrhomatic simulation.
    simulation['numraysE']=4 # Optional exponent setting. If numraysE>0, numraysB=(10**(numraysE) numraysM=(10**(numraysE-1)

    simulation['progressmod']=200 #after how much to update the progressbar
    simulation['outputdump']=1e8

    #Window nad pixels for figure of Point spread function [mm]. -1 lets the automatic work.
    simulation['PSFWindowX']=-1 
    simulation['PSFWindowY']=-1
    simulation['PSFStepY']=-1
    simulation['PSFStepX']=-1

    #numerical parameters, default values should be ok for most cases. 
    #When details of mossaic stuff at non-optimal angles are important, having higher values makes more precision, like e.g. width=30, numpoints=50 was used for mossaicity section of the CPC paper
    simulation['numerical_mossaic_phimap_width']=10
    simulation['numerical_mossaic_phimap_numpoints']=14

### Crystal
    ## General
    crystal['d2']=4.00 #crystal spacing 2d [Angstrom]
       #old, wrong definitions:
        #crystal['radius_width']=1500 #Crystal radius along its width [mm] (dispersion plane) - defines range 
       #crystal['radius_length']=100 #Crystal radius along its length [mm] (spatial focusing) - defines the geometry
    crystal['radius_l']=1e9 #Crystal radius of curvature along its length [mm] (in dispersion plane) - defines spectral range etc.
    crystal['radius_w']=1e9 #Crystal radius curvature along its width [mm] (spatial focusing) - defines the geometry
    crystal['length']=40 #Crystal length [mm]
    crystal['width']=25 #Crystal width[mm]
    
  ## Parameters for mossaic crystals
    crystal['mosaicity']=0 #Mosaicity (mosaic distribution spread) fwhm, [°].   Zero means that monocrystal is used.
    crystal['crystalliteRockingcurveWidth']=0e-4 #[rad]
    crystal['crystalPeakReflectivity']=1 #[-] Usually around 0.45 for HOPGs.

    crystal['thickness']=0 #How penetration of rays into crystals is done:
    #-1:  The exponential probability distribution is used, limited by maxThickness
    # 0:  Everything is reflected from the crystal surface 
    # >0: Homogeneous depth distribution with given maximal this number stating the maximal depth [mm]

    crystal['penetrationDepth']=-1 # [mm] penetration depth of photons into the crystal, assuming exponential distribution; if set to -1, the reference is used.
    crystal['penetrationDepthMultiplier']=1 
    crystal['maxThickness']=0 #real thickness of crystal if exponential distribution is used (thickness=-1)

    crystal['mosaicCrystal_penetration_depth_reference']=695e-3 #mm; measured or estimated penetration depth at energy specified below
    crystal['mosaicCrystal_penetration_depth_reference_energy']=8045 #eV; energy, where reference penetration depth is estimated
    crystal['mosaicCrystalTransmission']='C_700um_transmission.dat' #File with crystal material transmission as a function of x-ray energy, used to get mean penetration depth    
    crystal['mosaicCrystalTransmission_thickness']=700e-3 #mm, thickness of sample whose transmission is tabelated in file 'mosaicCrystalTransmission'
    
    
  ## Parameters for monocrystals (non-mosaic)
    crystal['rockingCurveFWHM']=0 #[rad] 
    crystal['integrated_reflectivity']=1 #[rad] 
    # The codes assumes square rocking curve with above given width & integral.
    # The peak reflectivity is calculated as  integrated_reflectivity / rockingCurveFWHM.   
    
### Geometry
    #Main distances [mm]. Positive value will be taken, -1 will make calculation for vonHamos geomtery:
    geometry['CrystalSource']=-1 
    geometry['CrystalDetector']=-1
    geometry['defocusation']=1.00 #Multiplication factor for the Crystal-Detector distance.
    geometry['detectorOffset']=0  #Additive factor for the Crystal-Detector distance.  
    geometry['detRot']=0#[°] rotation of detector. 0° mean it is perpendicular to incoming beam, positive number more suitble for vonHamos, -1° calculate the ideal von Hamos rotation
    geometry['ThBragg0']=-1; #[rad] Incidence angle of the central ray on the crystal. if set to -1, then it is calculated based on Bragg law.
    
    ## Detector. Those parameters does not influnece the simulation, only its evaluation 
    geometry['detectorLength']=28 
    geometry['detectorWidth']=-1; #-1 means automatic, otherwise [mm] 
    geometry['detectorPxSize']=13e-3 #-1 means automatic, otherwise [mm] 
    geometry['evaluation_width']=1  #[mm] Width of spectra selected for evaluation of spectral resolution


### Source 
    source['EcentralRay']=8000 #Central energy of spectrometer. [eV]
    source['EmaxBandwidth']=1000 #Energy bandwidth which will be used to test the setup [eV].
    source['size']=0 # [mm] Uncertainity in the source position (i.e. source is cube with given size)

### This is end of user defining variables, follow imortatn code

    #internal variables:
    simulation['show_progress']=1
    simulation['collectLostBeams']=False

    ## simulation settings (configured by mmmxrt_spectrometer)
    source['secondBeamRatio']=0 #ratio - how much of second monoergetic beam is added.
    source['secondBeamEOffset']=10#eV
    source['rOffsetRatio']=0.0 #ratio of rayes whose origin is offset
    source['rOffset']=[0 ,0, 0] #offset of part of the beam given by previous value
    source['continuum']=False
    source['continuumMarks']=False#add a marks with 
    source['continuumMarksSpread']=200
    source['continuumMarksCount']=3
    source['continuumAdd']=False#add a little bit of continuum to the simuled x-ray spectrum
    source['continuumAddedRatio']=0.3#fraction of rays that will have that added continuum
    source['useBeamSpectrum']=False
    source['beamSpectrum']='';#array containing the spectrum

    source['divergenceXcut']=1#this makes the beam elliptical - use just to improve the efficiency of the simulation, might make the efficiency calculation wrong
    source['divergenceRing']=np.array([]) #Divergence will be ring-like with angular radius given by its positive value [rad]
    source['divergenceGrating']=-1 
    source['divergenceGaussian']=False
    source['divergenceRectangular']=False
    source['divergenceAutomatic']=False
    source['divergenceX']=0
    source['divergenceY']=0
    source['divergenceFWHM']=-1
    
    source['do2DAngularResolutionTest']=False
    source['AngularGridRad']=0 # rad
    source['showspatial']=False
    source['show2Dspatial']=False
    source['showrealspatial']=False
    source['doAngularResolutionTest']=False


    #undocumented features    
    crystal['variableD2']=False #if True, the 2d spacing is linearly variable (useful for ML), goverened by following parameter.
    crystal['d2Variation']= 0.0 #[Å/mm]
    crystal['gap']= 0 #mm ..horizontal gap in the crystal. Special feauture for SAXS mirror


    if not os.path.exists(simulation['out_data_directory']):
        os.mkdir(simulation['out_data_directory'])

    parameters={}
    parameters['source']=source
    parameters['geometry']=geometry
    parameters['simulation']=simulation
    parameters['crystal']=crystal
    
    return parameters
