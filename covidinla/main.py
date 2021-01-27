import pandas as pd
import matplotlib.pyplot as plt
import tilemapbase
from math import log
import os.path as path
from os import listdir
from progress.bar import Bar
import imageio

# get dataset from source
print("Getting data set...")
raw_data = pd.read_csv("https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/latimes-place-totals.csv")

# convert date column to a time series
raw_data["date"] = pd.to_datetime(raw_data["date"])

# LA data only
fips = int(input("Enter state fips (LA is 37):"))
la_data = (raw_data[raw_data["fips"] == fips])
title = la_data["county"].iloc[0]

# sort by date
la_data = la_data.sort_values(by=["place","date"], ascending=True)
la_data.reset_index(inplace=True)

# compute moving sum average of new cases
la_data["new_cases"] = la_data.groupby("place")["confirmed_cases"].diff().fillna(0) / la_data.groupby("place")["date"].diff().fillna(pd.Timedelta(seconds=0)).dt.days.replace(0,1)
la_data["avg"] = la_data.groupby("place")["new_cases"].rolling(5).mean().fillna(0).reset_index()["new_cases"]

# init plotting library
print("Getting map...")
tilemapbase.init(create=True)
tiles = tilemapbase.tiles.Stamen_Toner_Lite
lon_west = la_data.x.min()
lon_east = la_data.x.max()
lat_north = la_data.y.max()
lat_south = la_data.y.min()
extent = tilemapbase.Extent.from_lonlat(lon_west, lon_east, lat_south, lat_north)
extent = extent.to_aspect(1.0)
plotter = tilemapbase.Plotter(extent, tiles, width=600)

# project each item in the plot axis
print("Projecting on map...")
la_data["px"], la_data["py"] = zip(*la_data.apply(lambda row: tilemapbase.project(row["x"], row["y"]), axis=1))

# compute area size
la_data["s"] = la_data["avg"].map(lambda x: x*20)

# create plot figure common for all frames
fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plotter.plot(ax, tiles)
plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

# group by date in order to create each frame
groups = la_data.groupby("date")
frames_bar = Bar("Creating frames... ", max=len(groups))
i = 0
for key, day_df in groups:
    
    # create the axis for the cases
    sct = ax.scatter(day_df.px,day_df.py,s=day_df.s, marker="o", color="blue", alpha=0.3)
    
    # add text to plot
    txt = ax.text(0.05, 0.05, key.strftime("%d %b, %Y"), fontsize=15, transform=ax.transAxes)

    # save plot and erase axis
    plt.savefig(f"output/{i}.png", format="png", bbox_inches="tight", pad_inches=0)
    sct.remove()
    txt.remove()
    i = i + 1
    frames_bar.next()
frames_bar.finish()

# make a gif from the images
gif_bar = Bar("Making gif... ", max=i+1)
with imageio.get_writer(f"{title}.gif", mode='I', loop=1, duration=0.1) as writer:
    for key in range(0, i):
        image = imageio.imread(f"output/{key}.png")
        writer.append_data(image)
        gif_bar.next()
gif_bar.finish()
