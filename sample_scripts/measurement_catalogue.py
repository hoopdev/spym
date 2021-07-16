import spym
import os
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def format_title(attrs):
    ''' Provide a title from the metadata of the DataArray.

    '''

    title = ""

    if "filename" in attrs:
        title += attrs["filename"] + "<br>"

    title += "V={:.2f} {}, I={:.2f} {}, Vm={:.2f} {}".format(
        attrs["bias"],
        attrs["bias_units"],
        attrs["setpoint"],
        attrs["setpoint_units"],
        attrs["bias_modulation"],
        attrs["bias_modulation_units"])
    return title

data_dir = 'E:/Dropbox/data/0713/'
data_files = os.listdir(data_dir)

fig_list_Topo = []
fig_list_STS = []
for item_name in data_files:
    if item_name.endswith('.sm4'):
        if 'STS' in item_name:
            f_sts = spym.load(os.path.join(data_dir+item_name))
            lia_current = f_sts.LIA_Current
            fig = lia_current.spym.plotly(display = False)
            fig_list_STS.append(fig)
        
        else:
            f_image= spym.load(os.path.join(data_dir+item_name))
            # print(tf.attrs)
            tf = f_image.Topography_Forward
            tf.spym.align()
            tf.spym.plane()
            tf.spym.fixzero()

            topo_f = tf.spym._dr
            lia_f = f_image.LIA_Current_Forward.spym._dr
            title = format_title(topo_f.attrs)

            xaxis_topo =dict(
                    title = "x (nm)",
                    ticks= 'outside',
                    range=(topo_f.x.min(),topo_f.x.max()),
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )
            yaxis_topo =dict(
                    title = "y (nm)",
                    ticks= 'outside',
                    range=(topo_f.y.min(),topo_f.y.max()),
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )
            if lia_f.attrs['bias_modulation'] > 0:
                fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.15,  subplot_titles=('Topography', 'LIA Current'))
                colorbar_topo= dict(
                        title = 'Height (pm)',
                        titleside = 'right',
                        tickmode = 'array',
                        ticks = 'outside',
                        len=1,
                        thickness = 10,
                        outlinecolor='Black',
                        outlinewidth=2,
                        x = 0.45
                )
                trace_topo = go.Heatmap(
                        x = topo_f.x,
                        y = topo_f.y,
                        z = topo_f.values,
                        colorbar = colorbar_topo,
                        colorscale= "Solar",
                        showscale=True,
                        # name = str(bias),
                        zsmooth = 'best'
                )
                xaxis_lia =dict(
                        title = "x (nm)",
                        ticks= 'outside',
                        range=(lia_f.x.min(),lia_f.x.max()),
                        linewidth=1,
                        linecolor='Black',
                        mirror=True
                )
                yaxis_lia =dict(
                        title = "y (nm)",
                        ticks= 'outside',
                        range=(lia_f.y.min(),lia_f.y.max()),
                        linewidth=1,
                        linecolor='Black',
                        mirror=True
                )
                colorbar_lia= dict(
                        title = 'LIA Current (pA)',
                        titleside = 'right',
                        tickmode = 'array',
                        ticks = 'outside',
                        len=1,
                        thickness = 10,
                        outlinecolor='Black',
                        outlinewidth=2,
                        # x = 0.46
                )
                trace_lia = go.Heatmap(
                        x = lia_f.x,
                        y = lia_f.y,
                        z = lia_f.values,
                        colorbar = colorbar_lia,
                        colorscale= "Solar",
                        showscale=True,
                        zsmooth = 'best'
                )
                fig.add_trace(trace_topo, row=1, col=1)
                fig.add_trace(trace_lia, row=1, col=2)
                layout = go.Layout(title = title,height=800, width=1600,showlegend=True,xaxis=xaxis_topo,yaxis=yaxis_topo,xaxis2=xaxis_lia,yaxis2=yaxis_lia,xaxis_showgrid=True,yaxis_showgrid=True,plot_bgcolor='White')
                fig.update_layout(layout)

            else:
                fig = make_subplots(rows=1, cols=1,  subplot_titles=('Topography'))
                colorbar_topo= dict(
                        title = 'Height (pm)',
                        titleside = 'right',
                        tickmode = 'array',
                        ticks = 'outside',
                        len=1,
                        thickness = 10,
                        outlinecolor='Black',
                        outlinewidth=2,
                )
                trace_topo = go.Heatmap(
                        x = topo_f.x,
                        y = topo_f.y,
                        z = topo_f.values,
                        colorbar = colorbar_topo,
                        colorscale= "Solar",
                        showscale=True,
                        zsmooth = 'best'
                )
                fig.add_trace(trace_topo, row=1, col=1)
                layout = go.Layout(title = title,height=800, width=800,showlegend=True,xaxis=xaxis_topo,yaxis=yaxis_topo,xaxis_showgrid=True,yaxis_showgrid=True,plot_bgcolor='White')
                fig.update_layout(layout)
            fig_list_Topo.append(fig)

filename= os.path.join(data_dir+"catalogue.html")
dashboard = open(filename, 'w')
dashboard.write("<html><head></head><body>" + "\n")
include_plotlyjs = True

for fig in fig_list_Topo+fig_list_STS:
    inner_html = fig.to_html(include_plotlyjs = include_plotlyjs).split('<body>')[1].split('</body>')[0]
    dashboard.write(inner_html)
    include_plotlyjs = False
dashboard.write("</body></html>" + "\n")