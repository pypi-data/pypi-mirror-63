jsomark
#######

.. image:: https://travis-ci.org/knowark/jsomark.svg?branch=master
    :target: https://travis-ci.org/knowark/jsomark

.. image:: https://codecov.io/gh/knowark/jsomark/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/knowark/jsomark

JSON <-> XML parsing and composing convention.


What is jsomark?
================

jsomark is a JSON to XML translation convention. jsomark accepts json in an
standardized format and converts it to XML. It should as well reverse the
operation and produce a JSON document from an XML one.

Usage
=====

To **create an XML** from a **JSON** document just use
the **json_to_xml** function:

.. code-block:: python

    from jsomark import json_to_xml
    
    json_data = b'{"hello": "world"}'

    xml_data = json_to_xml(json_data)

    assert xml_data == b'<hello>world</hello>'

*jsomark* also supports more complex documents, like **nested json**
structures and Python json serializable **dictionaries**:


.. code-block:: python

    from jsomark import json_to_xml
    
    json_data = {
        "Company": {
            "Name": "Knowark",
            "Country": "Colombia"
        }
    }

    xml_data = json_to_xml(json_data)

    assert xml_data == (
        b'<Company><Name>Knowark</Name><Country>Colombia</Country></Company>')


Attributes
----------

XML can carry more information (i.e. metadata) than JSON, that is why a
convention in the format of a converting json document is needed to match the
original XML semantics. In *jsomark*, **attributes** are defined with
the **symbol "&"**:

.. note::
    Attribute values can only be **text** or **bytes**

.. code-block:: python

    from jsomark import json_to_xml

    json_data = {
        "Device": {
            "Reference": {
                "&": {"ID": "XYZ2020", "Serial": "S10987"}
            }
        }
    }

    xml_data = json_to_xml(json_data)

    assert xml_data == (
        b'<Device><Reference ID="XYZ2020" Serial="S10987"/></Device>')

If the key with attributes also has a **text content**, then the
**symbol "#"** should be used to carry it:


.. code-block:: python

    from jsomark import json_to_xml

    json_data = {
        "Employee": {
            "Company": {
                "&": {"VAT": "900123765"},
                "#": "Servagro"
            }
        }
    }

    xml_data = json_to_xml(json_data)

    assert xml_data == (
        b'<Employee><Company VAT="900123765">Servagro</Company></Employee>')

.. note::
    If a JSON key doesn't have attributes, its value becomes the text
    of the resulting XML element as seen in the previous examples.


Lists
-----

Lists in the JSON document are interpreted as **repeating elements**
inside the generated XML.


.. code-block:: python

    from jsomark import json_to_xml

    json_data = {
        "Order": {
            "Line": [
                {"&": {"ID": "1"}, "#": "Chocolate Ice Cream"},
                {"&": {"ID": "2"}, "#": "Banana Split"},
                {"&": {"ID": "3"}, "#": "Caramel Cake"}
            ]
        }
    }

    xml_data = json_to_xml(json_data)

    assert xml_data == (
        b'<Order><Line ID="1">Chocolate Ice Cream</Line>'
        b'<Line ID="2">Banana Split</Line>'
        b'<Line ID="3">Caramel Cake</Line></Order>')


Namespaces
----------

In jsomark, namespaces are provided as a **separate dictionary** whose keys
are the prefixes that must be used in the json document itself. The default
namespace should be set in the *'None'* key of the namespaces dictionary and
its keys in the json document don't have to be prefixed:

.. Note::
    Don't miss the **":"** separator in the non-default namespaced key
    such as *'isbn:number'* in the following example.

.. code-block:: python

    from jsomark import json_to_xml

    namespaces = {
        None: 'urn:loc.gov:books',
        'isbn': 'urn:ISBN:0-395-36341-6'
    }

    json_data = {
        "book": {
            "title": "Cheaper by the Dozen",
            "isbn:number": 1568491379
        }
    }

    xml_data = json_to_xml(json_data, namespaces=namespaces)

    assert xml_data == (
        b'<book xmlns="urn:loc.gov:books" xmlns:isbn="urn:ISBN:0-395-36341-6">'
        b'<title>Cheaper by the Dozen</title>'
        b'<isbn:number>1568491379</isbn:number></book>'
