import numpy as np

from .base import Model
from .stimulus import Stimulus
from colour import Color
from functools import lru_cache
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, or_
from v2_dataset import units
from v2_dataset.orm import Column, RangeConstraint, StrictForeignKey, mixins, types


class Protocol(Model, mixins.PolymorphicBase):
    name = Column(types.String, primary_key=True, nullable=False)
    stimulus = Column(types.Enum(Stimulus))
    trials_per_condition = Column(types.Integer)
    condition_time_ms = Column(types.Integer)
    pre_trial_time_ms = Column(types.Integer)
    post_trial_time_ms = Column(types.Integer)
    visual_field_deg = Column(types.Integer)
    comment = Column(types.String())

    # TODO: Constraint temporarily lifted, because dataset contents 0.4.1 contain uncurated protocols with lots of NULL.
    # __table_args__ = (
    #     UniqueConstraint(
    #         stimulus,
    #         trials_per_condition,
    #         condition_time_ms,
    #         pre_trial_time_ms,
    #         post_trial_time_ms,
    #         visual_field_deg,
    #     ),
    # )

    def __getitem__(self, item):
        return self._conditions_map[item]

    @property
    @lru_cache(maxsize=None)
    def _conditions_map(self):
        return {c.code: c for c in self.conditions}

    @property
    @lru_cache(maxsize=None)
    def condition_groups(self):
        """
        :rtype: Dict[str, List[Condition]]
        """
        groups = set(c.group for c in self.conditions)
        result = {g: [c for c in self.conditions if c.group == g] for g in groups}
        return result

    @property
    def condition_time(self):
        return self.condition_time_ms * units.ms

    @property
    def post_trial_time(self):
        return self.post_trial_time_ms * units.ms

    @property
    def pre_trial_time(self):
        return self.pre_trial_time_ms * units.ms

    @property
    def total_trial_time(self):
        return self.pre_trial_time + self.condition_time + self.post_trial_time

    @property
    def visual_field(self):
        return self.visual_field_deg * units.deg

    @lru_cache(maxsize=None)
    def no_conditions(self, stimulus_only=False):
        condition_set = [
            cond for cond in self.conditions if not stimulus_only or cond.is_stimulus
        ]
        return len(condition_set)


class Gratings(Protocol, mixins.PolymorphicDerived):
    name = Column(
        types.String, StrictForeignKey(Protocol.name), primary_key=True, nullable=False
    )

    def as_array(self, sf_unit="1/radian", tf_unit="hertz", orient_unit="radian"):
        """
        :param sf_unit: Union[str, pint.Unit]
        :param tf_unit: Union[str, pint.Unit]
        :param orient_unit: Union[str, pint.Unit]
        :return: numpy.ndarray
        """
        return np.array(
            [
                (
                    c.group,
                    c.code,
                    c.contrast,
                    c.spatial_freq.to(sf_unit).m,
                    c.speed.to(tf_unit).m,
                    c.orientation.to(orient_unit),
                    np.array(c.color_a.rgb),
                    np.array(c.color_b.rgb),
                )
                for c in self.conditions
                if c.is_stimulus
            ],
            dtype=[
                ("group", "U20"),
                ("code", "u2"),
                ("contrast", "f4"),
                ("sf", "f4"),
                ("tf", "f4"),
                ("orient", "f4"),
                ("color_a", "(3,)f4"),
                ("color_b", "(3,)f4"),
            ],
        )


class MovingBars(Protocol, mixins.PolymorphicDerived):
    name = Column(
        types.String, StrictForeignKey(Protocol.name), primary_key=True, nullable=False
    )
    bar_length_deg = Column(types.Float, nullable=False)
    bar_width_deg = Column(types.Float, nullable=False)
    bar_speed_deg_per_s = Column(types.Float, nullable=False)

    __table_args__ = (
        CheckConstraint(bar_length_deg > 0),
        CheckConstraint(bar_width_deg > 0),
        CheckConstraint(bar_speed_deg_per_s > 0),
    )

    @property
    def bar_length(self):
        return self.bar_length_deg * units.deg

    @property
    def bar_speed(self):
        return self.bar_speed_deg_per_s * units.deg / units.sec

    @property
    def bar_width(self):
        return self.bar_width_deg * units.deg


class Condition(Model, mixins.PolymorphicBase):
    protocol_name = Column(
        types.String, StrictForeignKey(Protocol.name), primary_key=True, nullable=False
    )
    code = Column(types.Integer, primary_key=True, nullable=False)
    group = Column(types.String, nullable=True)

    is_stimulus = Column(types.Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint(code > 0),
        CheckConstraint(or_(code < 250, is_stimulus != None)),
    )


class GratingCondition(Condition, mixins.PolymorphicDerived):
    protocol_name = Column(types.String, primary_key=True, nullable=False)
    code = Column(types.Integer, primary_key=True, nullable=False)

    contrast = Column(types.Float)
    spatial_freq_invdeg = Column(types.Float)
    speed_hz = Column(types.Float)
    orientation_deg = Column(types.Float)
    color_a_hex = Column(types.String(7))
    color_b_hex = Column(types.String(7))

    __table_args__ = (
        RangeConstraint(contrast, 0, 1),
        CheckConstraint(spatial_freq_invdeg >= 0),
        CheckConstraint(speed_hz >= 0),
        RangeConstraint(orientation_deg, 0, 360, open_right=True),
        ForeignKeyConstraint(
            [protocol_name, code], [Condition.protocol_name, Condition.code]
        ),
    )

    @property
    def orientation(self):
        return self.orientation_deg * units.deg

    @property
    @lru_cache(maxsize=None)
    def is_colored(self):
        black = Color("black")
        white = Color("white")
        return (self.color_a not in [black, white]) and (
            self.color_b not in [black, white]
        )

    @property
    def spatial_freq(self):
        return self.spatial_freq_invdeg / units.deg

    @property
    def speed(self):
        return self.speed_hz * units.hertz

    @property
    @lru_cache(maxsize=None)
    def color_a(self):
        """
        :rtype: colour.Color
        """
        return Color(self.color_a_hex)

    @property
    @lru_cache(maxsize=None)
    def color_b(self):
        """
        :rtype: colour.Color
        """
        return Color(self.color_b_hex)


class MovingBarCondition(Condition, mixins.PolymorphicDerived):
    protocol_name = Column(types.String, primary_key=True, nullable=False)
    code = Column(types.Integer, primary_key=True, nullable=False)

    orientation_deg = Column(types.Float)

    __table_args__ = (
        RangeConstraint(orientation_deg, 0, 360, open_right=True),
        ForeignKeyConstraint(
            [protocol_name, code], [Condition.protocol_name, Condition.code]
        ),
    )

    @property
    def motion_direction(self):
        return self.orientation + 90 * units.deg

    @property
    def motion_vector(self):
        vector = np.array(
            [np.cos(self.motion_direction), np.sin(self.motion_direction)]
        )
        return vector

    @property
    def orientation(self):
        return self.orientation_deg * units.deg


Model.relate_1_to_n(Protocol, Condition, "conditions", "protocol")
