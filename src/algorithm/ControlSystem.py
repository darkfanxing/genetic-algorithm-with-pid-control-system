from typing import List, Dict, Union
from scipy.signal import square
from numpy import array, linspace, pi, sin
from .Chromosome import Chromosome


class ControlSystem():
    """The PID Control System.

    Attributes:
        eta_boundary (float): The boundary of eta.
        period (int): The number of cycles of te signal.
        slicing_per_period (int): The number of slicing in a period.
        u_boundary (List[float]): The boundary of u.
        y (List[float]): The control system's output collection.
        y_now (float): The control system's output at the current time.
        y_fore (float): The control system's output at the pervious time.
        u_now (float): The function u's output at the current time.
        u_fore (float): The function u's output at the pervious time.
        error_now (float): The error of the control system's input and
            output at the current time.
        error_fore (float): The error of the control system's input and
            output at the previous time.
        error_sum (float): The error sum so far.
        kp (float): The P value of PID used by the control system.
        ki (float): The I value of PID used by the control system.
        kd (float): The D value of PID used by the control system.
    """

    def __init__(
        self,
        chromosome: Chromosome,
        config: Dict[str, Union[float, List[float]]],
    ) -> None:
        self.y_now: float = config["initial-y-now"]
        self.period: int = config["period"]
        self.slicing_per_period: int = config["slicing-per-period"]
        self.u_boundary: List[float] = config["u-boundary"]

        self.kp = chromosome.kp
        self.ki = chromosome.ki
        self.kd = chromosome.kd
        self.eta = chromosome.eta

        self.__init_input_signal()
        self.__init_system_parameter()

    def __init_input_signal(self) -> None:
        """Initialize the input (square) signal of the control system.

        the input signal's parameters can modify @ `../../genetic-algorithm-config.yaml`.

        """
        self.input_signal: List[float] = square(
            2 * pi * self.period * linspace(
                start=0,
                stop=1,
                num=self.period * self.slicing_per_period,
            ))

    def __init_system_parameter(self) -> None:
        """initialize the parameters of the control system
        """
        self.y_fore: float = 0
        self.y: List[float] = [self.y_now]

        self.error_now: float = self.input_signal[0] - self.y_now
        self.error_fore: float = 0
        self.error_sum: float = 0
        self.errors: List[float] = [self.error_now]

        self.u_now: float = 0
        self.__update_u_now()
        self.u_fore: List[float] = 0

    def __update_u_now(self) -> None:
        """Update function u's output at the current time

        The boundary can modify @ `../../genetic-algorithm-config.yaml`.

        """
        u_next = \
            self.kp * self.error_now \
            + self.ki * self.error_sum \
            + self.kd * (self.error_now - self.error_fore)

        if u_next < self.u_boundary[0]:
            u_next = self.u_boundary[0]
        elif u_next > self.u_boundary[1]:
            u_next = self.u_boundary[1]

        self.u_now = u_next

    def __update_y_now(self) -> None:
        """Update control system's (function y's) output at the current time

        You can see the control system @ `../../README.md`

        """
        self.y_now = \
            2.6 * self.y_now \
            - 1.2 * self.y_fore \
            + self.u_now \
            + 1.2 * self.u_fore \
            + self.eta * self.y_now * sin(self.u_now + self.u_fore + self.y_now + self.y_fore)

    def run(self) -> None:
        """Run the control system with PID and eta value

        It will update the parameters of the control system at every tick

        """
        for index in range(1, self.period * self.slicing_per_period, 1):
            self.__update_y_now()
            self.error_now = self.input_signal[index] - self.y_now
            self.__update_u_now()

            self.error_sum += self.error_now
            self.errors.append(self.error_now)
            self.error_fore = self.error_now

            self.y.append(self.y_now)
            self.y_fore = self.y_now

            self.u_fore = self.u_now

    def get_fitness_value(self):
        """Calculate the fitness value of this control system

        Returns:
            float: The sum of errors at each time

        """

        return sum(abs(array(self.errors)))
