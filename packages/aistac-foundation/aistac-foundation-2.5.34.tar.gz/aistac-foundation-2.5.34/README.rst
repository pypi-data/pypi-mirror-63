Discovery Foundation
####################

The purpose of this foundation package is to provide a common platform through a set of abstractions that support the
core objectives of the Accelerated Machine Learning initiative. it applies the concepts of Parameterised Intent and
its Separation of Concerns (SoC), based around advanced OOD patterns, to provide a common foundation to differing
needs of data scientist and productisation coders while sharing common ideas and their implementation.

**Parametrized Intent** is a unique technique extracting the ideas and thinking of the data scientist or development
specialist from their discovery code and capturing it as intent with parameters that can be replayed in a
productionized environment. This decoupling and Separation of Concern between data, code and intended actions
considerably improves transparancy of ideas, code reuse and reduced time to market.

**Accelerated Machine Learning** is a unique approach around machine learning that innovates the data science discovery
vertical and productization of the data science delivery model. More specifically, it is an incubator project that
shadowed a team of Ph.D. data scientists in connection with the development and delivery of machine learning
initiatives to define measurable benefit propositions for customer success. To accomplish this, the project developed
specific and unique knowledge regarding transition and preparation of data sets for algorithmic execution and
augmented knowledge, which is at the core of the projects services offerings. From this the project developed a new
approach to data science discovery and productization dubbed “Accelerated Machine Learning”.

.. class:: no-web no-pdf

|pypi| |rdt| |license| |wheel|


.. contents::

.. section-numbering::

Installation
============

package install
---------------



The best way to install this package is directly from the Python Package Index repository using pip

.. code-block:: bash

    $ pip install discovery-foundation

if you want to upgrade your current version then using pip

.. code-block:: bash

    $ pip install --upgrade discovery-foundation

Package Overview
================

AbstractComponent
-----------------

The ``AbstractComponent`` class is a foundation class for the component build. It provides an encapsulated view of
the Property Management and Parameterised Intent

Abstract AI Single Task Application Component (AI-STAC) component class provides all the basic building blocks
of a components build including property management, augmented knowledge notes and parameterised intent pipeline.

For convenience there are two Factory Initialisation methods available ``from_env(...)`` and ``from_uri(...)`` the
second being an abstract method. This factory method initialises the concrete PropertyManager and IntentModel
classes and should use the parent ``_init_properties(...)`` methods to set the properties connector

As an example concrete implemntation of this method:

.. code-block:: python

        def __init__(self, property_manager: ExamplePropertyManager, intent_model: ExampleIntentModel,
                     default_save=None):
            super().__init__(property_manager=property_manager, intent_model=intent_model, default_save=default_save,
                             default_module='aistac.handlers.python_handlers',
                             default_source_handler='PythonSourceHandler',
                             default_persist_handler='PythonPersistHandler')

        @classmethod
        def from_uri(cls, task_name: str, uri_pm_path: str, pm_file_type: str = None, pm_module: str = None,
                     pm_handler: str = None, default_save = None, template_source_path: str = None,
                     template_persist_path: str = None, template_source_module: str = None,
                     template_persist_module: str = None, template_source_handler: str = None,
                     template_persist_handler: str = None, **kwargs):
            _pm = ExamplePropertyManager(task_name=task_name)
            _intent_model = ExampleIntentModel(property_manager=_pm)
            super()._init_properties(property_manager=_pm, uri_pm_path=uri_pm_path, **kwargs)
            super()._add_templates(property_manager=_pm, is_source=True, path=template_source_path,
                                   module=template_source_module, handler=template_source_handler)
            super()._add_templates(property_manager=_pm,is_source=False, path=template_persist_path,
                                   module=template_persist_module, handler=template_persist_handler)
            return cls(property_manager=_pm, intent_model=_intent_model, default_save=default_save)

To implement a new remote class Factory Method follow the method naming convention '_from_remote_<schema>()'
where <schema> is the uri schema name. this method should be a @classmethod and return a tuple of
module_name and handler.

For example if we were using an AWS S3 where the schema is s3:// the Factory method be similar to:

.. code-block:: python

    @classmethod
    def _from_remote_s3(cls) -> (str, str):
        _module_name = 'ds_discovery.handler.aws_s3_handlers'
        _handler = 'AwsS3PersistHandler'
        return _module_name, _handler


AbstractPropertyManager
-----------------------
The ``AbstractPropertiesManager`` facilitates the management of all the contract properties  including that of the
connector handlers, parameterised intent and Augmented Knowledge

Abstract AI Single Task Application Component (AI-STAC) class that creates a super class for all properties
managers

The Class initialisation is abstracted and is the only abstracted method. A concrete implementation of the
overloaded ``__init__`` manages the ``root_key`` and ``knowledge_key`` for this construct. The ``root_key`` adds a key
property reference to the root of the properties and can be referenced directly with ``<name>_key``. Likewise
the ``knowledge_key`` adds a catalog key to the restricted catalog keys.

More complex ``root_key`` constructs, where a grouping of keys might be desirable, passing a dictionary of name
value pairs as part of the list allows a root base to group related next level keys. For example

.. code-block:: python

    root_key = [{base: [primary, secondary}]

would add ``base.primary_key`` and ``base.secondary_key`` to the list of keys.

Here is a default example of an initialisation method:

.. code-block:: python

        def __init__(self, task_name: str):
            # set additional keys
            root_keys = []
            knowledge_keys = []
            super().__init__(task_name=task_name, root_keys=root_keys, knowledge_keys=knowledge_keys)


The property manager is not responsible for persisting the properties but provides the methods to load and persist
its in memory structure. To initialise the load and persist a ConnectorContract must be set up.

The following is a code snippet of setting a ConnectorContract and loading its content

.. code-block:: python

            self.set_property_connector(connector_contract=connector_contract)
            if self.get_connector_handler(self.CONNECTOR_PM_CONTRACT).exists():
                self.load_properties(replace=replace)

When using the property manager it will not automatically persist its properties and must be explicitely managed in
the component class. This removes the persist decision making away from the property manager. To persist the
properties use the method call ``persist_properties()``


AbstractIntentModel
-------------------
The ``AbstractIntentModel`` facilitates the Parameterised Intent, giving the base methods to record and replay intent.

Abstract AI Single Task Application Component (AI-STAC) Class for Parameterised Intent containing parameterised
intent registration methods ``_intent_builder(...)`` and ``_set_intend_signature(...)``.

it is creating a construct initialisation to allow for the control and definition of an ``intent_param_exclude``
list, ``default_save_intent`` boolean and a ``default_intent_level`` value.

As an example of an initialisation method

.. code-block:: python

    def __init__(self, property_manager: AbstractPropertyManager, default_save_intent: bool=None,
                 intent_next_available: bool=None):
        # set all the defaults
        default_save_intent = default_save_intent if isinstance(default_save_intent, bool) else True
        default_intent_level = -1 if isinstance(intent_next_available, bool) and intent_next_available else 0
        intent_param_exclude = ['inplace', 'canonical']
        super().__init__(property_manager=property_manager, intent_param_exclude=intent_param_exclude,
                         default_save_intent=default_save_intent, default_intent_level=default_intent_level)

in order to define the run pattern for the component task ``run_intent_pipeline(...)`` is an abstracted method
that defines the run pipeline of the intent.

As an example of a run_pipeline that iteratively updates a canonical with each intent

.. code-block:: python

        def run_intent_pipeline(self, canonical, levels: [int, str, list]=None, inplace: bool=False, **kwargs):
            inplace = inplace if isinstance(inplace, bool) else False
            # test if there is any intent to run
            if self._pm.has_intent() and not inplace:
                # create the copy and use this for all the operations
                if not inplace:
                    with threading.Lock():
                        canonical = deepcopy(canonical)
                # get the list of levels to run
                if isinstance(levels, (int, str, list)):
                    levels = self._pm.list_formatter(levels)
                else:
                    levels = sorted(self._pm.get_intent().keys())
                for level in levels:
                    for method, params in self._pm.get_intent(level=level).items():
                        if method in self.__dir__():
                            if isinstance(kwargs, dict):
                                params.update(kwargs)
                            canonical = eval(f"self.{method}(canonical, inplace=False, save_intent=False, **{params})")
            if not inplace:
                return canonical
            return

    the code signature for an intent method would have the following construct

.. code-block:: python

    def <intent_method_sig>(self, ...<intent parameters>..., save_intent: bool=True, intent_level: [int, str]=None):
        # resolve intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, save_intent=save_intent)

        # intend code block on the canonical
        ...


Reference
=========

Python version
--------------

Python 2.6 and 2.7 are not supported nor is Python 3.5. Although Python 3.6 is supported, it is recommended to install
``discovery-foundation`` against the latest Python 3.7> whenever possible.
Python 3 is the default for Homebrew installations starting with version 0.9.4.

GitHub Project
--------------
Discovery-Transitioning-Utils: `<https://github.com/Gigas64/discovery-foundation>`_.

Change log
----------

See `CHANGELOG <https://github.com/doatridge-cs/discovery-foundation/blob/master/CHANGELOG.rst>`_.


Licence
-------

BSD-3-Clause: `LICENSE <https://github.com/doatridge-cs/discovery-foundation/blob/master/LICENSE.txt>`_.


Authors
-------

`Gigas64`_  (`@gigas64`_) created discovery-foundation.


.. _pip: https://pip.pypa.io/en/stable/installing/
.. _Github API: http://developer.github.com/v3/issues/comments/#create-a-comment
.. _Gigas64: http://opengrass.io
.. _@gigas64: https://twitter.com/gigas64


.. |pypi| image:: https://img.shields.io/pypi/pyversions/Django.svg
    :alt: PyPI - Python Version

.. |rdt| image:: https://readthedocs.org/projects/discovery-foundation/badge/?version=latest
    :target: http://discovery-transitioning-utils.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |license| image:: https://img.shields.io/pypi/l/Django.svg
    :target: https://github.com/Gigas64/discovery-foundation/blob/master/LICENSE.txt
    :alt: PyPI - License

.. |wheel| image:: https://img.shields.io/pypi/wheel/Django.svg
    :alt: PyPI - Wheel

