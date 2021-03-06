import h5py
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import netCDF4
from pyproj import Proj, transform
from mpl_toolkits.basemap import Basemap
import config 
from mpl_toolkits.axes_grid1 import ImageGrid
import pysteps

def uncrop_center(img, uncropx=700, uncropy=765):
    y,x= img.shape
    startx = 20+uncropx//2-(x//2)
    starty = 40+uncropy//2-(y//2)    
    
    endx = uncropx - (startx + x)
    endy = uncropy - (starty + y)
    npad = [(0, 0)] * img.ndim
    
    npad[0] = (starty, endy)
    npad[1] = (startx, endx)
               
    return np.pad(img, pad_width=npad, mode='constant', constant_values=0)

def plot_on_map(rdr, ftype='.nc', res='l',colorbar=True, vmax=None, axis=None, vmin=None):
    '''
    Plot radar file on top of map.
    rdr: image file
    ftype: file extension, can be either '.nc' or '.h5'
    res: resolution, can be c (crude), l (low), i (intermediate), h (high), f (full) 
    '''
    
    dir_aart = config.dir_aart
    aart_fbase = config.prefix_aart
    proj = Proj("+proj=stere +lat_0=90 +lon_0=0.0 +lat_ts=60.0 +a=6378.137 +b=6356.752 +x_0=0 +y_0=0")
    
    if ftype != '.nc' and ftype !='.h5':
        print('Error: invalid file extension {}, should be .nc or .h5'.format(ftype))
        
     # Add padding to target image
    if ftype =='.nc' and rdr.shape[0] == 384:
        rdr = uncrop_center(rdr)   
    # Remove padding if the image  was padded
    if rdr.shape[0] > 765 and ftype =='.h5':
        rdr = rdr[:765]

        
    # All images are plotted on the same map
    # Get the map from random nc file
    path = dir_aart + '2019/{}201901010000.nc'.format(aart_fbase)
    with netCDF4.Dataset(path, 'r') as ds:
        # Get coordinates of the pixels
        xx, yy = np.meshgrid(ds['x'][:], ds['y'][:])
        lon, lat = proj(xx, yy, inverse=True)
        # Plot values on map
        iso_dict = ds['iso_dataset'].__dict__
        min_x = float(iso_dict['min_x'].replace('f', ''))
        min_y = float(iso_dict['min_y'].replace('f', ''))
        max_x = float(iso_dict['max_x'].replace('f', ''))
        max_y = float(iso_dict['max_y'].replace('f', ''))
        
        if ftype == '.nc':
            rain = ds['image1_image_data'][:]
            mask = rain.mask
            
    if  ftype == '.h5':  
        path = config.dir_rtcor +  '2019/01/{}201901010000.h5'.format(config.prefix_rtcor)
        with h5py.File(path, 'r') as f:
                rain = f['image1']['image_data'][:]
                mask = (rain == 65535)

    # Mask the data
    mx = np.ma.masked_array(rdr, mask)
    # Plot the precipitation on map  
    mp = Basemap(projection='stere',
                         lat_0=90,
                         lon_0=0, 
                         lat_ts=60,   
                         llcrnrlon=min_x,   # lower longitude
                         llcrnrlat=min_y,    # lower latitude
                         urcrnrlon=max_x,   # uppper longitude
                         urcrnrlat=max_y,   # uppper latitude
                         resolution=res
                        )
    mp.drawcoastlines()
    mp.drawstates()
    mp.drawcountries()

    xx, yy = mp(lon, lat)

    vmin=-0.00001    
    if vmin:
        vmin = vmin
    cmap = cm.viridis
    if axis:
        im = axis.imshow(mx, vmin = vmin, vmax=vmax, cmap=cmap, origin='upper', 
           extent=[xx.min(), xx.max(), yy.min(), yy.max()])
        if colorbar:
            axis.colorbar()
        return im
    else:
        im = plt.imshow(mx, vmin = vmin, vmax=vmax, cmap=cmap, origin='upper', 
               extent=[xx.min(), xx.max(), yy.min(), yy.max()])
        if colorbar:
            plt.colorbar()
        return im

def plot_target_pred(target, pred):
    data = [target, pred]
    vmax = np.max(data)

    
    n = target.shape[0]
    # Set up figure and image grid
    fig = plt.figure(figsize=(9,9)) 

    grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                     nrows_ncols=(n,2),
                     axes_pad=0.10,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="single",
                     cbar_size="7%",
                     cbar_pad=0.1
                     )
    cmap, norm, _, _ = pysteps.visualization.precipfields.get_colormap('intensity', 'mm/h', 'pysteps')
    
    for i in range(n):
        im = grid[i*2].imshow(np.squeeze(data[0][i]), cmap = cmap, norm = norm)
        grid[i*2].axis('off')
    grid[0].set_title('y')
    for i in range(n):
        im = grid[1+2*i].imshow(np.squeeze(data[1][i]), cmap = cmap, norm = norm)
        grid[1+2*i].axis('off') 
    grid[1].set_title('y_pred')
    # Colorbar
    pysteps_colorbar(im, cax=grid.cbar_axes[0])
    #grid[1].cax.toggle_label(True)

    #plt.tight_layout(rect=(0,0,1,1))    # Works, but may still require rect paramater to keep colorbar labels visible
    return fig

def pysteps_colorbar(im, cax=None):
    ptype='intensity'
    units='mm/h'
    colorscale='pysteps'
    extend = "max"
    
    # get colormap and color levels
    _, _, clevs, clevs_str = pysteps.visualization.precipfields.get_colormap(ptype, units, colorscale)

    cbar = plt.colorbar(
            im, ticks=clevs, spacing="uniform", extend=extend, shrink=0.8, cax=cax
        )
    if clevs_str is not None:
        cbar.ax.set_yticklabels(clevs_str)

    if ptype == "intensity":
        cbar.ax.set_title(units, fontsize=10)
        cbar.set_label("Precipitation intensity")