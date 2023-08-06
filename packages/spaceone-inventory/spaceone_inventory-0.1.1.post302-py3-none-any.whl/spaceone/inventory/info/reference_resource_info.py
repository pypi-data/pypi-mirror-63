# -*- coding: utf-8 -*-

__all__ = ['ReferenceResourceInfo']


def ReferenceResourceInfo(reference_vo):
    if reference_vo:
        return {
            'resource_id': reference_vo.resource_id,
            'external_link': reference_vo.external_link
        }
    else:
        return {}
