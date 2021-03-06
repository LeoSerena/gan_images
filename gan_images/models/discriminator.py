import tensorflow as tf
from tensorflow import keras as K

def init_conv2D(image_shape, D, filter_dim, strides, num_channels):
    return K.layers.Conv2D(
        D,
        filter_dim,
        strides=strides,
        padding='same',
        input_shape=[image_shape[0], image_shape[1], num_channels]
    )

def init_discriminator(
    image_shape = (128, 128),
    D = 256,
    filter_dim = (5,5),
    num_channels = 3
):
    # It is desirable that the discriminator performs better than the generator. Thus it should be larger and be more deep with more layers.
    model = K.Sequential()

    model.add(init_conv2D(image_shape = image_shape, D = int(D/4), filter_dim = filter_dim, strides = (2,2), num_channels = num_channels))
    model.add(K.layers.LeakyReLU())
    model.add(K.layers.Dropout(0.3))

    model.add(init_conv2D(image_shape = image_shape, D = int(D/2), filter_dim = filter_dim, strides = (2,2), num_channels = num_channels))
    model.add(K.layers.LeakyReLU())
    model.add(K.layers.Dropout(0.3))

    model.add(K.layers.Flatten())
    model.add(K.layers.Dense(1))

    return model

def d_loss(real, fake, real_label = 0.9):
    # The from_logits = True indicates the values are in [-inf, inf]
    cross_entropy = K.losses.BinaryCrossentropy(from_logits = True)

    # real samples have label 1 
    # Note that one proposed trick is to replace 1 with something close such as 0.9 because the model is sometimes overconfident
    # They say to not do it for the fake samples
    real_loss = cross_entropy(tf.ones_like(real) * real_label, real)
    # fake samples have label 0
    fake_loss = cross_entropy(tf.zeros_like(fake), fake)

    total_loss = real_loss + fake_loss

    return total_loss