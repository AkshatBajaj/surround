# surround.py
#
# Manages a set of stages and the data that is passed between them.
import logging

LOGGER = logging.getLogger(__name__)

class Frozen():
    """
    A class that can toggle the ability of adding new attributes.
    When the class is considered frozen, adding new attributes will
    trigger a :exc:`TypeError` exception.
    """

    __isfrozen = False

    def __setattr__(self, key, value):
        """
        Called when an attribute is created/modified, throws an exception when frozen and adding a new attribute.
        Otherwise sets the attribute at the provided key to the provided value.

        :param key: the name of the attribute
        :type key: string
        :param value: the new value of the attribute
        :type value: any
        """

        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen object" % self)
        object.__setattr__(self, key, value)

    def freeze(self):
        """
        Freeze this class, throw exceptions from now on when a new attribute is added.
        """

        self.__isfrozen = True

    def thaw(self):
        """
        Thaw the class, no longer throw exceptions on new attributes.
        """

        self.__isfrozen = False


class State(Frozen):
    """
    Stores the data to be passed between each stage in a pipeline.
    Each stage is responsible for setting the attributes to this class.

    Formerly know as ``SurroundData``.

    **Attributes:**

    - `stage_metadata` (:class:`list`) - information that can be used to identify the stage
    - `execution_time` (:class:`str`) - how long it took to execute the entire pipeline
    - `errors` (:class:`list`) - list of error messages (stops the pipeline when appended to)
    - `warnings` (:class:`list`) - list of warning messages (displayed in console)

    Example::

        class AssemblyState(State):
            # Extra attributes must be defined before the pipeline is ran!
            input_data = None
            output_data = None

            def __init__(self, input_data)
                self.input_data = input_data


        class Predict(Estimator):
            # Do prediction here

        pipeline = Assembler("Example")
                    .set_stages([Predict()])
        pipeline.init_assembler()

        data = PipelineData("received data")
        pipeline.run(data)

        print(data.output_data)

    .. note::
        This class is frozen when the pipeline is being ran.
        This means that an exception will be thrown if a new attribute
        is added during pipeline execution.
    """

    def __init__(self):
        self.stage_metadata = []
        self.execution_time = []
        self.errors = []
        self.warnings = []
        self.metrics = {}
