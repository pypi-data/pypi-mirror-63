# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

from mixbox import entities
from mixbox import fields

import cybox.bindings.cybox_core as core_binding
from cybox.common import StructuredText, MeasureSource, Location
from cybox.common.vocabs import EventType, VocabField
from cybox.core import Actions, Frequency


class Event(entities.Entity):
    _binding = core_binding
    _binding_class = core_binding.EventType
    _namespace = 'http://cybox.mitre.org/cybox-2'

    id_ = fields.TypedField("id")
    idref = fields.TypedField("idref")

    type_ = VocabField("Type", EventType)
    description = fields.TypedField("Description", StructuredText)
    observation_method = fields.TypedField("Observation_Method", MeasureSource)
    actions = fields.TypedField("Actions", Actions)
    frequency = fields.TypedField("Frequency", Frequency)
    location = fields.TypedField("Location", Location)
    event = fields.TypedField("Event", type_="cybox.core.event.Event", multiple=True)
