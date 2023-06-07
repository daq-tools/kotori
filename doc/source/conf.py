# -*- coding: utf-8 -*-
#
# Kotori documentation build configuration file, created by
# sphinx-quickstart on Fri Nov  6 21:36:37 2015.
#
# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.graphviz",
    "sphinxcontrib.mermaid",
    "sphinxext.opengraph",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The root toctree document.
root_doc = 'index'

# General information about the project.
project = u'Kotori'
copyright = u'2013-2023, The Kotori Developers'
author = u'The Kotori Developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# version = 'x.x.x'
# The full version, including alpha/beta/rc tags.
# release = 'x.x.x'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["readme.rst"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'
html_last_updated_fmt = ""

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Kotoridoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (root_doc, 'Kotori.tex', u'Kotori Documentation',
   u'Kotori Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (root_doc, 'kotori', u'Kotori Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (root_doc, 'Kotori', u'Kotori Documentation',
   author, 'Kotori', 'Data Acquisition and Telemetry',
   'DAQ'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# -- Custom options -------------------------------------------

html_theme = "furo"
html_show_sourcelink = True

# Theme options.
html_theme_options = {
    "light_logo": "img/kotori-logo.png",
    "dark_logo": "img/kotori-logo-dark.png",
    # https://github.com/pradyunsg/furo/blob/main/src/furo/assets/styles/variables/_colors.scss
    "light_css_variables": {
        "color-brand-primary": "#436FCEFF",
        "color-background-border": "#4743CE4F",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/daq-tools/kotori",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/kotori/",
            "html": "",
            "class": "fa-brands fa-solid fa-cart-shopping-fast fa-2x",
        },
        {
            "name": "Documentation",
            "url": "https://kotori.readthedocs.io/",
            "html": "",
            "class": "fa-brands fa-solid fa-readthedocs fa-2x",
        },
    ],
}

# Furo: Add Font Awesome Icon Pack.
# https://pradyunsg.me/furo/customisation/footer/#font-awesome
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]


# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Intersphinx ----------------------------------------------------------

# Link with BERadio and Hiveeyes projects.
intersphinx_mapping = {
    "beradio": ("https://hiveeyes.org/docs/beradio/", None),
    "hiveeyes": ("https://hiveeyes.org/docs/system/", None),
    "hiveeyes-arduino": ("https://hiveeyes.org/docs/arduino/", None),
}

# Disable caching remote inventories completely.
# http://www.sphinx-doc.org/en/stable/ext/intersphinx.html#confval-intersphinx_cache_limit
# intersphinx_cache_limit = 0


# -- Link checker ---------------------------------------------------------

# A list of regular expressions that match documents in which Sphinx
# should not check the validity of links.
linkcheck_exclude_documents = [
    "development/backlog",
    "development/ideas",
    "development/notepad/.*",
    "development/research/.*",
]

# A list of regular expressions that match URIs that should not be checked when doing a linkcheck build.
linkcheck_ignore = [
    "http://daq.example.net",
    "http://kotori.example.org:3000/.*",
    "http://kotori.example.org.*",
    "https://htsql.org/",
    # Ignore GitHub anchors.
    "https://github.com/daq-tools/kotori/blob/.*#",
    "https://github.com/grafana/grafana/blob/.*#",
    "https://github.com/hiveeyes/arduino/blob/.*#",
    "https://github.com/influxdata/influxdb/blob/.*#",
]

# A list of regular expressions that match anchors Sphinx should skip when checking the validity of anchors in links.
linkcheck_anchors_ignore = [
    # "https://github.com/daq-tools/kotori/blob/",
]


# -- Pygments lexer -------------------------------------------------------

# Enable proper highlighting for inline PHP by tuning Pygments' PHP lexer.
# See also http://mbless.de/blog/2015/03/02/php-syntax-highlighting-in-sphinx.html

# Load PhpLexer
from pygments.lexers.web import PhpLexer
from sphinx.highlighting import lexers

# Enable highlighting for PHP code not between <?php ... ?> by default
lexers["php"] = PhpLexer(startinline=True)
lexers["php-annotations"] = PhpLexer(startinline=True)


# -- Options for MyST -------------------------------------------------

myst_heading_anchors = 3
myst_enable_extensions = [
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "linkify",
    "strikethrough",
    "tasklist",
]


# -- Runtime setup --------------------------------------------------------


def setup(app):
    # Foundation.
    # app.add_css_file("assets/css/font-entypo.css")
    app.add_css_file("assets/css/hexagons.min.css")
    app.add_js_file("assets/js/hexagons.min.js")

    # Application.
    app.add_css_file("css/kotori-sphinx.css")


# -- Attic ----------------------------------------------------------------

# TODO: Put those slogans back on the corresponding pages?
"""
"heroes": {
    "index": "A data historian based on InfluxDB, Grafana, MQTT and more.",
    "about/index": "A data historian based on InfluxDB, Grafana, MQTT and more.",
    "about/scenarios": "Conceived for consumers, integrators and developers.",
    "about/technologies": "Standing on the shoulders of giants.",
    "examples/index": "Telemetry data acquisition and sensor networks for humans.",
    "setup/index": "Easy to install and operate.",
},
"""
