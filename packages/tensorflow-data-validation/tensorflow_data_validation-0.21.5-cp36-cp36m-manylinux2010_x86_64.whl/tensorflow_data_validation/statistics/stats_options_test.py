# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for StatsOptions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from absl.testing import parameterized
from tensorflow_data_validation import types
from tensorflow_data_validation.statistics import stats_options
from tensorflow_data_validation.statistics.generators import lift_stats_generator
from tensorflow_data_validation.utils import slicing_util

from tensorflow.python.util.protobuf import compare  # pylint: disable=g-direct-tensorflow-import
from tensorflow_metadata.proto.v0 import schema_pb2

INVALID_STATS_OPTIONS = [
    {
        'testcase_name': 'invalid_generators',
        'stats_options_kwargs': {
            'generators': {}
        },
        'exception_type': TypeError,
        'error_message': 'generators is of type dict, should be a list.'
    },
    {
        'testcase_name': 'invalid_generator',
        'stats_options_kwargs': {
            'generators': [{}]
        },
        'exception_type': TypeError,
        'error_message': 'Statistics generator must extend one of '
                         'CombinerStatsGenerator, TransformStatsGenerator, '
                         'or CombinerFeatureStatsGenerator '
                         'found object of type dict.'
    },
    {
        'testcase_name': 'invalid_feature_whitelist',
        'stats_options_kwargs': {
            'feature_whitelist': {}
        },
        'exception_type': TypeError,
        'error_message': 'feature_whitelist is of type dict, should be a list.'
    },
    {
        'testcase_name': 'invalid_schema',
        'stats_options_kwargs': {
            'schema': {}
        },
        'exception_type': TypeError,
        'error_message': 'schema is of type dict, should be a Schema proto.'
    },
    {
        'testcase_name': 'invalid_slice_functions_list',
        'stats_options_kwargs': {
            'slice_functions': {}
        },
        'exception_type': TypeError,
        'error_message': 'slice_functions is of type dict, should be a list.'
    },
    {
        'testcase_name': 'invalid_slice_function_type',
        'stats_options_kwargs': {
            'slice_functions': [1]
        },
        'exception_type': TypeError,
        'error_message': 'slice_functions must contain functions only.'
    },
    {
        'testcase_name': 'sample_count_zero',
        'stats_options_kwargs': {
            'sample_count': 0
        },
        'exception_type': ValueError,
        'error_message': 'Invalid sample_count 0'
    },
    {
        'testcase_name': 'sample_count_negative',
        'stats_options_kwargs': {
            'sample_count': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid sample_count -1'
    },
    {
        'testcase_name': 'both_sample_count_and_sample_rate',
        'stats_options_kwargs': {
            'sample_count': 100,
            'sample_rate': 0.5
        },
        'exception_type': ValueError,
        'error_message': 'Only one of sample_count or sample_rate can be '
                         'specified.'
    },
    {
        'testcase_name': 'sample_rate_zero',
        'stats_options_kwargs': {
            'sample_rate': 0
        },
        'exception_type': ValueError,
        'error_message': 'Invalid sample_rate 0'
    },
    {
        'testcase_name': 'sample_rate_negative',
        'stats_options_kwargs': {
            'sample_rate': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid sample_rate -1'
    },
    {
        'testcase_name': 'sample_rate_above_one',
        'stats_options_kwargs': {
            'sample_rate': 2
        },
        'exception_type': ValueError,
        'error_message': 'Invalid sample_rate 2'
    },
    {
        'testcase_name': 'num_values_histogram_buckets_one',
        'stats_options_kwargs': {
            'num_values_histogram_buckets': 1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid num_values_histogram_buckets 1'
    },
    {
        'testcase_name': 'num_values_histogram_buckets_zero',
        'stats_options_kwargs': {
            'num_values_histogram_buckets': 0
        },
        'exception_type': ValueError,
        'error_message': 'Invalid num_values_histogram_buckets 0'
    },
    {
        'testcase_name': 'num_values_histogram_buckets_negative',
        'stats_options_kwargs': {
            'num_values_histogram_buckets': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid num_values_histogram_buckets -1'
    },
    {
        'testcase_name': 'num_histogram_buckets_negative',
        'stats_options_kwargs': {
            'num_histogram_buckets': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid num_histogram_buckets -1'
    },
    {
        'testcase_name': 'num_quantiles_histogram_buckets_negative',
        'stats_options_kwargs': {
            'num_quantiles_histogram_buckets': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid num_quantiles_histogram_buckets -1'
    },
    {
        'testcase_name': 'desired_batch_size_zero',
        'stats_options_kwargs': {
            'desired_batch_size': 0
        },
        'exception_type': ValueError,
        'error_message': 'Invalid desired_batch_size 0'
    },
    {
        'testcase_name': 'desired_batch_size_negative',
        'stats_options_kwargs': {
            'desired_batch_size': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid desired_batch_size -1'
    },
    {
        'testcase_name': 'semantic_domain_stats_sample_rate_zero',
        'stats_options_kwargs': {
            'semantic_domain_stats_sample_rate': 0
        },
        'exception_type': ValueError,
        'error_message': 'Invalid semantic_domain_stats_sample_rate 0'
    },
    {
        'testcase_name': 'semantic_domain_stats_sample_rate_negative',
        'stats_options_kwargs': {
            'semantic_domain_stats_sample_rate': -1
        },
        'exception_type': ValueError,
        'error_message': 'Invalid semantic_domain_stats_sample_rate -1'
    },
    {
        'testcase_name': 'semantic_domain_stats_sample_rate_above_one',
        'stats_options_kwargs': {
            'semantic_domain_stats_sample_rate': 2
        },
        'exception_type': ValueError,
        'error_message': 'Invalid semantic_domain_stats_sample_rate 2'
    },
]


class StatsOptionsTest(parameterized.TestCase):

  @parameterized.named_parameters(*INVALID_STATS_OPTIONS)
  def test_stats_options(self, stats_options_kwargs, exception_type,
                         error_message):
    with self.assertRaisesRegexp(exception_type, error_message):
      stats_options.StatsOptions(**stats_options_kwargs)

  def test_stats_options_json_round_trip(self):
    generators = [
        lift_stats_generator.LiftStatsGenerator(
            schema=None,
            y_path=types.FeaturePath(['label']),
            x_paths=[types.FeaturePath(['feature'])])
    ]
    feature_whitelist = ['a']
    schema = schema_pb2.Schema(feature=[schema_pb2.Feature(name='f')])
    label_feature = 'label'
    weight_feature = 'weight'
    slice_functions = [slicing_util.get_feature_value_slicer({'b': None})]
    sample_rate = 0.01
    num_top_values = 21
    frequency_threshold = 2
    weighted_frequency_threshold = 2.0
    num_rank_histogram_buckets = 1001
    num_values_histogram_buckets = 11
    num_histogram_buckets = 11
    num_quantiles_histogram_buckets = 11
    epsilon = 0.02
    infer_type_from_schema = True
    desired_batch_size = 100
    enable_semantic_domain_stats = True
    semantic_domain_stats_sample_rate = 0.1

    options = stats_options.StatsOptions(
        generators=generators,
        feature_whitelist=feature_whitelist,
        schema=schema,
        label_feature=label_feature,
        weight_feature=weight_feature,
        slice_functions=slice_functions,
        sample_rate=sample_rate,
        num_top_values=num_top_values,
        frequency_threshold=frequency_threshold,
        weighted_frequency_threshold=weighted_frequency_threshold,
        num_rank_histogram_buckets=num_rank_histogram_buckets,
        num_values_histogram_buckets=num_values_histogram_buckets,
        num_histogram_buckets=num_histogram_buckets,
        num_quantiles_histogram_buckets=num_quantiles_histogram_buckets,
        epsilon=epsilon,
        infer_type_from_schema=infer_type_from_schema,
        desired_batch_size=desired_batch_size,
        enable_semantic_domain_stats=enable_semantic_domain_stats,
        semantic_domain_stats_sample_rate=semantic_domain_stats_sample_rate)

    options_json = options.to_json()
    options = stats_options.StatsOptions.from_json(options_json)

    self.assertIsNone(options.generators)
    self.assertEqual(feature_whitelist, options.feature_whitelist)
    compare.assertProtoEqual(self, schema, options.schema)
    self.assertEqual(label_feature, options.label_feature)
    self.assertEqual(weight_feature, options.weight_feature)
    self.assertIsNone(options.slice_functions)
    self.assertEqual(sample_rate, options.sample_rate)
    self.assertEqual(num_top_values, options.num_top_values)
    self.assertEqual(frequency_threshold, options.frequency_threshold)
    self.assertEqual(weighted_frequency_threshold,
                     options.weighted_frequency_threshold)
    self.assertEqual(num_rank_histogram_buckets,
                     options.num_rank_histogram_buckets)
    self.assertEqual(num_values_histogram_buckets,
                     options.num_values_histogram_buckets)
    self.assertEqual(num_histogram_buckets, options.num_histogram_buckets)
    self.assertEqual(num_quantiles_histogram_buckets,
                     options.num_quantiles_histogram_buckets)
    self.assertEqual(epsilon, options.epsilon)
    self.assertEqual(infer_type_from_schema, options.infer_type_from_schema)
    self.assertEqual(desired_batch_size, options.desired_batch_size)
    self.assertEqual(enable_semantic_domain_stats,
                     options.enable_semantic_domain_stats)
    self.assertEqual(semantic_domain_stats_sample_rate,
                     options.semantic_domain_stats_sample_rate)

  def test_stats_options_from_json(self):
    options_json = """{
      "_generators": null,
      "_feature_whitelist": null,
      "_schema": null,
      "weight_feature": null,
      "label_feature": null,
      "_slice_functions": null,
      "_sample_count": null,
      "_sample_rate": null,
      "num_top_values": 20,
      "frequency_threshold": 1,
      "weighted_frequency_threshold": 1.0,
      "num_rank_histogram_buckets": 1000,
      "_num_values_histogram_buckets": 10,
      "_num_histogram_buckets": 10,
      "_num_quantiles_histogram_buckets": 10,
      "epsilon": 0.01,
      "infer_type_from_schema": false,
      "_desired_batch_size": null,
      "enable_semantic_domain_stats": false,
      "_semantic_domain_stats_sample_rate": null
    }"""
    actual_options = stats_options.StatsOptions.from_json(options_json)
    expected_options_dict = stats_options.StatsOptions().__dict__
    self.assertEqual(expected_options_dict, actual_options.__dict__)


if __name__ == '__main__':
  absltest.main()
