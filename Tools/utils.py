class AverageMeter(object):
    """Class to keep track of the average value of a metric over time.

    This implementation is adapted from the PyTorch examples repository:
    https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """

    def __init__(self):
        """Initialize all the necessary attributes for the AverageMeter instance."""
        self.val = 0  # Stores the most recent value
        self.avg = 0  # Stores the running average of the values
        self.sum = 0  # Stores the cumulative sum of all values
        self.count = 0  # Stores the count of values added

    def __repr__(self):
        """String representation of the running average.

        Returns the running average formatted in scientific notation with two decimal places.
        """
        return f'{self.avg:.2e}'

    def update(self, val, n=1):
        """Update the meter with a new value.

        Args:
            val (float): The new value to add.
            n (int, optional): The weight of the new value (default is 1).
        """
        self.val = val  # Update the most recent value
        self.sum += val * n  # Update the cumulative sum with the weighted new value
        self.count += n  # Update the count with the weight
        self.avg = self.sum / self.count  # Recalculate the running average


class dotdict(dict):
    """Dictionary subclass that allows for dot notation access to dictionary attributes.

    This means you can access dictionary keys as if they were attributes.
    """

    def __getattr__(self, name):
        """Override the default attribute access method.

        Args:
            name (str): The name of the attribute to access.

        Returns:
            The value associated with the key `name`.

        Raises:
            AttributeError: If the key `name` does not exist in the dictionary.
        """
        return self[name]
