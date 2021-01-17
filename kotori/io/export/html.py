# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@elmyra.de>
from twisted.web.template import XMLString, Element, renderer, tags, CDATA
#from dyplot.dygraphs import Dygraphs


class GenericPage(Element):
    """
    Base class for HTML-based widgets.
    """

    @renderer
    def fill_slots(self, request, tag):

        slotdata = self.__dict__.copy()

        # Pass data to template verbatim without applying htmlentity conversion
        slotdata['data_uri'] = CDATA(slotdata['data_uri'])

        tag.fillSlots(**slotdata)
        return tag

    @renderer
    def header(self, request, tag):
        tdata = self.bucket.tdata
        title = 'Address: {network} » {gateway} » {node}'.format(**dict(tdata))
        return tag(tags.b(title))

    @renderer
    def footer_left(self, request, tag):
        return tag(tags.p('Query expression (times are UTC): ', self.bucket.tdata.expression))

    @renderer
    def footer_right(self, request, tag):
        """
        '(c) 2014-2016 ',
        tags.a('Open Hive', href='http://open-hive.org/'), ' and ',
        tags.a('Hiveeyes', href='https://hiveeyes.org/docs/system/'), '. ',
        """
        return tag(tags.p(
            'Powered by ',
            tags.a('Kotori', href='https://getkotori.org/'), ', ',
            tags.a('InfluxDB', href='https://github.com/influxdata/influxdb'), ', ',
            tags.a('dygraphs', href='http://dygraphs.com/'), ' and ',
            tags.a('DataTables', href='https://datatables.net/'), '.'
        ))


class DygraphsPage(GenericPage):
    """
    dygraphs plugin, see http://dygraphs.com/
    """

    loader = XMLString("""
        <html xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="fill_slots">
            <head>
                <script src="//cdnjs.cloudflare.com/ajax/libs/dygraph/1.1.1/dygraph-combined.js"></script>
                <style type="text/css" media="screen">
                    body {
                        font-family: Arial, sans-serif;
                        font-size: larger;
                    }
                    h1 {
                        font-size: large;
                    }
                    .footer {
                        padding-top: 1em;
                        font-size: x-small;
                    }
                    .footer.left {
                        float: left;
                    }
                    .footer.right {
                        float: right;
                    }
                    .clearfix {
                        clear: both;
                    }
                    .linegraph {
                        width: 100%;
                        height: 25em;
                    }
                </style>
            </head>
            <body>
                <h1 t:render="header"/>
                <p style="font-size: smaller">
                    <strong>Zoom:</strong> Click and Drag |
                    <strong>Pan:</strong> Shift-Click and Drag |
                    <strong>Unzoom:</strong> Double-Click
                </p>
                <div id="linegraph" class="linegraph"/>
                <script type="text/javascript">
                    var element = document.getElementById('linegraph');
                    var data_uri = '<t:slot name="data_uri" />'.replace('<![CDATA[', '').replace(']]>', '');
                    new Dygraph(element, data_uri, {
                      legend: 'always',
                    });
                </script>
                <div class="footer left" t:render="footer_left"/>
                <div class="footer right" t:render="footer_right"/>
                <div class="clearfix"/>
            </body>
        </html>
    """)

    def __init__(self, data_uri=None, bucket=None):
        self.data_uri = data_uri
        self.bucket = bucket


class DatatablesPage(GenericPage):
    """
    DataTables plugin, see https://datatables.net/
    """

    loader = XMLString("""
        <html xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="fill_slots">
            <head>
                <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/u/dt/jq-2.2.3,jszip-2.5.0,pdfmake-0.1.18,dt-1.10.12,b-1.2.1,b-colvis-1.2.1,b-html5-1.2.1,b-print-1.2.1,cr-1.3.2,fc-3.2.2,fh-3.1.2,kt-2.1.2,r-2.1.0,rr-1.1.2,sc-1.4.2,se-1.2.0/datatables.min.css" />
                <script src="//cdn.datatables.net/u/dt/jq-2.2.3,jszip-2.5.0,pdfmake-0.1.18,dt-1.10.12,b-1.2.1,b-colvis-1.2.1,b-html5-1.2.1,b-print-1.2.1,cr-1.3.2,fc-3.2.2,fh-3.1.2,kt-2.1.2,r-2.1.0,rr-1.1.2,sc-1.4.2,se-1.2.0/datatables.min.js"></script>
                <style type="text/css" media="screen">
                    body {
                        font-family: Arial, sans-serif;
                        font-size2: larger;
                    }
                    h1 {
                        font-size: large;
                    }
                    .footer {
                        padding-top: 1em;
                        font-size: x-small;
                    }
                    .footer.left {
                        float: left;
                    }
                    .footer.right {
                        float: right;
                    }
                    .clearfix {
                        clear: both;
                    }
                </style>
            </head>
            <body>
                <h1 t:render="header"/>
                <div id="dataframe" class="display" style="width: 100%"/>
                <table id="example" class="display" cellspacing="0" width="100%">
                </table>
                <script type="text/javascript">
                    $(document).ready(function(){
                        var data_uri = '<t:slot name="data_uri" />'.replace('<![CDATA[', '').replace(']]>', '');
                        $('#dataframe').load(data_uri, function() {
                            var table = $('.dataframe');
                            table.attr('border', '0');
                            table.DataTable({
                                buttons: [
                                    //'copy', 'csv', 'excel', 'pdf', 'print'
                                    'copy', 'csv', 'excel', 'print'
                                ]
                            });
                            table.attr('class', 'display dataTable');
                        });
                        console.log('READY.');

                    });
                </script>
                <div class="footer left" t:render="footer_left"/>
                <div class="footer right" t:render="footer_right"/>
                <div class="clearfix"/>
            </body>
        </html>
    """)

    def __init__(self, data_uri=None, bucket=None):
        self.data_uri = data_uri
        self.bucket = bucket
