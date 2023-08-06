import enum


class Stimulus(enum.Enum):
    """This enumeration describes known stimulus types used in the dataset. The presentation of such stimuli is modeled,
    to some degree, by the :class:`v2_dataset.model.protocol.Protocol` entity type and its subclasses.
    """

    GRATING = 0
    MB = 1
