# -*- coding: utf-8 -*-
"""
module reduce_lr_on_plateau.py
--------------------------------
Reduce Learning rate on plateau training callback.
"""
import numpy as np
import tensorflow as tf
from . import ModeEnum
from . import on_batch_begin, on_batch_end, on_epoch_begin, on_epoch_end, on_train_begin, \
    on_train_end, on_validate_begin, on_validate_end


class ReduceLROnPlateau(object):
    """Reduce learning rate when a metric has stopped improving.

    Models often benefit from reducing the learning rate by a factor
    of 2-10 once learning stagnates. This callback monitors a
    quantity and if no improvement is seen for a 'patience' number
    of epochs, the learning rate is reduced.

    Example:

    ```python
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                                patience=5, min_lr=0.001)
    model.fit(X_train, Y_train, callbacks=[reduce_lr])
    ```
    """

    def __init__(
            self,
            monitor='val_loss',
            factor=0.1,
            patience=10,
            verbose=1,
            mode: ModeEnum=ModeEnum.MIN,
            min_delta=1e-4,
            cooldown=0,
            min_lr=0,
            **kwargs
    ):
        """
        ReduceLROnPlateau callback initialization.

        :param monitor: quantity to be monitored.

        :param factor: factor by which the learning rate will
            be reduced. new_lr = lr * factor

        :param patience: number of epochs with no improvement
            after which learning rate will be reduced.
        verbose: int. 0: quiet, 1: update messages.

        :param mode: one of {auto, min, max}. In `min` mode,
            lr will be reduced when the quantity
            monitored has stopped decreasing; in `max`
            mode it will be reduced when the quantity
            monitored has stopped increasing; in `auto`
            mode, the direction is automatically inferred
            from the name of the monitored quantity.

        :param min_delta: threshold for measuring the new optimum,
            to only focus on significant changes.

        :param cooldown: number of epochs to wait before resuming
            normal operation after lr has been reduced.

        :param min_lr: lower bound on the learning rate.
        """

        self.monitor = monitor
        if factor >= 1.0:
            raise ValueError('ReduceLROnPlateau ' 'does not support a factor >= 1.0.')
        self.factor = factor
        self.min_lr = min_lr
        self.min_delta = min_delta
        self.patience = patience
        self.verbose = verbose
        self.cooldown = cooldown
        self.cooldown_counter = 0  # Cooldown counter.
        self.wait = 0
        self.best = 0
        self.mode = mode
        self.monitor_op = None
        self._reset()

        on_train_begin.connect(self.on_train_begin, weak=False)
        on_epoch_end.connect(self.on_epoch_end, weak=False)

    def _reset(self):
        """Resets wait counter and cooldown counter.
        """
        if self.mode is ModeEnum.MIN:
            self.monitor_op = lambda a, b: np.less(a, b - self.min_delta)
            self.best = np.Inf
        else:
            self.monitor_op = lambda a, b: np.greater(a, b + self.min_delta)
            self.best = -np.Inf

        self.cooldown_counter = 0
        self.wait = 0

    def on_train_begin(self, sender):
        self._reset()

    def on_epoch_end(self, sender):
        optimizer = sender.optimizer
        lr, lr_t = self._get_current_lr(optimizer)
        sender.current_state["learning_rate"] = lr

        current = sender.current_state.get(self.monitor)
        epoch = sender.current_state["current_epoch"]
        if current is None:
            print(
                'Reduce LR on plateau conditioned on metric `%s` '
                'which is not available. Available metrics are: %s',
                self.monitor, ','.join(list(sender.current_state.keys()))
            )

        else:
            if self.in_cooldown():
                self.cooldown_counter -= 1
                self.wait = 0

            if self.monitor_op(current, self.best):
                self.best = current
                self.wait = 0
            elif not self.in_cooldown():
                self.wait += 1
                if self.wait >= self.patience:
                    old_lr = float(lr)
                    if old_lr > self.min_lr:
                        new_lr = old_lr * self.factor
                        new_lr = max(new_lr, self.min_lr)
                        self._set_lr(sender, lr_t, new_lr)
                        if self.verbose > 0:
                            print('\nEpoch %05d: ReduceLROnPlateau reducing learning '
                                  'rate to %s. from %s' % (epoch + 1, new_lr, old_lr))
                        self.cooldown_counter = self.cooldown
                        self.wait = 0

    def in_cooldown(self):
        return self.cooldown_counter > 0

    def _set_lr(self, sender, lr_t, new_value):
        assign_op = tf.assign(lr_t, new_value)
        sess = tf.get_default_session()
        sess.run(assign_op)

    def _get_current_lr(self, optimizer):
        """
        Returns the current learning rate and learning_rate tensor.
        :param optimizer: tensorflow optimizer.
        """
        if hasattr(optimizer, "_lr_t"):
            # lr_t = optimizer._lr_t
            lr_t = optimizer._lr
        elif hasattr(optimizer, "_learning_rate_tensor"):
            # lr_t = optimizer._learning_rate_tensor
            lr_t = optimizer._learning_rate
        else:
            raise AttributeError("Could not fint learning rate attribute on the optimizer.")
        sess = tf.get_default_session()
        lr, = sess.run(
            fetches=[lr_t],
        )

        return lr, lr_t
