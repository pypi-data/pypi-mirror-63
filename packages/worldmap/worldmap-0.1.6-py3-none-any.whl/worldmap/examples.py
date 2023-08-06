# %%
import worldmap
print(worldmap.__version__)

# %% Retrieve availble maps that can be used to superimpose data on top of it
[map_names,filenames] = worldmap.map_names()

# %% Retrieve names in map
county_names = worldmap.county_names(map_name='world')
county_names = worldmap.county_names(map_name='netherlands')
county_names = worldmap.county_names(map_name='belgium')
county_names = worldmap.county_names(map_name='new zealand')

# %% Retrieve citynames for abbrevations
out = worldmap.code2county('NL')
out = worldmap.code2county('GB')

# %% Retrieve abbrevations for city names
out = worldmap.county2code('Netherlands')
out = worldmap.county2code('Germany')

# %% Coloring of maps
county_names = ['zeeland','Overijssel', 'flevoland']
opacity = [0.4, 0.6, 0.9]
out = worldmap.plot(county_names,opacity=opacity, cmap='Set1', map_name='netherlands', filename='Netherlands_map.svg')

county_names = ['Norway','Nederland','belgium']
opacity = [10, 25, 5]
out = worldmap.plot(county_names, opacity=opacity, map_name='world', cmap='Set2')

country_names = ['Nederland', 'austrialia', 'brazile']
cmap = ['#000fff','#000fff','#000fff']
out = worldmap.plot(country_names, cmap=cmap, map_name='world')

# %%
