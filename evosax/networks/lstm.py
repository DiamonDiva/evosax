from flax import linen as nn
import jax
import chex
from typing import Tuple
from .shared import (
    identity_out,
    tanh_out,
    categorical_out,
    gaussian_out,
    default_bias_init,
)


class LSTM(nn.Module):
    """Simple LSTM Wrapper with flexible output head."""

    num_hidden_units: int = 32
    num_output_units: int = 1
    output_activation: str = "identity"
    model_name: str = "LSTM"

    @nn.compact
    def __call__(
        self, x: chex.Array, carry: chex.ArrayTree, rng: chex.PRNGKey
    ) -> Tuple[Tuple[chex.ArrayTree, chex.ArrayTree], chex.Array]:
        lstm_state, x = nn.LSTMCell(bias_init=default_bias_init())(carry, x)
        if self.output_activation == "identity":
            x = identity_out(x, self.num_output_units)
        elif self.output_activation == "tanh":
            x = tanh_out(x, self.num_output_units)
        elif self.output_activation == "categorical":
            x = categorical_out(rng, x, self.num_output_units)
        elif self.output_activation == "gaussian":
            x = gaussian_out(rng, x, self.num_output_units)
        return lstm_state, x

    def initialize_carry(self) -> Tuple[chex.ArrayTree, chex.ArrayTree]:
        """Initialize hidden state of LSTM."""
        return nn.LSTMCell.initialize_carry(
            jax.random.PRNGKey(0), (), self.num_hidden_units
        )
