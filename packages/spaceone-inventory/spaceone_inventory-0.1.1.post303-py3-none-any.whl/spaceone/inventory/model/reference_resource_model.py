# -*- coding: utf-8 -*-

from mongoengine import *


class ReferenceResource(EmbeddedDocument):
    resource_id = StringField(default=None, null=True)
    external_link = StringField(default=None, null=True)
