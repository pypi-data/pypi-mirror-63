from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import Dense, Flatten
import tensorflow.keras.models


class Predictor:
    learning_rate = 0.01

    decay_lr = 0

    loss_fn = 'categorical_crossentropy'

    def __init__(self, output_activation, ft_range, lr=0.001, loss = 'categorical_crossentropy'):
        self.model = None
        self.output_activation = output_activation
        self.ft_range = ft_range
        self.learning_rate = lr
        self.loss_fn = loss

    def predict(self, input):
        return self.model.predict(input)

    def classify(self, input):
        return self.model.predict_proba(input), self.model.predict_classes(input)

    def load_model(self, path):
        self.model = tensorflow.keras.models.load_model(path)
        self.model._make_predict_function()

    def get_model(self, shape, num_classes, inner_activation='relu'):
        model = Sequential()
        # Input arrays of shape (*, layers[1])
        # Output = arrays of shape (*, layers[1] * 16)
        model.add(Dense(units=int(64), input_shape=shape, activation=inner_activation))
        model.add(Dense(units=int(64), activation=inner_activation))
        # model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(units=num_classes, activation=self.output_activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        # opt = optimizers.RMSprop(lr=0.001)
        model.compile(optimizer="adam", loss=self.loss_fn, metrics=['acc'])
        model.summary()
        self.model = model
        return model

    def get_model_configurable(self, shape, num_classes, inner_activation='relu', num_dense_layers=1, num_units_per_layer=[64], loss='categorical_crossentropy', metrics=['acc','categorical_accuracy']):
        model = Sequential()
        # Input arrays of shape (*, layers[1])
        # Output = arrays of shape (*, layers[1] * 16)
        model.add(Dense(units=int(num_units_per_layer[0]), input_shape=shape, activation=inner_activation))
        for i in range(1,num_dense_layers):
            model.add(Dense(units=int(num_units_per_layer[i]), activation=inner_activation))
        
        model.add(Flatten())
        model.add(Dense(units=num_classes, activation=self.output_activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        # opt = optimizers.RMSprop(lr=self.learning_rate)
        model.compile(loss=loss, metrics=metrics)
        model.summary()
        self.model = model
        return model
