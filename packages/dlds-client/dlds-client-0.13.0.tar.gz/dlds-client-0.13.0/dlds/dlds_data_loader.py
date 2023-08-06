import os
import json
from collections import OrderedDict
from copy import copy, deepcopy
from typing import Dict, List, Optional
from enum import Enum

from tqdm import tqdm

import numpy as np

from dlds import DLDSClient

from dlds.decoder.dlds_decoder import *


# from dlds.decoder.opencv_decoder import *


class LoadMode(Enum):
    PRELOAD = 0
    ADHOC = 1
    ADHOC_CACHED = 2


class DLDSDataLoader:
    """Data loader for data from the Data Spree Vision Platform"""

    def __init__(self, dlds_client: DLDSClient, network_model: Dict, dataset_directory: str,
                 mode: LoadMode = LoadMode.ADHOC_CACHED,
                 allowed_status=('annotated', 'reviewed'), decoder: DLDSDecoder = None,
                 distinct_items_per_category: bool = True):
        """
        """
        self._dlds_client = dlds_client
        self._network_model = network_model
        self._dataset_directory = dataset_directory
        self._mode = mode
        self._allowed_status = allowed_status
        self._decoders = []

        if decoder is None:
            pass  # self.add_decoder(DefaultDecoder)
        else:
            self.add_decoder(decoder)

        self._items = {}

        # load class label ids and names that are used within this model
        self._class_labels = dlds_client.get_model_class_labels(network_model['id'])

        #### refactoring datasubsets ####
        # TODO: deprecated dataset api
        # use whole dataset(s), split them into train and eval and use them in case no subset is given

        # get all categories and aggregate the respective subset IDs
        self._subsets_ids_by_category = {}
        for entry in network_model['data_subsets']:
            if entry['category'] not in self._subsets_ids_by_category.keys():
                self._subsets_ids_by_category[entry['category']] = []
            if entry['data_subset'] not in self._subsets_ids_by_category[entry['category']]:
                self._subsets_ids_by_category[entry['category']].append(entry['data_subset'])

        # get all subset IDs
        subset_ids = []
        condensed_subset_ids = [self._subsets_ids_by_category[cat] for cat in self._subsets_ids_by_category.keys()]
        for subset_id in [item for sublist in condensed_subset_ids for item in sublist]:
            subset_ids.append(subset_id)

        # get all item IDs
        self._item_ids = set()
        self._item_ids_by_subset = {}
        for subset_id in subset_ids:
            if subset_id not in self._item_ids_by_subset:
                self._item_ids_by_subset[subset_id] = []

            subset_item_details = self._dlds_client.get_data_subset_items(subset_id)
            for item in subset_item_details:
                # del item['name']
                # del item['updated_date']
                if item['status'] in self._allowed_status:
                    item['exists'] = False
                    self._items[item['id']] = item
                    self._item_ids_by_subset[subset_id].append(item['id'])
                    self._item_ids.add(item['id'])

        self._item_ids = list(self._item_ids)

        self._item_ids_by_category = {}
        for category in self._subsets_ids_by_category.keys():
            for subset_id in self._subsets_ids_by_category[category]:
                if category not in self._item_ids_by_category:
                    if distinct_items_per_category:
                        self._item_ids_by_category[category] = set()
                    else:
                        self._item_ids_by_category[category] = list()

                if distinct_items_per_category:
                    self._item_ids_by_category[category].update(self._item_ids_by_subset[subset_id])
                else:
                    self._item_ids_by_category[category].extend(self._item_ids_by_subset[subset_id])

            if distinct_items_per_category:
                self._item_ids_by_category[category] = list(self._item_ids_by_category[category])

        if self._mode == LoadMode.PRELOAD:
            for item_id in tqdm(self._item_ids):
                image_directory = os.path.join(self._dataset_directory, str(self._items[item_id]['dataset']), 'images')
                annotation_directory = os.path.join(self._dataset_directory, str(self._items[item_id]['dataset']),
                                                    'annotations')
                #image_file_name = self._items[item_id]['name'].split('/')[-1]

                item = self._items[item_id]
                dataset_id = item['dataset']
                item_name = item['name'].split('/')[-1]
                image_file_name = '{}_{}_{}'.format(dataset_id, item_id, item_name)
                annotation_file_name = image_file_name.split('.')[0] + '.json'
                image_path = os.path.join(image_directory, image_file_name)
                annotation_path = os.path.join(annotation_directory, annotation_file_name)
                if os.path.exists(image_path) and os.path.exists(annotation_path):
                    item['exists'] = True
                else:
                    self._dlds_client.download_dataset_item(item_id, image_dir=image_directory,
                                                            annotation_dir=annotation_directory,
                                                            accepted_status=self._allowed_status,
                                                            return_item=False)
                    #item['exists'] = False

    def add_decoder(self, decoder):
        self._decoders.append(decoder)

    def get_class_labels(self) -> List[Dict]:
        """Get the list of class labels that are selected for the loaded model.

        :return: List containing the class labels with ID and name.
        """
        return copy(self._class_labels)

    def get_categories(self) -> List[str]:
        """List containing the names of all categories.

        :return: List of category names.
        """
        return list(self._item_ids_by_category.keys())

    def get_subset_ids(self, category=None) -> List[int]:
        """List containing the IDs of the subsets of the specified category or all subsets.

        :param category: Category to filter the subset IDs.
        :return: List of subset IDs.
        """

        if category is None:
            return list(self._item_ids_by_subset.keys())
        else:
            return list(self._subsets_ids_by_category[category])

    def get_item_ids(self) -> List[int]:
        """List containing the IDs of all items.

        This list contains unique item IDs, e.g. an item that belongs to multiple subsets is only listed once.

        :return: List of item IDs.
        """
        return copy(list(set(self._item_ids)))

    def get_item_ids_by_category(self, category) -> List[int]:
        """Get the IDs of all items that belong to the specified category.

        :param category: Category to filter the item IDs.
        :return: List of item IDs.
        """
        return copy(self._item_ids_by_category.get(category, []))

    def get_item_ids_by_subset(self, subset_id):
        """Get the IDs of all items that belong to the specified subset.

        :param subset_id: ID of a subset.
        :return: List of item IDs.
        """
        return copy(self._item_ids_by_subset.get(subset_id, []))

    def get_item(self, item_id) -> Optional[Dict]:
        """Get dataset item given its ID.

        :param item_id: ID of the item.
        :param load_image:
        :return: Dictionary containing the image and meta data or None if the item does not exist.
        >>> {
        >>> 'id': int,
        >>> 'image': [],
        >>> 'annotations': Dict
        >>> }
        """

        # get item, only returns if item is already downloaded
        data = None
        item = self._items.get(item_id)
        image_directory = os.path.join(self._dataset_directory, str(item['dataset']), 'images')
        annotation_directory = os.path.join(self._dataset_directory, str(item['dataset']), 'annotations')

        image_file_name = item['name'].split('/')[-1]

        item_id = item['id']
        dataset_id = item['dataset']
        item_name = item['name'].split('/')[-1]
        image_file_name = '{}_{}_{}'.format(dataset_id, item_id, item_name)

        annotation_file_name = os.path.splitext(image_file_name)[0] + '.json'
        image_path = os.path.join(image_directory, image_file_name)
        annotation_path = os.path.join(annotation_directory, annotation_file_name)

        item['exists'] = os.path.exists(image_path) and os.path.exists(annotation_path)

        item_serialized = None
        if not item['exists']:
            if self._mode == LoadMode.PRELOAD:
                item_serialized = self._dlds_client.download_dataset_item(item_id, image_dir=image_directory,
                                                                          annotation_dir=annotation_directory,
                                                                          accepted_status=self._allowed_status,
                                                                          return_item=True)
                if item_serialized is not None:
                    item['exists'] = True
                else:
                    raise FileNotFoundError('item not found')

            if self._mode == LoadMode.ADHOC:
                item_serialized = self._dlds_client.download_dataset_item(item_id, image_dir=None,
                                                                          annotation_dir=None,
                                                                          accepted_status=self._allowed_status,
                                                                          return_item=True)
                if item_serialized is None:
                    raise FileNotFoundError('item not found')

            if self._mode == LoadMode.ADHOC_CACHED:
                item_serialized = self._dlds_client.download_dataset_item(item_id, image_dir=image_directory,
                                                                          annotation_dir=annotation_directory,
                                                                          accepted_status=self._allowed_status,
                                                                          return_item=True)
                if item_serialized is not None:
                    item['exists'] = True
                else:
                    raise FileNotFoundError('item not found')

            if item_serialized is None:
                raise Exception('Can not receive item.')

            annotations = item_serialized['annotations']

        elif item['exists']:
            with open(image_path, 'rb') as f:
                item_serialized = {
                    'image': f.read()
                }
            with open(annotation_path, 'r') as f:
                annotations = json.load(f)
            if annotations is None:
                annotations = {}
        else:
            raise ValueError('item is corrupted.')

        # deserialize
        item_file_extension = os.path.splitext(item['name'])[1].lower().replace('.', '')
        deserialized = False
        if self._decoders:
            for decoder in self._decoders:
                extensions = decoder.get_file_extensions()
                if item_file_extension in extensions:
                    data = decoder(item_serialized['image'])
                    deserialized = True
                    # instead of break add datatype to sample dict with
                    break
        if not deserialized:
            data = item_serialized['image']

        sample = {
            'id': item_id,
            'image': data,
            'data_type': item_file_extension,
            'annotations': annotations
        }

        return sample
