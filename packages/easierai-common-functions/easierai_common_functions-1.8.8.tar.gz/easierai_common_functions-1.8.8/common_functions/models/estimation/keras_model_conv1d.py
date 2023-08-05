from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D
import tensorflow.keras.models


class Predictor:
    learning_rate = 0.01

    decay_lr = 0

    loss_fn = 'mse'

    def __init__(self, output_activation, ft_range, lr=0.001):
        self.model = None
        self.output_activation = output_activation
        self.ft_range = ft_range
        self.learning_rate = lr

    def predict(self, input):
        return self.model.predict(input)

    def classify(self, input):
        return self.model.predict_proba(input), self.model.predict_classes(input)

    def load_model(self, path):
        self.model = tensorflow.keras.models.load_model(path)
        self.model._make_predict_function()

    def get_model(self, shape, num_forecasts, inner_activation='relu'):
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=2, activation=inner_activation, input_shape=shape))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        model.add(Dense(units=num_forecasts, activation=self.output_activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        opt = optimizers.RMSprop(lr=0.001)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mae'])
        model.summary()
        self.model = model
        return model

    def get_model_configurable(self, shape, num_forecasts, inner_activation='relu', num_dense_layers=1, num_units_per_layer=[64], loss='mae', metrics=['mse']):
        model = Sequential()
        # Input arrays of shape (*, layers[1])
        # Output = arrays of shape (*, layers[1] * 16)
        model.add(Conv1D(filters=64, kernel_size=2, input_shape=shape, activation=inner_activation))
        for i in range(1,num_dense_layers):
            model.add(Conv1D(filters=num_units_per_layer[i], kernel_size=2, activation=inner_activation))
        
        model.add(Flatten())
        model.add(Dense(units=num_forecasts, activation=self.output_activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        opt = optimizers.RMSprop(lr=self.learning_rate)
        model.compile(optimizer=opt, loss=loss, metrics=metrics)
        model.summary()
        self.model = model
        return model
