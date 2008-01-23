# make plots of etopo bathymetry/topography data on
# various map projections, drawing coastlines, state and
# country boundaries, filling continents and drawing
# parallels/meridians

from mpl_toolkits.basemap import Basemap, shiftgrid
from pylab import show,arange,draw,figure,load,ravel,cm,axes,\
                  colorbar,title,gca,pi,meshgrid
import matplotlib.colors as colors

# read in topo data (on a regular lat/lon grid)
# longitudes go from 20 to 380.
topodatin = load('etopo20data.gz')
lonsin = load('etopo20lons.gz')
latsin = load('etopo20lats.gz')

# shift data so lons go from -180 to 180 instead of 20 to 380.
topoin,lons = shiftgrid(180.,topodatin,lonsin,start=False)
lats = latsin

print 'min/max etopo20 data:'
print min(ravel(topoin)),max(ravel(topoin))

# create new figure
fig=figure()
# setup cylindrical equidistant map projection (global domain).
m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,\
            resolution='c',area_thresh=10000.,projection='cyl')
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topoin,cm.jet)
# get axes position, add colorbar axes to right of this.
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
#m.drawcountries()
#m.drawstates()
#m.fillcontinents()
# draw parallels
delat = 30.
circles = arange(0.,90.+delat,delat).tolist()+\
          arange(-delat,-90.-delat,-delat).tolist()
m.drawparallels(circles,labels=[1,0,0,1])
# draw meridians
delon = 60.
meridians = arange(-180,180,delon)
m.drawmeridians(meridians,labels=[1,0,0,1])
title('Cylindrical Equidistant')
print 'plotting Cylindrical Equidistant example ...'
print m.srs

# create new figure
fig=figure()
# setup miller cylindrical map projection.
m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,\
            resolution='c',area_thresh=10000.,projection='mill')
# transform to nx x ny regularly spaced native projection grid
nx = len(lons); ny = len(lats)
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
fig.add_axes([0.1,0.1,0.75,0.75])
# plot image over map.
im = m.imshow(topodat,cm.jet)
m.drawcoastlines()
# draw parallels
m.drawparallels(circles,labels=[1,1,1,1])
# draw meridians
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Miller Cylindrical',y=1.1)
print 'plotting Miller Cylindrical example ...'
print m.srs

# create new figure
fig=figure()
# setup mercator map projection (-80 to +80).
m = Basemap(llcrnrlon=-180.,llcrnrlat=-80,urcrnrlon=180.,urcrnrlat=80.,\
            resolution='c',area_thresh=10000.,projection='merc',\
            lon_0=0.5*(lons[0]+lons[-1]),lat_ts=20.)
# transform to nx x ny regularly spaced native projection grid
nx = len(lons); ny = int(80.*len(lats)/90.)
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
fig.add_axes([0.1,0.1,0.75,0.75])
# plot image over map.
im = m.imshow(topodat,cm.jet)
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents()
# draw parallels
m.drawparallels(circles,labels=[1,1,1,1])
# draw meridians
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Mercator',y=1.1)
print 'plotting Mercator example ...'
print m.srs

# create new figure
fig=figure()
# setup cassini-soldner basemap.
m = Basemap(llcrnrlon=-6,llcrnrlat=49,urcrnrlon=4,urcrnrlat=59,\
            resolution='l',area_thresh=1000.,projection='cass',\
            lat_0=54.,lon_0=-2.)
fig.add_axes([0.125,0.2,0.6,0.6])
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/20000.)+1; ny = int((m.ymax-m.ymin)/20000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map.
im = m.imshow(topodat,cm.jet)
# get current axis instance.
ax = gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
# draw parallels
delat = 2.
circles = arange(40.,70.,delat)
m.drawparallels(circles,labels=[1,0,0,1],fontsize=10)
# draw meridians
delon = 2.
meridians = arange(-10,10,delon)
m.drawmeridians(meridians,labels=[1,0,0,1],fontsize=10)
title('Cassini-Soldner Projection')
print 'plotting Cassini-Soldner example ...'
print m.srs

# create new figure
fig=figure()
# setup gnomonic basemap.
m = Basemap(llcrnrlon=-95.,llcrnrlat=-52,urcrnrlon=-35.,urcrnrlat=15.,\
            resolution='c',area_thresh=10000.,projection='gnom',\
            lat_0=-10.,lon_0=-60.)
fig.add_axes([0.125,0.2,0.6,0.6])
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map.
im = m.imshow(topodat,cm.jet)
# get current axis instance.
ax = gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
# draw parallels
delat = 20.
circles = arange(-80.,100.,delat)
m.drawparallels(circles,labels=[1,0,0,1],fontsize=10)
# draw meridians
delon = 20.
meridians = arange(-180,180,delon)
m.drawmeridians(meridians,labels=[1,0,0,1],fontsize=10)
title('Gnomonic Projection')
print 'plotting Gnomonic example ...'
print m.srs

# create new figure
fig=figure()
# setup transverse mercator basemap.
m = Basemap(width=2*6370997,height=3.1*6370997,\
            resolution='c',area_thresh=10000.,projection='cass',\
            lat_0=0.,lon_0=-90.)
fig.add_axes([0.125,0.2,0.6,0.6])
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map.
im = m.imshow(topodat,cm.jet)
# get current axis instance.
ax = gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
# draw parallels
delat = 20.
circles = arange(-80.,100.,delat)
m.drawparallels(circles,labels=[1,0,0,0],fontsize=10)
# draw meridians
delon = 20.
meridians = arange(-180,180,delon)
m.drawmeridians(meridians,labels=[1,0,0,0],fontsize=10)
title('Transverse Mercator Projection')
print 'plotting Transverse Mercator example ...'
print m.srs

# create new figure
fig=figure()
# setup oblique mercator basemap.
m = Basemap(llcrnrlon=-130.,llcrnrlat=39,urcrnrlon=-124.,urcrnrlat=60.,\
            resolution='l',area_thresh=1000.,projection='omerc',\
            lon_2=-140,lat_2=55,lon_1=-120,lat_1=40)
fig.add_axes([0.125,0.2,0.6,0.6])
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/20000.)+1; ny = int((m.ymax-m.ymin)/20000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map.
im = m.imshow(topodat,cm.jet)
# get current axis instance.
ax = gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# draw parallels
delat = 3.
circles = arange(40,60,delat)
m.drawparallels(circles,labels=[1,0,0,0],fontsize=10)
# draw meridians
delon = 3.
meridians = arange(-140,-120,delon)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
title('Oblique Mercator Projection')
print 'plotting Oblique Mercator example ...'
print m.srs

# create new figure
fig=figure()
# setup polyconic basemap.
m = Basemap(llcrnrlon=-35.,llcrnrlat=-30,urcrnrlon=80.,urcrnrlat=50.,\
            resolution='c',area_thresh=1000.,projection='poly',\
            lat_0=0.,lon_0=20.)
fig.add_axes([0.125,0.2,0.6,0.6])
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
# plot image over map.
im = m.imshow(topodat,cm.jet)
# get current axis instance.
ax = gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
# draw parallels
delat = 20.
circles = arange(-80.,100.,delat)
m.drawparallels(circles,labels=[1,0,0,0],fontsize=10)
# draw meridians
delon = 20.
meridians = arange(-180,180,delon)
m.drawmeridians(meridians,labels=[1,0,0,1],fontsize=10)
title('Polyconic Projection')
print 'plotting Polyconic example ...'
print m.srs

# create new figure
fig=figure()
# setup equidistant conic
m = Basemap(llcrnrlon=-90.,llcrnrlat=18,urcrnrlon=-70.,urcrnrlat=26.,\
            resolution='l',area_thresh=1000.,projection='eqdc',\
            lat_1=21.,lat_2=23.,lon_0=-80.)
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='olive')
# draw parallels
delat = 2.
circles = arange(17,27,delat)
m.drawparallels(circles,labels=[1,0,0,0])
# draw meridians
delon = 5.
meridians = arange(-100,-60,delon)
m.drawmeridians(meridians,labels=[0,0,0,1])
title('Equidistant Conic')
print 'plotting Equidistant Conic example ...'
print m.srs

# create new figure
fig=figure()
# setup lambert conformal map projection (North America).
m = Basemap(llcrnrlon=-145.5,llcrnrlat=1,urcrnrlon=-2.566,urcrnrlat=46.352,\
            resolution='c',area_thresh=10000.,projection='lcc',\
            lat_1=50.,lon_0=-107.)
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
m.drawstates()
#m.fillcontinents()
# draw parallels
delat = 20.
circles = arange(0.,90.+delat,delat).tolist()+\
          arange(-delat,-90.-delat,-delat).tolist()
m.drawparallels(circles,labels=[1,1,0,1])
# draw meridians
delon = 30.
meridians = arange(10.,360.,delon)
m.drawmeridians(meridians,labels=[1,1,0,1])
title('Lambert Conformal Conic')
print 'plotting Lambert Conformal example ...'
print m.srs

# create new figure
fig=figure()
# setup albers equal area map projection (Europe).
m = Basemap(llcrnrlon=-10.,llcrnrlat=20,urcrnrlon=55.,urcrnrlat=75,\
            resolution='l',projection='aea',\
            lat_1=40.,lat_2=60,lon_0=35.)
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
im.set_clim(-4000.,3000.) # adjust range of colors.
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
# draw parallels
delat = 20.
circles = arange(0.,90.+delat,delat).tolist()+\
          arange(-delat,-90.-delat,-delat).tolist()
m.drawparallels(circles,labels=[1,1,1,1])
# draw meridians
delon = 30.
meridians = arange(10.,360.,delon)
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Albers Equal Area Conic',y=1.075)
print 'plotting Albers Equal Area example ...'
print m.srs

# create new figure
fig=figure()
# setup stereographic map projection (Southern Hemisphere).
#m = Basemap(llcrnrlon=120.,llcrnrlat=0.,urcrnrlon=-60.,urcrnrlat=0.,\
#            resolution='c',area_thresh=10000.,projection='stere',\
#            lat_0=-90.,lon_0=75.,lat_ts=-90.)
# this is equivalent, but simpler.
m = Basemap(lon_0=75.,boundinglat=-20,
            resolution='c',area_thresh=10000.,projection='spstere')
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
#m.fillcontinents()
# draw parallels
m.drawparallels(circles)
# draw meridians
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Polar Stereographic',y=1.075)
print 'plotting Stereographic example ...'
print m.srs

# create new figure
fig=figure()
# setup lambert azimuthal map projection (Northern Hemisphere).
#m = Basemap(llcrnrlon=-150.,llcrnrlat=-18.,urcrnrlon=30.,urcrnrlat=--18.,\
#            resolution='c',area_thresh=10000.,projection='laea',\
#            lat_0=90.,lon_0=-105.)
# this is equivalent, but simpler.
m = Basemap(lon_0=-105,boundinglat=20.,
            resolution='c',area_thresh=10000.,projection='nplaea')
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
m.drawstates()
#m.fillcontinents()
# draw parallels
m.drawparallels(circles)
# draw meridians
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Lambert Azimuthal Equal Area',y=1.075)
print 'plotting Lambert Azimuthal example ...'
print m.srs

# create new figure
fig=figure()
# setup azimuthal equidistant map projection (Northern Hemisphere).
#m = Basemap(llcrnrlon=-150.,llcrnrlat=40.,urcrnrlon=30.,urcrnrlat=40.,\
#            resolution='c',area_thresh=10000.,projection='aeqd',\
#            lat_0=90.,lon_0=-105.)
# this is equivalent, but simpler.
m = Basemap(lon_0=-105,boundinglat=55.,
            resolution='c',area_thresh=10000.,projection='npaeqd')
# transform to nx x ny regularly spaced native projection grid
nx = int((m.xmax-m.xmin)/40000.)+1; ny = int((m.ymax-m.ymin)/40000.)+1
topodat = m.transform_scalar(topoin,lons,lats,nx,ny)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map.
im = m.imshow(topodat,cm.jet)
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
m.drawcoastlines()
m.drawcountries()
m.drawstates()
#m.fillcontinents()
# draw parallels
m.drawparallels(circles)
# draw meridians
m.drawmeridians(meridians,labels=[1,1,1,1])
title('Azimuthal Equidistant',y=1.075)
print 'plotting Azimuthal Equidistant example ...'
print m.srs

# projections with elliptical boundaries (orthographic, sinusoidal,
# mollweide and robinson)

# create new figure
fig=figure()
# setup of basemap ('ortho' = orthographic projection)
m = Basemap(projection='ortho',
            resolution='c',area_thresh=10000.,lat_0=30,lon_0=-60)
# transform to nx x ny regularly spaced native projection grid
# nx and ny chosen to have roughly the same horizontal res as original image.
dx = 2.*pi*m.rmajor/len(lons)
nx = int((m.xmax-m.xmin)/dx)+1; ny = int((m.ymax-m.ymin)/dx)+1
# interpolate to native projection grid.
# values outside of projection limb will be masked.
topo = m.transform_scalar(topoin,lons,lats,nx,ny,masked=True)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# set missing value in color pallette.
palette = cm.jet
palette.set_bad(ax.get_axis_bgcolor(), 0.0)
# plot image over map with imshow.
# (if contourf were used, no interpolation would be necessary
#  and values outside projection limb would be handled transparently
#  - see contour_demo.py)
im = m.imshow(topo,palette,norm=colors.normalize(clip=False))
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
# draw coastlines and political boundaries.
m.drawcoastlines()
# draw parallels and meridians (labelling is 
# not implemented for orthographic).
parallels = arange(-80.,90,20.)
m.drawparallels(parallels)
meridians = arange(0.,360.,20.)
m.drawmeridians(meridians)
# draw boundary around map region.
m.drawmapboundary()
title('Orthographic')
print 'plotting Orthographic example ...'
print m.srs

# create new figure
fig=figure()
# setup of basemap ('geos' = geostationary projection)
m = Basemap(projection='geos',
            rsphere=(6378137.00,6356752.3142),\
            resolution='c',area_thresh=10000.,lon_0=0,satellite_height=35785831)
# transform to nx x ny regularly spaced native projection grid
# nx and ny chosen to have roughly the same horizontal res as original image.
dx = 2.*pi*m.rmajor/len(lons)
nx = int((m.xmax-m.xmin)/dx)+1; ny = int((m.ymax-m.ymin)/dx)+1
# interpolate to native projection grid.
# values outside of projection limb will be masked.
topo = m.transform_scalar(topoin,lons,lats,nx,ny,masked=True)
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# set missing value in color pallette.
palette = cm.jet
palette.set_bad(ax.get_axis_bgcolor(), 0.0)
# plot image over map with imshow.
# (if contourf were used, no interpolation would be necessary
#  and values outside projection limb would be handled transparently
#  - see contour_demo.py)
im = m.imshow(topo,palette,norm=colors.normalize(clip=False))
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.075, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
# draw coastlines and political boundaries.
m.drawcoastlines()
# draw parallels and meridians (labelling is 
# not implemented for geostationary).
parallels = arange(-80.,90,20.)
m.drawparallels(parallels)
meridians = arange(0.,360.,20.)
m.drawmeridians(meridians)
# draw boundary around map region.
m.drawmapboundary()
title('Geostationary')
print 'plotting Geostationary example ...'
print m.srs

# create new figure
fig=figure()
# setup of sinusoidal ('sinu' = sinusioidal projection)
m = Basemap(projection='sinu',
            resolution='c',area_thresh=10000.,lon_0=0.5*(lonsin[0]+lonsin[-1]))
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map with pcolormesh.
x,y = m(*meshgrid(lonsin,latsin))
p = m.pcolormesh(x,y,topodatin,shading='flat')
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
# draw coastlines and political boundaries.
m.drawcoastlines()
# draw parallels and meridians
parallels = arange(-60.,90,30.)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = arange(0.,360.,30.)
m.drawmeridians(meridians)
# draw boundary around map region.
m.drawmapboundary()
title('Sinusoidal')
print 'plotting Sinusoidal example ...'
print m.srs

# create new figure
fig=figure()
# setup of basemap ('moll' = mollweide projection)
m = Basemap(projection='moll',
            resolution='c',area_thresh=10000.,lon_0=0.5*(lonsin[0]+lonsin[-1]))
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map with pcolormesh.
x,y = m(*meshgrid(lonsin,latsin))
p = m.pcolormesh(x,y,topodatin,shading='flat')
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
# draw coastlines and political boundaries.
m.drawcoastlines()
# draw parallels and meridians
parallels = arange(-60.,90,30.)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = arange(0.,360.,30.)
m.drawmeridians(meridians)
# draw boundary around map region.
m.drawmapboundary()
title('Mollweide')
print 'plotting Mollweide example ...'
print m.srs

# create new figure
fig=figure()
# setup of basemap ('robin' = robinson projection)
m = Basemap(projection='robin',
            resolution='c',area_thresh=10000.,lon_0=0.5*(lonsin[0]+lonsin[-1]))
ax = fig.add_axes([0.1,0.1,0.7,0.7])
# plot image over map with pcolormesh.
x,y = m(*meshgrid(lonsin,latsin))
p = m.pcolormesh(x,y,topodatin,shading='flat')
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = axes([l+w+0.05, b, 0.05, h]) # setup colorbar axes.
colorbar(cax=cax) # draw colorbar
axes(ax)  # make the original axes current again
# draw coastlines and political boundaries.
m.drawcoastlines()
# draw parallels and meridians
parallels = arange(-60.,90,30.)
m.drawparallels(parallels,labels=[1,0,0,0])
meridians = arange(0.,360.,60.)
m.drawmeridians(meridians,labels=[0,0,0,1])
# draw boundary around map region.
m.drawmapboundary()
title('Robinson')
print 'plotting Robinson example ...'
print m.srs
show()


print 'done'
