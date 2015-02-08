file_content = \
"""
.. My Train Application documentation master file, created by
   sphinx-quickstart on Mon Jul  7 12:48:25 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MTA documentation!
================================================

**Applications**:

.. toctree::
  :maxdepth: 2

{0}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


"""

sub_file_content = \
"""
.. My Train Application documentation master file, created by
   sphinx-quickstart on Mon Jul  7 12:48:25 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation of {0}
================================================

.. toctree::
    :maxdepth: 2

{1}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

"""


mini_text = \
"""
{0}
------------------

.. automodule:: {1}
    :members:
"""

app_structure = \
"""
`{0} 
<{1}.html>`_
"""

include_text = "    source/{0}\n"
