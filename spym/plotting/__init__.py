import matplotlib.pyplot as plt
import hvplot.xarray
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Plotting():
    ''' Plotting.
    
    '''

    def __init__(self, spym_instance):
        self._spym = spym_instance

    def plot(self, title=None, **kwargs):
        ''' Plot data with custom parameters using matplotlib.

        Args:
            title: title of the figure (string). By default gives some basic information on the data plotted. Pass an empty string to disable it.
            **kwargs: any argument accepted by xarray.plot() function.

        '''

        dr = self._spym._dr
        attrs = dr.attrs

        # Clear plt
        plt.clf()

        # Set plot properties
        if attrs['interpretation'] == 'spectrum':
            # plot wraps matplotlib.pyplot.plot()
            plot = dr.plot.line(hue="y", **kwargs)

        elif attrs['interpretation'] == 'image':
            # plot is an instance of matplotlib.collections.QuadMesh
            plot = dr.plot.pcolormesh(**kwargs)
            fig = plot.get_figure()
            ax = plot.axes
            # Fit figure pixel size to image
            fig_width, fig_height = self._fit_figure_to_image(fig, dr.data, ax)
            fig.set_size_inches(fig_width, fig_height)

            # Apply colormap
            plot.set_cmap('afmhot')

        else:
            # Create figure
            # xarray plot() wraps:
            #   - matplotlib.pyplot.plot() for 1d arrays
            #   - matplotlib.pyplot.pcolormesh() for 2d arrays
            #   - matplotlib.pyplot.hist() for anything else
            plot = dr.plot(**kwargs)

        # Set figure title
        if title is None:
            title = self._format_title()
        plt.title(title)

        plt.plot()

        return plot

    def hvplot(self, title=None, **kwargs):
        ''' Plot data with custom parameters using hvplot.

        Args:
            title: title of the figure (string). By default gives some basic information on the data plotted. Pass an empty string to disable it.
            **kwargs: any argument accepted by hvplot() function.

        '''

        dr = self._spym._dr
        attrs = dr.attrs

        # Set figure title
        if title is None:
            title = self._format_title()

        # Set hvplot properties
        if attrs['interpretation'] == 'spectrum':
            hvplot = dr.hvplot(**kwargs).opts(title=title)

        elif attrs['interpretation'] == 'image':
            hvplot = dr.hvplot(**kwargs).opts(title=title,
                                              cmap='afmhot',
                                              frame_width=512,
                                              frame_height=512,
                                              data_aspect=1)

        else:
            hvplot = dr.hvplot(**kwargs).opts(title=title)

        return hvplot

    def _format_title(self):
        ''' Provide a title from the metadata of the DataArray.

        '''

        title = ""
        attrs = self._spym._dr.attrs

        if "filename" in attrs:
            title += attrs["filename"] + "\n"

        title += "V={:.2f} {}, I={:.2f} {}, Vm={:.2f} {}".format(
            attrs["bias"],
            attrs["bias_units"],
            attrs["setpoint"],
            attrs["setpoint_units"],
            attrs["bias_modulation"],
            attrs["bias_modulation_units"])

        return title

    def _format_title_plotly(self):
        ''' Provide a title from the metadata of the DataArray.

        '''

        title = ""
        attrs = self._spym._dr.attrs

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

    def _fit_figure_to_image(self, figure, image, axis=None):
        ''' Calculate figure size so that plot (matplotlib axis) pixel size is equal to the image size.

        Args:
            figure: matplotlib Figure instance.
            image: 2d numpy array.
            axis: axis of the figure to adapt, if None takes the first (or only) axis.

        Returns:
            adapted width and height of the figure in inches.

        '''

        if axis is None:
            axis = figure.axes[0]
        bounds = axis.bbox.bounds

        im_width, im_height = image.shape

        width_scale = im_width/bounds[2]
        height_scale = im_height/bounds[3]

        fig_width, fig_height = figure.get_size_inches()

        return fig_width*width_scale, fig_height*height_scale



    def plotly(self, title=None, display = True):
        ''' Plot data using plotly.

        Args:
            title: title of the figure (string). By default gives some basic information on the data plotted. Pass an empty string to disable it.

        '''

        dr = self._spym._dr
        attrs = dr.attrs

        # Set plot properties
        if attrs['interpretation'] == 'spectrum':
            # plot is an given by plotly.graph_objects.Scatter()
            # output averaged spectrum in addition to each spectrum
            xaxis =dict(
                    title = "Voltage (V)",
                    ticks= 'outside',
                    range=(dr.x.min(),dr.x.max()),
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )
            yaxis =dict(
                    title = "LIA Current (pA)",
                    ticks= 'outside',
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )


            # averaged spectrum
            fig = make_subplots(rows=1, cols=1)
            trace_average = go.Scatter(
                x=dr.x,
                y=dr.values.mean(axis=0),
                mode='lines',
                name="average",
                showlegend=True)
            fig.add_trace(trace_average,row=1,col=1)

            #each spectrum
            for i,spectrum in enumerate(dr.values):
                trace = go.Scatter(
                    x=dr.x,
                    y=spectrum,
                    mode='lines',
                    visible='legendonly',
                    name=i,
                    showlegend=True)
                fig.add_trace(trace,row=1,col=1)
            fig.update_layout(height=600, width=600,showlegend=True,xaxis=xaxis,yaxis=yaxis,xaxis_showgrid=True,yaxis_showgrid=True,plot_bgcolor='White')

        elif attrs['interpretation'] == 'image':
            # plot is given by plotly.graph_objects.Heatmap()
            xaxis =dict(
                    title = "X (nm)",
                    ticks= 'outside',
                    range=(dr.x.min(),dr.x.max()),
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )
            yaxis =dict(
                    title = "Y (nm)",
                    ticks= 'outside',
                    range=(dr.y.min(),dr.y.max()),
                    linewidth=1,
                    linecolor='Black',
                    mirror=True
            )
            fig = make_subplots(rows=1, cols=1)
            trace = go.Heatmap(
                    x = dr.x,
                    y = dr.y,
                    z=dr.values,
                    colorscale= "Solar",
                    colorbar_title="Height (pm)",
                    showscale=True,
                    name = 'Topography',
            )

            fig.add_trace(trace,row=1,col=1)
            fig.update_layout(height=600, width=600,showlegend=True,xaxis=xaxis,yaxis=yaxis,xaxis_showgrid=True,yaxis_showgrid=True,plot_bgcolor='White')

        else:
            #TODO
            # Create figure
            # xarray plot() wraps:
            #   - matplotlib.pyplot.plot() for 1d arrays
            #   - matplotlib.pyplot.pcolormesh() for 2d arrays
            #   - matplotlib.pyplot.hist() for anything else
            # plot = dr.plot(**kwargs)
            fig = None

        # Set figure title
        if title is None:
            title = self._format_title_plotly()
        fig.update_layout(title_text=title,)

        if (display):
            fig.show()

        return fig