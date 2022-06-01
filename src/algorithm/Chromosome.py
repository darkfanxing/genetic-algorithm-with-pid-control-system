class Chromosome():
    """One of the population of GA

    Attributes:
        kp (float): The P value of the PID control system
        ki (float): The I value of the PID control system
        kd (float): The D value of the PID control system
        eta (float): The parameter of the control system's output function

    """

    def __init__(self, kp: float, ki: float, kd: float, eta: float) -> None:
        """Initialize the chromosome's attributes

        Args:
            kp (float): _description_
            ki (float): _description_
            kd (float): _description_
            eta (float): _description_
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.eta = eta
