import sys
import time


class ProgressBar:
    """
    Instantiate a progress bar. It assumes values from 0 to end_value - 1.

    Example code:
    >>> bar = ProgressBar(end_value=100, text="Iteration")
    >>> for i in range(0, 100):
    >>>    time.sleep(1)
    >>>    bar.update(i)
    """
    def __init__(self, end_value=100, text=None, bar_length=20):
        """
        Initialize the progress bar.

        :param end_value:       Maximum number of iterations
        :param text:        Text to be displayed before the bar
        :param bar_length:  Number of hashes to display
        """
        self.end_value = end_value
        self.current = 0
        self.bar_length = bar_length
        if text:
            self.text = text
        else:
            self.text = "Progress"

        # Start displaying the bar
        sys.stdout.write("\r{0}: [{1}] {2}%".format(self.text,
                                                    ' ' * self.bar_length,
                                                    self.current))
        sys.stdout.flush()

    def update(self, new_val):
        """
        Update the bar with new_val.

        :param new_val: New current value
        """
        self.current = new_val + 1
        if self.current <= self.end_value:
            percent = float(self.current) / self.end_value
            hashes = '#' * int(round(percent * self.bar_length))
            spaces = ' ' * (self.bar_length - len(hashes))
            sys.stdout.write("\r{0}: [{1}] {2}%".format(self.text,
                                                        hashes + spaces,
                                                        int(round(percent * 100))))
            sys.stdout.flush()
            if self.current == self.end_value:
                sys.stdout.write("\n")


def progress_bar_test(end_value, text, bar_length=20):
    bar = ProgressBar(end_value=end_value, text=text, bar_length=bar_length)
    for i in range(0, end_value):
        time.sleep(1)
        bar.update(i)


if __name__ == '__main__':
    progress_bar_test(5, 'Iterations')