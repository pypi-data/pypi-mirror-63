# Copyright 2019 Google LLC
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
"""Implementation of algorithms required for premade models."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

from . import categorical_calibration_layer
from . import configs
from . import lattice_layer
from . import linear_layer
from . import pwl_calibration_layer
from . import pwl_calibration_lib

from absl import logging
import enum
import numpy as np
import six

import tensorflow as tf

# Layer names used for layers in the premade models.
INPUT_LAYER_NAME = 'tfl_input'
CALIB_LAYER_NAME = 'tfl_calib'
LATTICE_LAYER_NAME = 'tfl_lattice'
LINEAR_LAYER_NAME = 'tfl_linear'
OUTPUT_CALIB_LAYER_NAME = 'tfl_output_calib'

# Prefix for passthrough (identity) nodes for shared calibration.
# These nodes pass shared calibrated values to submodels in an ensemble.
CALIB_PASSTHROUGH_NAME = 'tfl_calib_passthrough'

# Prefix for defining feature calibrator regularizers.
_INPUT_CALIB_REGULARIZER_PREFIX = 'calib_'

# Prefix for defining output calibrator regularizers.
_OUTPUT_CALIB_REGULARIZER_PREFIX = 'output_calib_'


def _input_calibration_regularizers(model_config, feature_config):
  """Returns pwl layer regularizers defined in the model and feature configs."""
  regularizer_configs = []
  regularizer_configs.extend(feature_config.regularizer_configs or [])
  regularizer_configs.extend(model_config.regularizer_configs or [])
  return [(r.name.replace(_INPUT_CALIB_REGULARIZER_PREFIX, ''), r.l1, r.l2)
          for r in regularizer_configs
          if r.name.startswith(_INPUT_CALIB_REGULARIZER_PREFIX)]


def _output_calibration_regularizers(model_config):
  """Returns output calibration regularizers defined in the model config."""
  return [(r.name.replace(_OUTPUT_CALIB_REGULARIZER_PREFIX, ''), r.l1, r.l2)
          for r in model_config.regularizer_configs or []
          if r.name.startswith(_OUTPUT_CALIB_REGULARIZER_PREFIX)]


def _lattice_regularizers(model_config, feature_configs):
  """Returns lattice regularizers defined in the model and feature configs."""
  # dict from regularizer name to pair of per feature l1 and l2 amounts.
  regularizers_dict = {}
  n_dims = len(feature_configs)
  for index, feature_config in enumerate(feature_configs):
    for regularizer_config in feature_config.regularizer_configs or []:
      if not (
          regularizer_config.name.startswith(_INPUT_CALIB_REGULARIZER_PREFIX) or
          regularizer_config.name.startswith(_OUTPUT_CALIB_REGULARIZER_PREFIX)):
        if regularizer_config.name not in regularizers_dict:
          regularizers_dict[regularizer_config.name] = ([0.0] * n_dims,
                                                        [0.0] * n_dims)
        regularizers_dict[
            regularizer_config.name][0][index] += regularizer_config.l1
        regularizers_dict[
            regularizer_config.name][1][index] += regularizer_config.l2

  regularizers = [(k,) + v for k, v in regularizers_dict.items()]

  for regularizer_config in model_config.regularizer_configs or []:
    if not (
        regularizer_config.name.startswith(_INPUT_CALIB_REGULARIZER_PREFIX) or
        regularizer_config.name.startswith(_OUTPUT_CALIB_REGULARIZER_PREFIX)):
      regularizers.append((regularizer_config.name, regularizer_config.l1,
                           regularizer_config.l2))
  return regularizers


class LayerOutputRange(enum.Enum):
  """Enum to indicate the output range based on the input of the next layers."""
  MODEL_OUTPUT = 1
  INPUT_TO_LATTICE = 2
  INPUT_TO_FINAL_CALIBRATION = 3


def _output_range(layer_output_range, model_config, feature_config=None):
  """Returns min/max/init_min/init_max for a given output range."""
  if layer_output_range == LayerOutputRange.INPUT_TO_LATTICE:
    if feature_config is None:
      raise ValueError('Expecting feature config for lattice inputs.')
    output_init_min = output_min = 0.0
    output_init_max = output_max = feature_config.lattice_size - 1.0
  elif layer_output_range == LayerOutputRange.MODEL_OUTPUT:
    output_min = model_config.output_min
    output_max = model_config.output_max
    output_init_min = np.min(model_config.output_initialization)
    output_init_max = np.max(model_config.output_initialization)
  elif layer_output_range == LayerOutputRange.INPUT_TO_FINAL_CALIBRATION:
    output_init_min = output_min = 0.0
    output_init_max = output_max = 1.0
  else:
    raise ValueError('Unsupported layer output range.')
  return output_min, output_max, output_init_min, output_init_max


def build_input_layer(feature_configs, dtype):
  """Creates a mapping from feature name to `tf.keras.Input`.

  Args:
    feature_configs: A list of `tfl.configs.FeatureConfig` instances that
      specify configurations for each feature.
    dtype: dtype

  Returns:
    Mapping from feature name to `tf.keras.Input` for the inputs specified by
      `feature_configs`.
  """
  input_layer = {}
  for feature_config in feature_configs:
    layer_name = '{}_{}'.format(INPUT_LAYER_NAME, feature_config.name)
    if feature_config.num_buckets:
      input_layer[feature_config.name] = tf.keras.Input(
          shape=(1,), dtype=tf.int32, name=layer_name)
    else:
      input_layer[feature_config.name] = tf.keras.Input(
          shape=(1,), dtype=dtype, name=layer_name)
  return input_layer


def build_calibration_layers(calibration_input_layer, feature_configs,
                             model_config, layer_output_range, submodels,
                             separate_calibrators, dtype):
  """Creates a calibration layer for `submodels` as list of list of features.

  Args:
    calibration_input_layer: A mapping from feature name to `tf.keras.Input`.
    feature_configs: A list of `tfl.configs.FeatureConfig` instances that
      specify configurations for each feature.
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
    layer_output_range: A `tfl.premade_lib.LayerOutputRange` enum.
    submodels: A list of list of feature names.
    separate_calibrators: If features should be separately calibrated for each
      lattice in an ensemble.
    dtype: dtype

  Returns:
    A list of list of Tensors representing a calibration layer for `submodels`.
  """
  # Create a list of (feature_name, calibration_output_idx) pairs for each
  # submodel. When using shared calibration, all submodels will have
  # calibration_output_idx = 0.
  submodels_input_features = []
  calibration_last_index = collections.defaultdict(int)
  for submodel in submodels:
    submodel_input_features = []
    submodels_input_features.append(submodel_input_features)
    for feature_name in submodel:
      submodel_input_features.append(
          (feature_name, calibration_last_index[feature_name]))
      if separate_calibrators:
        calibration_last_index[feature_name] += 1

  calibration_output = {}
  for feature_config in feature_configs:
    feature_name = feature_config.name
    units = max(calibration_last_index[feature_name], 1)
    calibration_input = calibration_input_layer[feature_name]
    layer_name = '{}_{}'.format(CALIB_LAYER_NAME, feature_name)

    (output_min, output_max, output_init_min,
     output_init_max) = _output_range(layer_output_range, model_config,
                                      feature_config)

    if feature_config.num_buckets:
      kernel_initializer = tf.compat.v1.random_uniform_initializer(
          output_init_min, output_init_max)
      calibrated = (
          categorical_calibration_layer.CategoricalCalibration(
              num_buckets=feature_config.num_buckets,
              units=units,
              output_min=output_min,
              output_max=output_max,
              kernel_initializer=kernel_initializer,
              monotonicities=feature_config.monotonicity if isinstance(
                  feature_config.monotonicity, list) else None,
              default_input_value=feature_config.default_value,
              dtype=dtype,
              name=layer_name)(calibration_input))
    else:
      kernel_regularizer = _input_calibration_regularizers(
          model_config, feature_config)
      monotonicity = feature_config.monotonicity
      if (pwl_calibration_lib.canonicalize_monotonicity(monotonicity) == 0 and
          feature_config.pwl_calibration_always_monotonic):
        monotonicity = 1
      kernel_initializer = pwl_calibration_layer.UniformOutputInitializer(
          output_min=output_init_min,
          output_max=output_init_max,
          monotonicity=monotonicity)
      calibrated = (
          pwl_calibration_layer.PWLCalibration(
              units=units,
              input_keypoints=feature_config.pwl_calibration_input_keypoints,
              output_min=output_min,
              output_max=output_max,
              clamp_min=feature_config.pwl_calibration_clamp_min,
              clamp_max=feature_config.pwl_calibration_clamp_max,
              missing_input_value=feature_config.default_value,
              impute_missing=(feature_config.default_value is not None),
              kernel_initializer=kernel_initializer,
              kernel_regularizer=kernel_regularizer,
              monotonicity=monotonicity,
              convexity=feature_config.pwl_calibration_convexity,
              dtype=dtype,
              name=layer_name)(calibration_input))
    if units == 1:
      calibration_output[feature_name] = [calibrated]
    else:
      calibration_output[feature_name] = tf.split(calibrated, units, axis=1)

  # Create passthrough nodes for each submodel input so that we can recover
  # the model structure for plotting and analysis.
  # {CALIB_PASSTHROUGH_NAME}_{feature_name}_
  #   {calibration_output_idx}_{submodel_idx}_{submodel_input_idx}
  submodels_inputs = []
  for submodel_idx, submodel_input_features in enumerate(
      submodels_input_features):
    submodel_inputs = []
    submodels_inputs.append(submodel_inputs)
    for (submodel_input_idx,
         (feature_name,
          calibration_output_idx)) in enumerate(submodel_input_features):
      passthrough_name = '{}_{}_{}_{}_{}'.format(CALIB_PASSTHROUGH_NAME,
                                                 feature_name,
                                                 calibration_output_idx,
                                                 submodel_idx,
                                                 submodel_input_idx)
      submodel_inputs.append(
          tf.identity(
              calibration_output[feature_name][calibration_output_idx],
              name=passthrough_name))

  return submodels_inputs


def _monotonicities_from_feature_configs(feature_configs):
  """Returns list of monotonicities defined in the given feature_configs."""
  monotonicities = []
  for feature_config in feature_configs:
    if not feature_config.monotonicity:
      monotonicities.append(0)
    elif (isinstance(feature_config.monotonicity, six.string_types) and
          feature_config.monotonicity.lower() == 'none'):
      monotonicities.append(0)
    else:
      monotonicities.append(1)
  return monotonicities


def _dominance_constraints_from_feature_configs(feature_configs):
  """Returns list of dominance constraints in the given feature_configs."""
  feature_names = [feature_config.name for feature_config in feature_configs]
  monotonic_dominances = []
  for dominant_idx, dominant_feature_config in enumerate(feature_configs):
    for dominance_config in dominant_feature_config.dominates or []:
      if dominance_config.feature_name in feature_names:
        weak_idx = feature_names.index(dominance_config.feature_name)
        if dominance_config.dominance_type == 'monotonic':
          monotonic_dominances.append((dominant_idx, weak_idx))
        else:
          raise ValueError('Unrecognized dominance type: {}'.format(
              dominance_config.dominance_type))
  return monotonic_dominances


def build_linear_layer(linear_input, feature_configs, model_config,
                       weighted_average, submodel_index, dtype):
  """Creates a `tfl.layers.Linear` layer initialized to be an average.

  Args:
    linear_input: Input to the linear layer.
    feature_configs: A list of `tfl.configs.FeatureConfig` instances that
      specify configurations for each feature.
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
    weighted_average: If the linear coefficients should be positive and sum up
      to one.
    submodel_index: Corresponding index into submodels.
    dtype: dtype

  Returns:
    A `tfl.layers.Linear` instance.
  """
  layer_name = '{}_{}'.format(LINEAR_LAYER_NAME, submodel_index)

  linear_input = tf.keras.layers.Concatenate(axis=1)(linear_input)
  num_input_dims = len(feature_configs)
  kernel_initializer = tf.compat.v1.constant_initializer(
      [1.0 / num_input_dims] * num_input_dims)
  bias_initializer = tf.compat.v1.constant_initializer(0)

  if weighted_average:
    # Linear coefficients should be possitive and sum up to one.
    linear_monotonicities = [1] * num_input_dims
    normalization_order = 1
    use_bias = False
  else:
    linear_monotonicities = _monotonicities_from_feature_configs(
        feature_configs)
    normalization_order = None
    use_bias = model_config.use_bias

  monotonic_dominances = _dominance_constraints_from_feature_configs(
      feature_configs)

  return linear_layer.Linear(
      num_input_dims=num_input_dims,
      monotonicities=linear_monotonicities,
      monotonic_dominances=monotonic_dominances,
      use_bias=use_bias,
      normalization_order=normalization_order,
      kernel_initializer=kernel_initializer,
      bias_initializer=bias_initializer,
      dtype=dtype,
      name=layer_name)(
          linear_input)


def build_lattice_layer(lattice_input, feature_configs, model_config,
                        layer_output_range, submodel_index, is_inside_ensemble,
                        dtype):
  """Creates a `tfl.layers.Lattice` layer.

  Args:
    lattice_input: Input to the lattice layer.
    feature_configs: A list of `tfl.configs.FeatureConfig` instances that
      specify configurations for each feature.
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
    layer_output_range: A `tfl.premade_lib.LayerOutputRange` enum.
    submodel_index: Corresponding index into submodels.
    is_inside_ensemble: If this layer is inside an ensemble.
    dtype: dtype

  Returns:
    A `tfl.layers.Lattice` instance.
  """
  layer_name = '{}_{}'.format(LATTICE_LAYER_NAME, submodel_index)

  (output_min, output_max, output_init_min,
   output_init_max) = _output_range(layer_output_range, model_config)

  feature_names = [feature_config.name for feature_config in feature_configs]
  lattice_sizes = [
      feature_config.lattice_size for feature_config in feature_configs
  ]
  lattice_monotonicities = _monotonicities_from_feature_configs(feature_configs)
  lattice_unimodalities = [
      feature_config.unimodality for feature_config in feature_configs
  ]
  lattice_regularizers = _lattice_regularizers(model_config, feature_configs)

  # Construct trust constraints within this lattice.
  edgeworth_trusts = []
  trapezoid_trusts = []
  for conditional_idx, conditional_feature_config in enumerate(feature_configs):
    for trust_config in conditional_feature_config.reflects_trust_in or []:
      if trust_config.feature_name in feature_names:
        main_idx = feature_names.index(trust_config.feature_name)
        if trust_config.trust_type == 'edgeworth':
          edgeworth_trusts.append(
              (main_idx, conditional_idx, trust_config.direction))
        elif trust_config.trust_type == 'trapezoid':
          trapezoid_trusts.append(
              (main_idx, conditional_idx, trust_config.direction))
        else:
          raise ValueError('Unrecognized trust type: {}'.format(
              trust_config.trust_type))
      elif is_inside_ensemble and trust_config.trust_type == 'trapezoid':
        logging.warning(
            'A "main" feature (%s) for a trapezoid trust constraint is not '
            'present in a lattice that includes the "conditional" feature '
            '(%s). In an ensemble model, this can result in constraint '
            'violations. Consider manually setting the ensemble structure if '
            'this constraint needs to be satisfied.', trust_config.feature_name,
            conditional_feature_config.name)

  monotonic_dominances = _dominance_constraints_from_feature_configs(
      feature_configs)

  kernel_initializer = lattice_layer.LinearInitializer(
      lattice_sizes=lattice_sizes,
      monotonicities=lattice_monotonicities,
      unimodalities=lattice_unimodalities,
      output_min=output_init_min,
      output_max=output_init_max)
  return lattice_layer.Lattice(
      lattice_sizes=lattice_sizes,
      monotonicities=lattice_monotonicities,
      unimodalities=lattice_unimodalities,
      edgeworth_trusts=edgeworth_trusts,
      trapezoid_trusts=trapezoid_trusts,
      monotonic_dominances=monotonic_dominances,
      output_min=output_min,
      output_max=output_max,
      clip_inputs=False,
      kernel_regularizer=lattice_regularizers,
      kernel_initializer=kernel_initializer,
      dtype=dtype,
      name=layer_name)(
          lattice_input)


def build_output_calibration_layer(output_calibration_input, model_config,
                                   dtype):
  """Creates a monotonic output calibration layer with inputs range [0, 1].

  Args:
    output_calibration_input: Input to the output calibration layer.
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
    dtype: dtype

  Returns:
    A `tfl.layers.PWLCalibration` instance.
  """
  # kernel format: bias followed by diffs between consecutive keypoint outputs.
  kernel_init_values = np.ediff1d(
      model_config.output_initialization,
      to_begin=model_config.output_initialization[0])
  input_keypoints = np.linspace(0.0, 1.0, num=len(kernel_init_values))
  kernel_initializer = tf.compat.v1.constant_initializer(kernel_init_values)
  kernel_regularizer = _output_calibration_regularizers(model_config)
  return pwl_calibration_layer.PWLCalibration(
      input_keypoints=input_keypoints,
      output_min=model_config.output_min,
      output_max=model_config.output_max,
      kernel_initializer=kernel_initializer,
      kernel_regularizer=kernel_regularizer,
      monotonicity=1,
      dtype=dtype,
      name=OUTPUT_CALIB_LAYER_NAME)(
          output_calibration_input)


def set_categorical_monotonicities(feature_configs):
  """Maps categorical monotonicities to indices based on specified vocab list.

  Args:
    feature_configs: A list of `tfl.configs.FeatureConfig` objects.
  """
  if not isinstance(feature_configs, list) or any(
      not isinstance(fc, configs.FeatureConfig) for fc in feature_configs):
    raise ValueError(
        'feature_configs must be a list of tfl.configs.FeatureConfig objects: '
        '{}'.format(feature_configs))
  for feature_config in feature_configs:
    if feature_config.num_buckets and isinstance(feature_config.monotonicity,
                                                 list):
      # Make sure the vocabulary list exists. If not, assume user has already
      # properly set monotonicity as proper indices for this calibrator.
      if not feature_config.vocabulary_list:
        continue
      if not all(
          isinstance(m, tuple) and len(m) == 2
          for m in feature_config.monotonicity):
        raise ValueError(
            'Monotonicities should be a list of pairs (tuples): {}'.format(
                feature_config.monotonicity))
      indexed_monotonicities = []
      index_map = {
          category: index
          for (index, category) in enumerate(feature_config.vocabulary_list)
      }
      if feature_config.default_value is not None:
        index_map[feature_config.default_value] = feature_config.num_buckets - 1
      for left, right in feature_config.monotonicity:
        for category in [left, right]:
          if category not in index_map:
            raise ValueError(
                'Category `{}` not found in vocabulary list for feature `{}`'
                .format(category, feature_config.name))
        indexed_monotonicities.append((index_map[left], index_map[right]))

      feature_config.monotonicity = indexed_monotonicities


def set_random_lattice_ensemble(model_config):
  """Sets random lattice ensemble in the given model_config.

  Args:
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
  """
  if model_config.lattices != 'random':
    raise ValueError('model_config.lattices must be set to \'random\'.')
  if model_config.feature_configs is None:
    raise ValueError('Feature configs must be specified.')
  # Extract feature names
  feature_names = [
      feature_config.name for feature_config in model_config.feature_configs
  ]
  # Start by using each feature once.
  np.random.seed(model_config.random_seed)
  model_config.lattices = [[] for _ in range(model_config.num_lattices)]
  for feature_name in feature_names:
    non_full_indices = [
        i for (i, lattice) in enumerate(model_config.lattices)
        if len(lattice) < model_config.lattice_rank
    ]
    model_config.lattices[np.random.choice(non_full_indices)].append(
        feature_name)

  # Fill up lattices avoiding repeated features.
  for lattice in model_config.lattices:
    feature_names_not_in_lattice = [
        feature_name for feature_name in feature_names
        if feature_name not in lattice
    ]
    remaining_size = model_config.lattice_rank - len(lattice)
    lattice.extend(
        np.random.choice(
            feature_names_not_in_lattice, size=remaining_size, replace=False))


def verify_config(model_config):
  """Verifies that the model_config and feature_configs are fully specified.

  Args:
    model_config: Model configuration object describing model architecture.
      Should be one of the model configs in `tfl.configs`.
  """
  if isinstance(model_config, configs.CalibratedLatticeEnsembleConfig):
    if not isinstance(model_config.lattices, list):
      raise ValueError('Lattices are not fully specified for ensemble config.')
    for lattice in model_config.lattices:
      if (not np.iterable(lattice) or
          any(not isinstance(x, str) for x in lattice)):
        raise ValueError(
            'Lattices are not fully specified for ensemble config.')
  if model_config.feature_configs is None:
    raise ValueError('Feature configs must be fully specified.')
  for feature_config in model_config.feature_configs:
    if not feature_config.num_buckets:
      # Validate PWL Calibration configuration.
      if (not np.iterable(feature_config.pwl_calibration_input_keypoints) or
          any(not isinstance(x, (int, float))
              for x in feature_config.pwl_calibration_input_keypoints)):
        raise ValueError(
            'Input keypoints are invalid for feature {}: {}'.format(
                feature_config.name,
                feature_config.pwl_calibration_input_keypoints))
    elif feature_config.monotonicity and feature_config.monotonicity != 'none':
      # Validate Categorical Calibration configuration.
      if not np.iterable(feature_config.monotonicity):
        raise ValueError('Monotonicity is not a list for feature {}: {}'.format(
            feature_config.name, feature_config.monotonicity))
      for i, t in enumerate(feature_config.monotonicity):
        if not np.iterable(t):
          raise ValueError(
              'Element {} is not a tuple for feature {} monotonicty: {}'.format(
                  i, feature_config.name, t))
        for j, val in enumerate(t):
          if not isinstance(val, int):
            raise ValueError(
                'Element {} for tuple {} for feature {} monotonicity is not an '
                'index: {}'.format(j, i, feature_config.name, val))
          if val < 0 or val >= feature_config.num_buckets:
            raise ValueError(
                'Element {} for tuple {} for feature {} monotonicity is an '
                'invalid index not in range [0, num_buckets - 1]: {}'.format(
                    j, i, feature_config.name, val))
  if (not np.iterable(model_config.output_initialization) or
      any(not isinstance(x, (int, float))
          for x in model_config.output_initialization)):
    raise ValueError('Output initilization is invalid: {}'.format(
        model_config.output_initialization))
