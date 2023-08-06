# -*- coding: utf-8 -*-
import logging

__all__ = ['ReferenceResourceInfo']
_LOGGER = logging.getLogger(__name__)


def ReferenceResourceInfo(reference_vo):
    _LOGGER.debug(reference_vo)
    if reference_vo:
        _LOGGER.debug({
            'resource_id': reference_vo.resource_id,
            'external_link': reference_vo.external_link
        })
        return {
            'resource_id': reference_vo.resource_id,
            'external_link': reference_vo.external_link
        }
    else:
        {}
