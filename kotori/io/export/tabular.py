# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
import tempfile
from twisted.logger import Logger, LogLevel
from twisted.web.template import renderElement
from kotori.io.export.html import DatatablesPage
from kotori.io.protocol.util import get_data_uri
from kotori.io.export.util import dataframe_index_and_sort, make_timezone_unaware

log = Logger()

try:
    import pandas
except ImportError:
    log.failure('Tabular export not available, please install "pandas".', level=LogLevel.warn)


class UniversalTabularExporter(object):
    """
    Universal exporter for tabular data.

    Render pandas DataFrame to Excel (XLSX), HDF5
    and NetCDF formats and as DataTables HTML widget.
    """

    def __init__(self, bucket, dataframe):
        self.bucket = bucket
        self.request = bucket.request
        self.dataframe = dataframe

    def render(self, format, kind=None, buffer=None):

        # Variable aliases
        bucket = self.bucket
        df = self.dataframe

        # Compute group name for HDF5 and NetCDF formats
        # TODO: Optionally prefix with "realm" from "bucket.tdata"
        group_name = bucket.title.short

        if format == 'xlsx':

            # Ensure that datetimes are timezone unaware before writing to Excel.
            make_timezone_unaware(df)

            # http://pandas.pydata.org/pandas-docs/stable/io.html#io-excel-writer
            # https://stackoverflow.com/questions/28058563/write-to-stringio-object-using-pandas-excelwriter
            with pandas.ExcelWriter('temp.xlsx', engine='xlsxwriter') as excel_writer:
                excel_writer.book.filename = buffer
                df.to_excel(excel_writer, sheet_name=bucket.title.compact[:31], index=False)

        elif format in ['hdf', 'hdf5', 'h5']:

            # Create index from "time" column
            df = dataframe_index_and_sort(df, 'time')

            # http://pandas.pydata.org/pandas-docs/stable/io.html#hdf5-pytables
            t = tempfile.NamedTemporaryFile(suffix='.hdf5')
            try:
                df.to_hdf(t.name, group_name, format='table', data_columns=True, index=False)
                buffer.write(t.read())
            except Exception as ex:
                return self.request.error_response(bucket, with_traceback=True)

        elif format in ['nc', 'cdf']:

            # Create index from "time" column
            df = dataframe_index_and_sort(df, 'time')

            # http://xarray.pydata.org/
            # http://xarray.pydata.org/en/stable/io.html#netcdf
            t = tempfile.NamedTemporaryFile(suffix='.nc')
            try:
                #df.to_xarray().to_netcdf(path=t.name, group=group_name)
                #df.to_xarray().to_netcdf(path=t.name, format='NETCDF4', engine='h5netcdf', group=group_name)
                df.to_xarray().to_netcdf(path=t.name, format='NETCDF4', engine='netcdf4', group=group_name)
                buffer.write(t.read())
            except Exception as ex:
                return self.request.error_response(bucket, with_traceback=True)

        elif format in ['dt', 'datatables']:
            # https://datatables.net/

            # Compute data_uri, forward "from" and "to" parameters
            data_uri = get_data_uri(bucket, 'data.html')

            # Render HTML snippet containing DataTable widget
            page = DatatablesPage(data_uri=data_uri, bucket=bucket)
            bucket.request.setHeader('Content-Type', 'text/html; charset=utf-8')
            return renderElement(bucket.request, page)
