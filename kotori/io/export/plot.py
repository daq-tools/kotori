# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
import tempfile
from pprint import pprint
from string import Template
from pkg_resources import resource_string
from twisted.web.template import renderElement
from twisted.logger import Logger
from kotori.io.export.html import DygraphsPage
from kotori.io.protocol.util import get_data_uri
from kotori.io.export.util import dataframe_index_to_column, dataframe_wide_to_long_indexed, dataframe_index_and_sort
from kotori.io.export.util import matplotlib_locator_formatter

log = Logger()


class UniversalPlotter(object):
    """
    Universal plotter for timeseries data.

    Render pandas DataFrame to different timeseries plots.
    See also: http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook-plotting

    Tabular data:

        - CSV
        - JSON
        - HTML
        - Excel (XLSX)
        - HDF5
        - NetCDF
        - DataTables HTML widget

    Timeseries plots:

        - [PNG]  matplotlib
        - [PNG]  ggplot
        - [HTML] dygraphs
        - [HTML] Bokeh
        - [HTML] Vega/Vincent

    """

    def __init__(self, bucket, dataframe):
        self.bucket = bucket
        self.request = bucket.request
        self.dataframe = dataframe

    def render(self, format, kind=None, buffer=None):
        if format == 'png':
            return self.render_png(buffer)
        elif format == 'html':
            return self.render_html(kind)
        elif format == 'json':
            return self.render_json(kind)

    def render_png(self, buffer):
        """
        Render timeseries plots as PNG images.
        """

        bucket = self.bucket

        import matplotlib.font_manager
        matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

        import matplotlib
        try:
            matplotlib.use('agg')
        except:
            pass

        import matplotlib.pyplot as plt

        df = self.dataframe
        #df = df.set_index(['time'])

        # Compute datetime range boundaries
        datetime_min = min(df.time)
        datetime_max = max(df.time)
        datetime_delta = datetime_max - datetime_min
        #xmin = pd.to_datetime('2016-05-01')
        #xmax = pd.to_datetime('2016-08-01')

        renderer = bucket.tdata.get('renderer', 'matplotlib')
        if renderer == 'matplotlib':

            # Bring DataFrame into appropriate format
            df = dataframe_index_and_sort(df, 'time')

            # Propagate non-null values forward or backward, otherwise
            # matplotlib would not plot the sparse data frame properly.
            # With time series data, using pad/ffill is extremely common so that the “last known value” is available at every time point.
            # http://pandas.pydata.org/pandas-docs/stable/missing_data.html#filling-missing-values-fillna
            df.fillna(method='pad', inplace=True)

            # Make plots of DataFrame using matplotlib / pylab.
            # http://matplotlib.org/
            # http://pandas.pydata.org/pandas-docs/version/0.13.1/visualization.html
            # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
            # https://markthegraph.blogspot.de/2015/05/plotting-time-series-dataframes-in.html

            if 'style' in bucket.tdata and bucket.tdata.style:
                try:
                    plt.style.use(bucket.tdata.style)
                except Exception:
                    error_message = u'# Unknown style "{style_name}", available styles: {available}'.format(
                        style_name=bucket.tdata.style, available=plt.style.available)
                    log.error(error_message)
                    return self.request.error_response(bucket, error_message)


            # Basic plotting
            #df.plot()
            #plt.savefig(buffer)


            # Advanced plotting
            ax = df.plot()
            fig = ax.get_figure()

            # Figure heading
            title = fig.suptitle(bucket.title.human, fontsize=12)
            #fig.tight_layout(pad=1.5)

            # Axis and tick labels
            ax.set_xlabel('Time')
            ax.set_ylabel('Value')
            ax.tick_params(axis='x', labelsize='smaller')

            # Grid and legend
            # http://matplotlib.org/users/legend_guide.html
            # http://matplotlib.org/examples/pylab_examples/legend_demo3.html
            ax.grid(True)

            legend_params = dict(ncol=1, loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small', shadow=True, fancybox=True)
            legend = ax.legend(**legend_params) # title='Origin'
            #ax.legend(**legend_params) # title='Origin'

            # Sort list of legend labels
            # http://stackoverflow.com/questions/22263807/how-is-order-of-items-in-matplotlib-legend-determined/27512450#27512450


            # Axis formatting
            #ax.xaxis_date()
            #ax.autoscale_view()


            # Compute appropriate locator and formatter
            locator, formatter = matplotlib_locator_formatter(datetime_delta, span=1)

            #ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

            # Figure formatting
            fig.autofmt_xdate()

            # http://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box/10154763#10154763
            fig.savefig(buffer, bbox_extra_artists=(title, legend), bbox_inches='tight')

            # TODO: Add annotations
            """
            # https://stackoverflow.com/questions/11067368/annotate-time-series-plot-in-matplotlib
            # https://stackoverflow.com/questions/17891493/annotating-points-from-a-pandas-dataframe-in-matplotlib-plot
            import matplotlib.dates as mdates
            fig = plot.draw()
            ax = fig.axes[0]
            ax.annotate('Test', (mdates.date2num(x[1]), y[1]), xytext=(15, 15),
                textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))

            """


        elif renderer == 'ggplot':

            # https://yhat.github.io/ggplot/notebook.html?page=build/docs/examples/Multiple%20Line%20Plot.html
            # https://stackoverflow.com/questions/23541497/is-there-a-way-to-plot-a-pandas-series-in-ggplot
            # https://stackoverflow.com/questions/24478925/is-it-possible-to-plot-multiline-chart-on-python-ggplot/24479513#24479513

            # https://github.com/yhat/ggplot/blob/master/docs/how-to/Building%20Faceted%20(or%20Trellised)%20Plots.ipynb
            # https://github.com/yhat/ggplot/blob/master/docs/how-to/Annotating%20Plots%20-%20Titles%20and%20Labels.ipynb
            # https://github.com/yhat/ggplot/blob/master/docs/how-to/How%20to%20make%20xkcd%20style%20graphs.ipynb

            from ggplot import ggplot, aes, qplot, geom_line, geom_text, ggtitle, stat_smooth, scale_x_date, date_format, date_breaks
            from ggplot import theme_538, theme_bw, theme_gray, theme_xkcd

            # https://stackoverflow.com/questions/24478925/is-it-possible-to-plot-multiline-chart-on-python-ggplot/24479513#24479513
            # https://stackoverflow.com/questions/23541497/is-there-a-way-to-plot-a-pandas-series-in-ggplot

            # Convert DataFrame from wide to long format, retaining "time" as visible column
            df = dataframe_wide_to_long_indexed(df, 'time')
            dataframe_index_to_column(df, 'time')

            # Compute appropriate locator and formatter
            locator, formatter = matplotlib_locator_formatter(datetime_delta, span=2)

            plot = ggplot(df, aes(x='time', y='value', color='variable'))\
                   + geom_line()\
                   + scale_x_date(limits=(datetime_min, datetime_max), breaks=locator, labels=formatter)\
                   + ggtitle(bucket.title.human)

            # Axis labels
            plot.xlab = 'Time'
            plot.ylab = 'Value'

            # Labs
            #+ stat_smooth(colour='blue', span=0.2) \
            #+ geom_text(aes(x='x', y='y'), label='hello world')
            #+ scale_x_date(limits=(xmin, xmax), breaks=date_breaks('1 hour'), labels=date_format('%Y-%m-%d\n%H:%M'))

            theme_name = bucket.tdata.get('theme')
            # TODO: Switching themes will leak some matplotlib/pyplot properties, postpone to future versions
            if theme_name:
                if isinstance(theme_name, float):
                    theme_name = str(int(theme_name))
                try:
                    theme = eval('theme_' + theme_name)
                    plot += theme()
                except Exception:
                    error_message = u'# Unknown theme "{theme_name}"'.format(theme_name=theme_name)
                    log.error(error_message)
                    return self.request.error_response(bucket, error_message)

            plot.save(buffer)

            # Attempt to reset global matplotlib parameters to get rid of xkcd theme style
            """
            import matplotlib as mpl
            #mpl.rcParams = mpl.rc_params()
            #del mpl.rcParams['path.sketch']
            #del mpl.rcParams['path.effects']
            #mpl.rcParams = mpl.defaultParams.copy()
            #mpl.rcParams.clear()
            #mpl.rcdefaults()
            #mpl.rcParams = mpl.rcParamsOrig
            if 'axes.prop_cycle' in mpl.rcParams:
                del mpl.rcParams['axes.prop_cycle']
            mpl.rcParams.update({'path.sketch': None, 'path.effects': []})
            mpl.rcParams.update(mpl.rc_params())
            """

        elif renderer == 'seaborn':

            # TODO: We don't do statistical plotting yet.

            # https://stanford.edu/~mwaskom/software/seaborn/examples/timeseries_from_dataframe.html
            # https://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.tsplot.html
            import seaborn as sns
            sns.set(style="darkgrid")
            #sns.tsplot(data=gammas, time="timepoint", unit="subject", condition="ROI", value="BOLD signal")
            #print dir(df)
            #df['time'] = pandas.to_datetime(df['time'])
            #df = df.set_index(df.time)
            pprint(df)
            sns.tsplot(data=df, time="time")
            #sns.tsplot(data=df)
            plt.savefig(buffer)

        else:
            error_message = u'# Unknown renderer "{renderer_name}"'.format(renderer_name=renderer)
            log.error(error_message)
            return self.request.error_response(bucket, error_message)

    def render_html(self, kind):
        """
        Render HTML-based timeseries plots for dygraphs, Bokeh and Vega.
        """

        # Variable aliases
        bucket = self.bucket
        df = self.dataframe

        if kind == 'dygraphs':
            # http://dygraphs.com/

            # Compute data_uri, forward "from" and "to" parameters
            data_uri = get_data_uri(bucket, 'data.csv', {'pad': 'true'})

            # Render HTML snippet containing dygraphs widget
            page = DygraphsPage(data_uri=data_uri, bucket=bucket)
            bucket.request.setHeader('Content-Type', 'text/html; charset=utf-8')
            return renderElement(bucket.request, page)

        elif kind == 'bokeh':
            # http://bokeh.pydata.org/

            from bokeh.io import save
            from bokeh.charts import TimeSeries, vplot

            # Propagate non-null values forward or backward, otherwise
            # Bokeh would not plot the sparse data frame properly.
            # With time series data, using pad/ffill is extremely common so that the “last known value” is available at every time point.
            # http://pandas.pydata.org/pandas-docs/stable/missing_data.html#filling-missing-values-fillna
            df.fillna(method='pad', inplace=True)

            # Plot using matplotlib
            # http://bokeh.pydata.org/en/latest/docs/user_guide/compat.html#userguide-compat
            # https://github.com/bokeh/bokeh/tree/master/examples/compat/
            # https://github.com/bokeh/bokeh/blob/master/examples/compat/pandas_dataframe.py
            # https://github.com/bokeh/bokeh/blob/master/examples/compat/ggplot_line.py
            #df.plot()
            #what = mpl.to_bokeh()

            # Plot using Bokeh TimeSeries
            # http://bokeh.pydata.org/en/latest/docs/reference/charts.html#timeseries
            # http://bokeh.pydata.org/en/0.11.1/docs/user_guide/styling.html#location
            linegraph = TimeSeries(df, x='time', title=bucket.title.human, legend="top_left", width=800)

            # Plot TimeSeries object
            what = vplot(linegraph)

            # Render using Bokeh
            t = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
            save(what, filename=t.name, title=bucket.title.human)

            # Forward html to http response
            bucket.request.setHeader('Content-Type', 'text/html; charset=utf-8')
            return t.read()

        elif kind == 'vega':
            # https://github.com/wrobstory/vincent

            # Compute data_uri, forward "from" and "to" parameters
            data_uri = get_data_uri(bucket, 'data.vega.json', {'pad': 'true', 'backfill': 'true'})

            template = Template(str(resource_string('kotori.io.export', 'vega_template.html')))
            bucket.request.setHeader('Content-Type', 'text/html; charset=utf-8')
            response = template.substitute(path=data_uri, title=bucket.title.human)
            return response.encode('utf-8')

    def render_json(self, kind):
        """
        Render JSON chart description for HTML-based timeseries plot Vega, using Vincent.
        """

        # Variable aliases
        bucket = self.bucket
        df = self.dataframe

        if kind == 'vega':
            # https://github.com/wrobstory/vincent
            # https://github.com/wrobstory/vincent/blob/master/examples/line_chart_examples.py
            # https://stackoverflow.com/questions/29288914/how-to-get-vincent-to-display-a-pandas-date-time-axis-correctly
            # https://wrobstory.github.io/2013/04/pandas-vincent-timeseries.html

            from vincent import Line

            # Mungle DataFrame into appropriate format
            df = dataframe_index_and_sort(df, 'time')

            vis = Line(df)
            vis.axis_titles(x='Time', y='Value')
            vis.legend(title='Origin')

            bucket.request.setHeader('Content-Type', 'application/json')
            return vis.to_json()
