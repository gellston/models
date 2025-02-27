# Copyright 2020-2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Data operations, will be used in train.py."""

import mindspore as ms
import mindspore.dataset as de
from .model_utils.config import config


de.config.set_seed(1)
de.config.set_prefetch_size(512)


def create_transformer_dataset(rank_size=1, rank_id=0, do_shuffle="true", dataset_path=None,
                               bucket_boundaries=None, device_target="Ascend"):
    """create dataset"""
    def batch_per_bucket(bucket_len, dataset_path):
        dataset_path = dataset_path + "_" + str(bucket_len) + "_00"
        ds = de.MindDataset(dataset_path,
                            columns_list=["source_eos_ids", "source_eos_mask",
                                          "target_sos_ids", "target_sos_mask",
                                          "target_eos_ids", "target_eos_mask"],
                            shuffle=(do_shuffle == "true"), num_shards=rank_size, shard_id=rank_id)
        type_cast_op = de.transforms.c_transforms.TypeCast(ms.int32)
        ds = ds.map(operations=type_cast_op, input_columns="source_eos_ids")
        ds = ds.map(operations=type_cast_op, input_columns="source_eos_mask")
        ds = ds.map(operations=type_cast_op, input_columns="target_sos_ids")
        ds = ds.map(operations=type_cast_op, input_columns="target_sos_mask")
        ds = ds.map(operations=type_cast_op, input_columns="target_eos_ids")
        ds = ds.map(operations=type_cast_op, input_columns="target_eos_mask")

        # apply batch operations

        ds = ds.batch(config.batch_size, drop_remainder=True)
        return ds

    for i, _ in enumerate(bucket_boundaries):
        bucket_len = bucket_boundaries[i]
        ds_per = batch_per_bucket(bucket_len, dataset_path)
        if i == 0:
            ds = ds_per
        else:
            ds = ds + ds_per
    ds = ds.shuffle(ds.get_dataset_size())
    ds.channel_name = 'transformer'
    return ds
