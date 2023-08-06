# Copyright 2020 Nod Labs
# authors: dstamoulis, ruizhoud
#
# Code extends codebase from the "MNasNet on TPU" GitHub repo:
# https://github.com/tensorflow/tpu/tree/master/models/official/mnasnet
#
# This project incorporates material from the project listed above, and it
# is accessible under their original license terms (Apache License 2.0)
# ==============================================================================
"""Contains the searchable superkernel definition based on the
   Single-Path search space formulation.

[1] D. Stamoulis et al., Single-Path NAS: Designing Hardware-Efficient
    ConvNets in less than 4 Hours. arXiv:(TBD)
"""


import tensorflow as tf
import numpy as np
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.engine.base_layer import InputSpec


def Indicator(x):
  #TypeError: Value passed to parameter 'x' has DataType bool not in list of allowed values:
  #           bfloat16, float16, float32, float64, uint8, int8, uint16, int16,
  #           int32, int64, complex64, complex128
  #return tf.stop_gradient((x>=0) - tf.sigmoid(x)) + tf.sigmoid(x)
  return tf.stop_gradient(tf.to_float(x>=0) - tf.sigmoid(x)) + tf.sigmoid(x)


def sample_gumbel(shape, eps=1e-20):
  U = tf.random_uniform(shape, minval=0, maxval=1)
  return -tf.log(-tf.log(U + eps) + eps)


class DepthwiseConv2DMasked(tf.keras.layers.DepthwiseConv2D):
  def __init__(self,
               kernel_size,
               strides,
               depthwise_initializer,
               padding,
               use_bias,  
               runtimes=None,
               dropout_rate=None,
               **kwargs):

    super(DepthwiseConv2DMasked, self).__init__(
            kernel_size=kernel_size,
            strides=strides,
            depthwise_initializer=depthwise_initializer,
            padding=padding,
            use_bias=use_bias,
            **kwargs)

    self.runtimes = runtimes
    self.dropout_rate = tf.stop_gradient(dropout_rate)

    if kernel_size[0] != 5: # normal Depthwise type
      self.custom = False
    else:
      self.custom = True
      if self.runtimes is not None:
        self.R50c = K.cast_to_floatx(self.runtimes[2]) # 50% of the 5x5
        self.R100c = K.cast_to_floatx(self.runtimes[3]) # 100% of the 5x5
        self.R5x5 = K.cast_to_floatx(self.runtimes[3]) # 5x5 for 100%
        self.R3x3 = K.cast_to_floatx(self.runtimes[1]) # 3x3 for 100%
      else:
        self.R50c = K.cast_to_floatx(0.0)
        self.R100c = K.cast_to_floatx(0.0)
        self.R5x5 = K.cast_to_floatx(0.0)
        self.R3x3 = K.cast_to_floatx(0.0)


  def build(self, input_shape):

    # NOTE: necessary for defining a Keras layer!
    # https://keras.io/layers/writing-your-own-keras-layers/
    # also need to build the superclass so that layer is populated w/ weights!
    super(DepthwiseConv2DMasked, self).build(input_shape)

    runtime = 0.0

    if not self.custom:
      # back to typical DepthwiseConv2D
      self.depthwise_kernel_masked = self.depthwise_kernel
      self.runtime_reg = runtime

    else:

      # our implementation is channels_last
      assert self.data_format == 'channels_last'
      assert len(input_shape) == 4

      kernel_shape = self.depthwise_kernel.shape
      assert kernel_shape[-1] == 1 # I don't think we handle depth mult
      assert kernel_shape[0] == 5 # you cannot mask out if it is 3x3 already!
      assert kernel_shape[1] == 5 # you cannot mask out if it is 3x3 already!

      # Thresholds
      self.t5x5 = self.add_weight(shape=(1,),initializer='zeros',name="t5x5")
      self.t50c = self.add_weight(shape=(1,),initializer='zeros',name="t50c")
      self.t100c = self.add_weight(shape=(1,),initializer='zeros',name="t100c")

      # create masks based on kernel_shape
      center_3x3 = np.zeros(kernel_shape)
      center_3x3[1:4,1:4,:,:] = 1.0 # center 3x3
      self.mask3x3 = tf.convert_to_tensor(center_3x3,
                        dtype=self.t5x5.dtype)

      center_5x5 = np.ones(kernel_shape) - center_3x3 # 5x5 - center 3x3
      self.mask5x5 = tf.convert_to_tensor(center_5x5,
                        dtype=self.t5x5.dtype)

      num_channels = int(kernel_shape[2])
      c50  = int(round(1.0*num_channels/2.0)) #  50 %
      c100 = int(round(2.0*num_channels/2.0)) # 100 %

      mask_50c = np.zeros(kernel_shape)
      mask_50c[:,:,0:c50,:] = 1.0 # from 0% to 50% channels
      self.mask50c = tf.convert_to_tensor(mask_50c,
                        dtype=self.t5x5.dtype)

      mask_100c = np.zeros(kernel_shape)
      mask_100c[:,:,c50:c100,:] = 1.0 # from 50% to 100% channels
      self.mask100c = tf.convert_to_tensor(mask_100c,
                        dtype=self.t5x5.dtype)

      #--> make indicator results "accessible" as separate vars
      kernel_3x3 = self.depthwise_kernel * self.mask3x3
      kernel_5x5 = self.depthwise_kernel * self.mask5x5
      self.norm5x5 = tf.norm(kernel_5x5)

      x5x5 = self.norm5x5 - self.t5x5
      if self.dropout_rate is not None: # zero-out with drop_prob_
        self.d5x5 = tf.nn.dropout(Indicator(x5x5), self.dropout_rate)
      else:
        self.d5x5 = Indicator(x5x5)


      depthwise_kernel_masked_outside = \
            kernel_3x3 + kernel_5x5 * self.d5x5

      kernel_50c = depthwise_kernel_masked_outside * self.mask50c
      kernel_100c = depthwise_kernel_masked_outside * self.mask100c
      self.norm50c = tf.norm(kernel_50c)
      self.norm100c = tf.norm(kernel_100c)


      x100c = self.norm100c - self.t100c
      if self.dropout_rate is not None: # noise to add
        self.d100c = tf.nn.dropout(Indicator(x100c), self.dropout_rate)
      else:
        self.d100c = Indicator(x100c)


      if self.strides[0] == 1 and len(self.runtimes) == 9:
        x50c = self.norm50c - self.t50c
        if self.dropout_rate is not None: # noise to add
          self.d50c = tf.nn.dropout(Indicator(x50c), self.dropout_rate)
        else:
          self.d50c = Indicator(x50c)
      else: # you cannot drop all layers!
        self.d50c = 1.0

      self.depthwise_kernel_masked = \
            self.d50c * (kernel_50c + self.d100c *kernel_100c)

      # runtime term
      if self.runtimes is not None:
        ratio = self.R3x3 / self.R5x5
        runtime_channels = self.d50c * (self.R50c + self.d100c * (self.R100c-self.R50c)) 
        runtime = runtime_channels * ratio + runtime_channels * (1-ratio) * self.d5x5

      self.runtime_reg = runtime


  def call(self, inputs, total_runtime, training=None):
    outputs = K.depthwise_conv2d(
        inputs,
        self.depthwise_kernel_masked,
        strides=self.strides,
        padding=self.padding,
        dilation_rate=self.dilation_rate,
        data_format=self.data_format)

    if self.use_bias:
      outputs = K.bias_add(
              outputs,
              self.bias,
              data_format=self.data_format)

    total_runtime = total_runtime + self.runtime_reg

    if self.activation is not None:
      return self.activation(outputs), total_runtime

    return outputs, total_runtime


class SEMasked(tf.keras.layers.Conv2D):
  def __init__(self,
               reduced_filters,
               kernel_size,
               strides,
               kernel_initializer,
               padding,
               use_bias,
               runtimes=None,
               dropout_rate=None,
               prev_block=None,
               **kwargs):

    super(SEMasked, self).__init__(
            filters=reduced_filters,
            kernel_size=kernel_size,
            strides=strides,
            kernel_initializer=kernel_initializer,
            padding=padding,
            use_bias=use_bias,
            **kwargs)

    self.runtimes = runtimes
    self.dropout_rate = tf.stop_gradient(dropout_rate)
    self.prev = prev_block

    if self.runtimes is not None:
      self.R330 = tf.convert_to_tensor(self.runtimes[0], dtype=tf.float32)
      self.R360 = tf.convert_to_tensor(self.runtimes[1], dtype=tf.float32)
      self.R530 = tf.convert_to_tensor(self.runtimes[2], dtype=tf.float32)
      self.R560 = tf.convert_to_tensor(self.runtimes[3], dtype=tf.float32)
      self.R33025 = tf.convert_to_tensor(self.runtimes[4], dtype=tf.float32)
      self.R36025 = tf.convert_to_tensor(self.runtimes[5], dtype=tf.float32)
      self.R53025 = tf.convert_to_tensor(self.runtimes[6], dtype=tf.float32)
      self.R56025 = tf.convert_to_tensor(self.runtimes[7], dtype=tf.float32)
      self.S33025 = self.R33025 / self.R330
      self.S36025 = self.R36025 / self.R360
      self.S53025 = self.R53025 / self.R530
      self.S56025 = self.R56025 / self.R560

    else:
      self.S33025 = tf.convert_to_tensor(0.0, dtype=tf.float32)
      self.S36025 = tf.convert_to_tensor(0.0, dtype=tf.float32)
      self.S53025 = tf.convert_to_tensor(0.0, dtype=tf.float32)
      self.S56025 = tf.convert_to_tensor(0.0, dtype=tf.float32)

  def build(self, input_shape):

    # NOTE: necessary for defining a Keras layer!
    # https://keras.io/layers/writing-your-own-keras-layers/
    # also need to build the superclass so that layer is populated w/ weights!
    super(SEMasked, self).build(input_shape)

    runtime = 0.0

    # New thresholds
    self.t25 = self.add_weight(shape=(1,),initializer='zeros',name="t025")
    self.t50 = self.add_weight(shape=(1,),initializer='zeros',name="t050")

    # create masks based on kernel_shape
    kernel_shape = self.kernel.shape  # [kernel_size + (in_ch, out_ch)]
    num_channels = int(kernel_shape[3])  # This reduces the output channels to 0.5/0.25
    se25 = int(round(1.0*num_channels/2.0)) # se=0.25
    se50 = int(round(2.0*num_channels/2.0)) # se=0.50

    mask_se25 = np.zeros(kernel_shape)
    mask_se25[:,:,:,0:se25] = 1.0   # from se 0 to 0.25
    self.mask25 = tf.convert_to_tensor(mask_se25,
                      dtype=self.prev.t5x5.dtype)

    mask_se50 = np.zeros(kernel_shape)
    mask_se50[:,:,:,se25:se50] = 1.0 # from se 0.25 to 0.5
    self.mask50 = tf.convert_to_tensor(mask_se50,
                      dtype=self.prev.t5x5.dtype)

    #--> make indicator results "accessible" as separate vars
    kernel_se25 = self.kernel * self.mask25
    kernel_se50 = self.kernel * self.mask50
    self.norm25= tf.norm(kernel_se25)
    self.norm50 = tf.norm(kernel_se50)

    x50 = self.norm50 - self.t50
    if self.dropout_rate is not None: # noise to add
      self.d50se = tf.nn.dropout(Indicator(x50), self.dropout_rate)
    else:
      self.d50se = Indicator(x50)

    x25 = self.norm25 - self.t25
    if self.dropout_rate is not None: # noise to add
      self.d25se = tf.nn.dropout(Indicator(x25), self.dropout_rate)
    else:
      self.d25se = Indicator(x25)

    self.kernel_masked = \
          self.d25se * (kernel_se25 + self.d50se * kernel_se50)

    self.s_k6025 = self.prev.d5x5 * self.S56025 + (1-self.prev.d5x5) * self.S36025
    self.s_k3025 = self.prev.d5x5 * self.S53025 + (1-self.prev.d5x5) * self.S33025
    # runtime term
    if self.runtimes is not None:
      runtime = (1-self.d25se) * self.prev.runtime_reg + \
                self.d25se * (self.prev.d100c * self.s_k6025 + (1-self.prev.d100c) * self.s_k3025) * self.prev.runtime_reg

    self.runtime_se = runtime

  def call(self, inputs, total_runtime, training=None):
    outputs = K.conv2d(
        inputs,
        self.kernel_masked,
        strides=self.strides,
        padding=self.padding)

    if self.use_bias:
      outputs = K.bias_add(
        outputs,
        self.bias,
      )

    total_runtime = total_runtime + self.runtime_se

    return outputs, total_runtime

