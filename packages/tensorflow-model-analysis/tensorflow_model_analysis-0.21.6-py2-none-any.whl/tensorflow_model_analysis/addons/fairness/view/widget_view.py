# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""View API for Fairness Indicators."""
from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

import tensorflow as tf
from tensorflow_model_analysis.addons.fairness.notebook import visualization
from tensorflow_model_analysis.api import model_eval_lib
from tensorflow_model_analysis.slicer import slicer_lib as slicer
from tensorflow_model_analysis.types_compat import Optional, Text, Dict, Callable, Any, List


def stringify_slice_key_value(slice_key):
  """Stringifies a slice key value.

  The string representation of a SingletonSliceKeyType is "feature:value". This
  function returns value.

  When
  multiple columns / features are specified, the string representation of a
  SliceKeyType's value is "v1_X_v2_X_..." where v1, v2, ... are values. For
  example,
  ('gender, 'f'), ('age', 5) becomes f_X_5. If no columns / feature
  specified, return "Overall".

  Note that we do not perform special escaping for slice values that contain
  '_X_'. This stringified representation is meant to be human-readbale rather
  than a reversible encoding.

  The columns will be in the same order as in SliceKeyType. If they are
  generated using SingleSliceSpec.generate_slices, they will be in sorted order,
  ascending.

  Technically float values are not supported, but we don't check for them here.

  Args:
    slice_key: Slice key to stringify. The constituent SingletonSliceKeyTypes
      should be sorted in ascending order.

  Returns:
    String representation of the slice key's value.
  """
  if not slice_key:
    return 'Overall'

  # Since this is meant to be a human-readable string, we assume that the
  # feature values are valid UTF-8 strings (might not be true in cases where
  # people store serialised protos in the features for instance).
  # We need to call as_str_any to convert non-string (e.g. integer) values to
  # string first before converting to text.
  # We use u'{}' instead of '{}' here to avoid encoding a unicode character with
  # ascii codec.
  values = [
      u'{}'.format(tf.compat.as_text(tf.compat.as_str_any(value)))
      for _, value in slice_key
  ]
  return '_X_'.join(values)


def convert_eval_result_to_ui_input(
    eval_result,
    slicing_column = None,
    slicing_spec = None,
    output_name = '',
    multi_class_key = ''):
  """Renders the Fairness Indicator view.

  Args:
    eval_result: An tfma.EvalResult.
    slicing_column: The slicing column to to filter results. If both
      slicing_column and slicing_spec are None, show all eval results.
    slicing_spec: The slicing spec to filter results. If both slicing_column and
      slicing_spec are None, show all eval results.
    output_name: The output name associated with metric (for multi-output
      models).
    multi_class_key: The multi-class key associated with metric (for multi-class
      models).

  Returns:
    A FairnessIndicatorViewer object if in Jupyter notebook; None if in Colab.

  Raises:
    ValueError if no related eval result found or both slicing_column and
    slicing_spec are not None.
  """
  if slicing_column and slicing_spec:
    raise ValueError(
        'Only one of the "slicing_column" and "slicing_spec" parameters '
        'can be set.')
  if slicing_column:
    slicing_spec = slicer.SingleSliceSpec(columns=[slicing_column])

  data = []
  for (slice_key, metric_value) in eval_result.slicing_metrics:
    slice_key_ok = (
        slicing_spec is None or not slice_key or
        slicing_spec.is_slice_applicable(slice_key))
    metric_ok = (
        output_name in metric_value and
        multi_class_key in metric_value[output_name])

    if slice_key_ok and metric_ok:
      data.append({
          'sliceValue': stringify_slice_key_value(slice_key),
          'slice': slicer.stringify_slice_key(slice_key),
          'metrics': metric_value[output_name][multi_class_key]
      })
  if not data:
    raise ValueError(
        'No eval result found for output_name:"%s" and '
        'multi_class_key:"%s" and slicing_column:"%s" and slicing_spec:"%s".' %
        (output_name, multi_class_key, slicing_column, slicing_spec))
  return data


def render_fairness_indicator(
    eval_result = None,
    multi_eval_results = None,
    slicing_column = None,
    slicing_spec = None,
    output_name = '',
    multi_class_key = '',
    event_handlers = None,
):
  """Renders the Fairness Indicator view.

  Args:
    eval_result: An tfma.EvalResult.
    multi_eval_results: A map of {string: tfma.EvalResult}. The key is the eval
      or model name.
    slicing_column: The slicing column to to filter results. If both
      slicing_column and slicing_spec are None, show all eval results.
    slicing_spec: The slicing spec to filter results. If both slicing_column and
      slicing_spec are None, show all eval results.
    output_name: The output name associated with metric (for multi-output
      models).
    multi_class_key: The multi-class key associated with metric (for multi-class
      models).
    event_handlers: The event handler callback.

  Returns:
    A FairnessIndicatorViewer object if in Jupyter notebook; None if in Colab.
  """
  if ((eval_result and multi_eval_results) or
      (not eval_result and not multi_eval_results)):
    raise ValueError(
        'Exactly one of the "eval_result" and "multi_eval_results" '
        'parameters must be set.')

  if (multi_eval_results and len(multi_eval_results) != 2):
    raise ValueError(
        '"multi_eval_results" parameter only accept 2 eval results.')

  data = None
  multi_data = None
  if eval_result:
    data = convert_eval_result_to_ui_input(eval_result, slicing_column,
                                           slicing_spec, output_name,
                                           multi_class_key)
  else:
    multi_data = {}
    for eval_name in multi_eval_results:
      multi_data[eval_name] = convert_eval_result_to_ui_input(
          multi_eval_results[eval_name], slicing_column, slicing_spec,
          output_name, multi_class_key)
  return visualization.render_fairness_indicator(data, multi_data,
                                                 event_handlers)
