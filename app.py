from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.models.annotations import Title
from bokeh.embed import components
from bokeh.resources import CDN


start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 4, 30)

df = data.DataReader(name="AAL", data_source="yahoo", start=start, end=end)

p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
t = Title()
t.text = "American Airlines (AAL)"
p.title = t
p.grid.grid_line_alpha = 0.3

hours_16 = 16*60*60*1000  # converts to milliseconds


def inc_dec(c, o):
    if c >= o:
        value = "Increase"
    else:
        value = "Decrease"
    return value


df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
df["Middle"] = (df.Open + df.Close)/2
df["Height"] = abs(df.Close - df.Open)

# Vertical line high/low glyph
p.segment(df.index, df.High, df.index, df.Low, color="black")

# Rising price days
p.rect(
    df.index[df.Status == "Increase"],
    df.Middle[df.Status == "Increase"],
    hours_16,
    df.Height[df.Status == "Increase"],
    fill_color="#CCFFFF",
    line_color="black"
)

# Falling price days
p.rect(
    df.index[df.Status == "Decrease"],
    df.Middle[df.Status == "Decrease"],
    hours_16,
    df.Height[df.Status == "Decrease"],
    fill_color="#FF3333",
    line_color="black"
)

script1, div1 = components(p)
cdn_js = CDN.js_files
cdn_css = CDN.css_files

# output_file("CS.html")
# show(p)
