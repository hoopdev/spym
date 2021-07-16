import spym
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

data_dir = 'E:/Dropbox/data/0713/'
data_string = '20210713t_00'
# data_num_list = [str(num) for num in range(33,35)]
# data_num_list = [str(num) for num in range(33,54)]
data_num_list = [str(num) for num in range(54,75)]

trace_list = []
fig_list = []
bias_list = []
frame_list = []

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

button = {
        "buttons": [
            {
                "args": [None, frame_args(400),],
                "label": "&#9654;",
                "method": "animate"
            },
            {
                "args": [[None],frame_args(0),],
                "label": "&#9724;",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": True,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
}
sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Bias V=",
        "suffix": " (V)",
        "visible": True,
        "xanchor": "right"
    },
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

fig = make_subplots(
    rows=1, cols=2, subplot_titles=('Real Space', 'Q Space'),
    horizontal_spacing=0.15
)

for num_item in data_num_list:
    data_file  = os.path.join(data_dir+data_string+num_item+'.sm4')
    f_didv = spym.load(data_file)
    tf = f_didv.LIA_Current_Forward
    tf.spym.align()
    # tf.spym.plane()
    dr = tf.spym._dr
    z = dr.values
    bias = dr.attrs["bias"]

    # tf.spym.fixzero()
    dr = tf.spym._dr
    fft_z = np.abs(np.fft.fftshift(np.fft.fft2(dr.values)))

    qx = 2*np.pi/dr.x.max().values*np.linspace(-0.5,0.5,512)
    qy = 2*np.pi/dr.y.max().values*np.linspace(-0.5,0.5,512)

    # print(qx)
    # print(qy)

    xaxis =dict(
            title = "x (nm)",
            ticks= 'outside',
            range=(dr.x.min(),dr.x.max()),
            linewidth=1,
            linecolor='Black',
            mirror=True
    )
    yaxis =dict(
            title = "y (nm)",
            ticks= 'outside',
            range=(dr.y.min(),dr.y.max()),
            linewidth=1,
            linecolor='Black',
            mirror=True
    )
    colorbar= dict(
            title = 'LIA Current (pA)',
            titleside = 'right',
            tickmode = 'array',
            ticks = 'outside',
            len=1,
            thickness = 10,
            outlinecolor='Black',
            outlinewidth=2,
            x = 0.46
    )
    trace = go.Heatmap(
            x = dr.x,
            y = dr.y,
            z=z,
            colorbar = colorbar,
            colorscale= "Solar",
            showscale=True,
            name = str(bias),
            # zmin = -8,
            # zmax = 2,
            zsmooth = 'best'
    )
    xaxis_fft =dict(
            title = "qx (nm^-1)",
            ticks= 'outside',
            range=(-0.05,0.05),
            linewidth=1,
            linecolor='Black',
            mirror=True
    )
    yaxis_fft =dict(
            title = "qy (nm^-1)",
            ticks= 'outside',
            range=(-0.05,0.05),
            linewidth=1,
            linecolor='Black',
            mirror=True
    )
    colorbar_fft= dict(
            title = 'Intensity (arb.)',
            titleside = 'right',
            tickmode = 'array',
            ticks = 'outside',
            len=1,
            thickness = 10,
            outlinecolor='Black',
            outlinewidth=2
    )
    trace_fft = go.Heatmap(
            x = qx,
            y = qy,
            z=fft_z,
            colorbar = colorbar_fft,
            colorscale= "Jet",
            showscale=True,
            name = str(bias),
            zmin = 0,
            zmax = 1e5,
            # zsmooth = 'best'
    )
    bias_list.append(bias)

    frame_list.append(go.Frame(
        data=[trace,trace_fft], 
        name = num_item,
        traces=[0,1,]
    ))

    slider_step = {"args": [
        [num_item],
        frame_args(1000),
    ],
        "label": str(bias),
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

layout = go.Layout(updatemenus=[button],sliders=[sliders_dict], height=800, width=1600,showlegend=True,xaxis=xaxis,yaxis=yaxis,xaxis_showgrid=True,yaxis_showgrid=True,xaxis2=xaxis_fft,yaxis2=yaxis_fft,plot_bgcolor='White')
# layout = go.Layout(updatemenus=[button],sliders=[sliders_dict], height=800, width=800,showlegend=True,xaxis=xaxis,yaxis=yaxis,xaxis_showgrid=True,yaxis_showgrid=True,plot_bgcolor='White')

fig.add_trace(frame_list[0].data[0], row=1, col=1)
fig.add_trace(frame_list[0].data[1], row=1, col=2)

fig.frames=frame_list
fig.update_layout(layout)

# fig = go.Figure(data=frame_list[0].data,
#                 frames=frame_list,
#                 layout=layout,
#         )
# fig.show()
# fig.to_html(include_plotlyjs = include_plotlyjs)
fig.write_html("out.html")