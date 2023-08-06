# -*- coding: utf-8 -*-
from spaceone.inventory.model.collection_info_model import CollectionInfo, UpdateHistory

__all__ = ['CollectionInfo']


def UpdateHistoryInfo(update_history_vo: UpdateHistory):
    return {
        'key': update_history_vo.key,
        'updated_by': update_history_vo.updated_by,
        'updated_at': update_history_vo.updated_at
    }


def CollectionInfo(collection_info_vo: CollectionInfo):
    return {
        'state': collection_info_vo.state,
        'collectors': collection_info_vo.collectors,
        'update_history': list(map(UpdateHistoryInfo, collection_info_vo.update_history)),
        'pinned_keys': collection_info_vo.pinned_keys
    }