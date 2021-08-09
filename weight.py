import keras
import pydot
from keras.utils.vis_utils import plot_model

model = keras.models.load_model('iaps_real4')
model.summary()

plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

