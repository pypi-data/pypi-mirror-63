#!/usr/bin/env python3
"""
Authors: Valentyn Stadnytskyi
Date created: 23 Oct 2019
Date last modified: 25 Oct 2019
Python Version: 3

Description:
------------

"""


from numpy import array, zeros

pixel_size = 4.65 #in microns
plane = zeros((1024,1024))

def distance(x,y):
    pass

def tau(length, diameter, viscosity, compressibility):
    """
    convert the length of a plug to volume in 250 um capillary.

    Parameters
    ----------
    length : float
        cylinder length
    diameter : float
        cylinder diameter

    Returns
    -------
    tau : float
        tau constant in seconds

    Examples
    --------
    the example of usage

    >>> droplet_volume(250,250)
    """
    tau = 32*compressibility*viscosity*(length/diameter)**2
    return tau


def droplet_volume(length = 100, diameter = 250):
    """
    convert the length of a plug to volume in 250 um capillary.

    Parameters
    ----------
    l : float
        droplet or plug length
    d : float
        channel diameter

    Returns
    -------
    v : float
        volume of the object

    Examples
    --------
    the example of usage

    >>> droplet_volume(250,250)
    """

def flow_cylinder(diameter = 250, length = 1, viscosity = 1, pressure = 0.1, output_units = 'nL'):
    """
    calculates flow rate via a cylindrical capillary with a given diameter, length and fluid viscosity under a given pressure drop. Also takes string value to define output units

    Parameters
    ----------
    length : float
        length of a cylinder in meters
    diameter : float
        diameter of round cross-section in micrometer
    viscosity : float
        viscosity in cP or mPa*s
    pressure : float
        pressure difference in atmospheres
    output_units
        output units for the flow. Supports: nL/s, uL/s. Default: nL/s

    Returns
    -------
    flow : float
        flow of fluid in nL/s

    Examples
    --------
    the example of usage.
    D=50um,L = 1, eta = 1, P = 2 -> 31.086 nL/s
    D=10oum,L = 0.7, eta = 23, P = 2 -> 30.893 nL/s


    >>> flow_cylinder(diameter = 50, length = 1, viscosity = 1.0, pressure = 2.0)
    >>> 31.086120666502506
    """
    from numpy import pi
    #first convert to SI units
    diameter = diameter*10**-6
    length = length
    viscosity = viscosity*10**-3 # 1 cP = 1mPa*s
    pressure = pressure*101325 # 1 atm = 101325 Pascal
    flow = (pi * pressure*diameter**4) / (128*viscosity*length)
    if output_units == 'pL':
        output_factor = 10**15 # 1 m^3 -> 1e3 L -> 1e12 nL
    elif output_units == 'nL':
        output_factor = 10**12 # 1 m^3 -> 1e3 L -> 1e12 nL
    elif output_units == 'uL':
        output_factor = 10**9 # 1 m^3 -> 1e3 L -> 1e12 nL
    elif output_units == 'mL':
        output_factor = 10**6 # 1 m^3 -> 1e3 L -> 1e12 nL
    elif output_units == 'L':
        output_factor = 10**3 # 1 m^3 -> 1e3 L -> 1e12 nL
    else:
        output_factor = 10**12
    return flow*output_factor

def pressure_cylinder(diameter = 250, length = 1, viscosity = 1, flow = 0.1, flow_units = 'nL/s', output_units = 'atm'):
    """
    calculates pressure drop across a cylindrical capillary with a given diameter, length and fluid viscosity with given flow rate. Also takes string value to define output units

    Parameters
    ----------
    length : float
        length of a cylinder in meters
    diameter : float
        diameter of round cross-section in micrometer
    viscosity : float
        viscosity in cP or mPa*s
    flow : float
        pressure difference in atmospheres
    flow_units : string
        flow units (pL/s, uL/s, ul/s, mL/s, L/s, m^3/s)
    output_units : string
        output units for the flow. Supports: atm, Pa. Default: atm

    Returns
    -------
    pressure : float
        pressure drop across the capillary

    Examples
    --------
    the example of usage.
    D=50um,L = 1, eta = 1, P = 2 -> 31.086 nL/s
    D=10oum,L = 0.7, eta = 23, P = 2 -> 30.893 nL/s


    >>> pressure_cylinder(diameter = 50, length = 1, viscosity = 1.0, flow = 31.086, flow_units = 'nL/s')
    >>> 1.9999922366316594
    """
    from numpy import pi
    #first convert to SI units
    diameter = diameter*10**-6
    length = length
    viscosity = viscosity*10**-3 # 1 cP = 1mPa*s
    if flow_units == 'nL/s':
        flow_coeff = 10**-12
    elif flow_units == 'uL/s':
        flow_coeff = 10**-9
    elif flow_units == 'mL/s':
        flow_coeff = 10**-6
    flow = flow*flow_coeff #
    pressure = ((128*viscosity*length)/(pi *diameter**4))*flow
    if output_units == 'atm':
        output_factor = 1/101325 # 1 m^3 -> 1e3 L -> 1e12 nL
    elif output_units == 'Pa':
        output_factor = 1 # 1 m^3 -> 1e3 L -> 1e12 nL
    else:
        output_factor = 1/101325 # 1 m^3 -> 1e3 L -> 1e12 nL
    return pressure*output_factor

def find_circles(image):
    """
    takes and input image and find circles in it.

    returns radius and center coordinates of circles
    """
    import numpy as np
    import matplotlib.pyplot as plt

    from skimage import data, color
    from skimage.transform import hough_circle, hough_circle_peaks
    from skimage.feature import canny
    from skimage.draw import circle_perimeter
    from skimage.util import img_as_ubyte


    # Load picture and detect edges
    image = img_as_ubyte(image)
    edges = canny(image, sigma=2, low_threshold=10, high_threshold=20)


    # Detect two radii
    hough_radii = np.arange(40, 280, 5)
    hough_res = hough_circle(edges, hough_radii)

    # Select the most prominent 3 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=7)

    # Draw them
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    image = color.gray2rgb(image)
    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)
        image[circy, circx] = (220, 20, 20)

    ax.imshow(image, cmap=plt.cm.gray)
    plt.show()

def get_test_images(i = 0):
    from ubcs_auxiliary.save_load_object import load_from_file
    filename = './laue_crystallography/tests/images/holes_example1.imgpkl'
    img = load_from_file(filename)
    return img

def find_pixels_with_neighbors(input_mask, N = 2):
    from numpy import zeros
    mask = input_mask.copy()*0
    for r in range(input_mask.shape[0]):
        for c in range(input_mask.shape[1]):
            if input_mask[r,c] == 1:
                temp_mask = input_mask[r-N:r+N,c-N:c+N]
                if temp_mask.sum() >= 4*N*N:
                    mask[r,c] = 1
    return mask

def ellipse(h = 250, v = 250, x0 = 400, y0 = 400, size = (1024,1360), theta = 0):
    """
    returns array with 'size' with an ellipse centered at x0,y0 with diameters h(horizontal) and v(vertical) tilted at theta degrees. The h-horizontal and v-vertical is accurate only if theta is zero degrees.

    Parameters
    ----------
    h : float
        diameter of horizontal(zero degrees) axis of the ellipse
    v : float
        diameter of vertical(zero degrees) axis of the ellipse
    x0 : float
        x-coordinate of the center of the ellipse
    y0 : float
        y-coordinate of the center of the ellipse
    size : tuple
        size of the output image Default: 1024,1360
    theta : float
        angle of rotation in degrees. Default: 0

    Returns
    -------
    mask : numpy array
        numpy array with 'size'

    Examples
    --------
    the example of usage. To draw an ellise center at (1115,659) with horizontal diameter of 52 pixels and vertical diameter of 56 pixels.

    >>> e = draw_an_ellipsoid(h = 52, v = 56, x0 = 1115, y0 = 659
    """
    from astropy.modeling.functional_models import Ellipse2D
    from astropy.coordinates import Angle
    from numpy import mgrid
    Ellipse = Ellipse2D
    theta = Angle(theta, 'deg')
    e = Ellipse2D(amplitude=1, x_0=x0, y_0=y0, a=h/2, b=v/2,
              theta=theta.radian)
    y, x = mgrid[0:size[0], 0:size[1]]
    return e(x,y)

def analyse_array(arr, threshold = 10, N = [2]):
    """

    """
    from numpy import argwhere
    #step 1 Create flatten mask of zeros
    mask = arr*0 + 1
    fl_mask = mask.flatten()
    # find all indices with value below 10 (different number might be needed.
    idx = argwhere(arr.flatten() <= threshold)
    #mask those values
    fl_mask[idx] = 0
    # this will help to define thick counter lines
    mask = []
    mask.append([fl_mask.reshape(1024,1360),0])
    for i in N:
        mask.append([find_pixels_with_neighbors(mask[0][0],N = i),i])
    return mask

def plot_image_with_sum(img, title = ''):
    """
    plots an image with two graphs
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    # Plot figure with subplots of different sizes
    fig = plt.figure()
    # set up subplot grid
    gridspec.GridSpec(4,4)

    # large subplot
    plt.subplot2grid((4,4), (0,0), colspan=3, rowspan=3)
    #plt.locator_params(axis='x', nbins=5)
    #plt.locator_params(axis='y', nbins=5)
    # plt.title('Normal distribution')
    # plt.xlabel('Data values')
    # plt.ylabel('Frequency')
    plt.imshow(img)

    # small subplot 1
    plt.subplot2grid((4,4), (0,3), colspan=1, rowspan=3)
    #plt.locator_params(axis='x', nbins=5)
    #plt.locator_params(axis='y', nbins=5)
    # plt.title('t distribution')
    # plt.xlabel('Data values')
    # plt.ylabel('Frequency')
    x = img.sum(axis = 1)
    y = np.arange(0,len(x),1)
    plt.plot(x,y)
    plt.ylim(0,1024)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])

    # small subplot 2
    plt.subplot2grid((4,4), (3,0), colspan=3, rowspan=1)
    #plt.locator_params(axis='x', nbins=5)
    #plt.locator_params(axis='y', nbins=5)
    # plt.title('F distribution')
    # plt.xlabel('Data values')
    # plt.ylabel('Frequency')
    plt.plot(img.sum(axis = 0))
    plt.xlim(0,1360)
    # fit subplots and save fig
    fig.tight_layout()
    #fig.set_size_inches(w=11,h=7)
    fig_name = 'plot.png'
    plt.show()

if __name__ == '__main__':
    # The Record Name is specified by prefix
    prefix = 'microfludics'
    from pdb import pm
    from tempfile import gettempdir
    import logging
    logging.basicConfig(filename=gettempdir()+'/{}.log'.format(prefix),
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

    from tempfile import gettempdir

    #For testing
    from numpy import arange
    from matplotlib import pyplot as plt
    from ubcs_auxiliary.save_load_object import load_from_file
    root = '/Users/femto-13/microfluidics_data/puck5/'
    bckg = load_from_file(root + 'bck_19.imgpkl').astype('float64')
    for i in range(19):
        bckg += load_from_file(root + f'bck_{i}.imgpkl').astype('float64')
    bckg = bckg.T/20.0
    img1 = load_from_file(root + 'image_15.imgpkl').astype('float64').T
    data = -1*(img1-bckg)
    mask = analyse_array(data[:,:,0]+data[:,:,1]+data[:,:,2], threshold = 10, N = [1,2,3])
    plot_image_with_sum(mask[0][0].astype('int16'))
    plot_image_with_sum(mask[3][0])
