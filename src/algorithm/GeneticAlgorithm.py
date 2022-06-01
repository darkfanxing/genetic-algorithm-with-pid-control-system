from typing import List, Dict, Union
from numpy.random import randint, random, uniform
from .Chromosome import Chromosome
from .ControlSystem import ControlSystem


class GeneticAlgorithm():
    """The genetic algorithm (GA) with a control system.

    Attributes:
        pid_boundary (List[float]): The boundary of PID controller, and its value is
            [{ minimum_boundary }, { maximum_boundary }].
        eta_boundary (List[float]): The boundary of eta that the parameter of the control
            system output, and its value is [{ minimum_boundary }, { maximum_boundary }].
        population_number (int): The number of population in GA.
        mutation_probability (float): The mutation probability of chromosomes in GA.
        crossover_rate (float): The cross_over rate of chromosomes in GA.
        control_system_config (Dict[str, Union[float, List[float]]]): The config of the
            control system, read more @ `../../genetic-algorithm-config.yaml`.
    """

    def __init__(
        self,
        config: Dict[str, Union[float, List[float]]],
    ) -> None:
        """Initialization of GA.

        Args:
            config (Dict[str, Union[float, List[float]]]): The config of the whole project,
                read more @ `../../genetic-algorithm-config.yaml`.
        """
        self.pid_boundary: List[float] = \
            config["genetic-algorithm"]["PID-boundary"]
        self.eta_boundary: List[float] = \
            config["genetic-algorithm"]["eta-boundary"]
        self.population_number: int = \
            config["genetic-algorithm"]["population-number"]
        self.mutation_probability: float = \
            config["genetic-algorithm"]["mutation-probability"]
        self.crossover_rate: float = \
            config["genetic-algorithm"]["crossover-rate"]
        self.control_system_config: Dict[str, Union[float, List[float]]] = \
            config["control-system"]

        self.__generate_initial_population()

    def __generate_initial_population(self) -> None:
        """Generate the first populations of GA.

        If you want to change the PID / eta boundary, please modify at:

            `../../genetic-algorithm-config.yaml`

        """
        self.populations: List[Chromosome] = []
        for _ in range(self.population_number):
            self.populations.append(
                Chromosome(
                    kp=uniform(
                        self.pid_boundary[0],
                        self.pid_boundary[1],
                    ),
                    ki=uniform(
                        self.pid_boundary[0],
                        self.pid_boundary[1],
                    ),
                    kd=uniform(
                        self.pid_boundary[0],
                        self.pid_boundary[1],
                    ),
                    eta=uniform(
                        self.eta_boundary[0],
                        self.eta_boundary[1],
                    ),
                ))

    def produce_next_generation(self) -> None:
        """To the next generation.

            To evolve into the next generation, this function using the
            following steps:

                1. Get parent index by selection.
                2. Cross over all the parents with the probability of.
                   self.crossover_rate, then get the children (new populations).
                3. Mutate populations with self.mutation_probability.

        """
        fitness_values: List[float] = []
        for index in range(self.population_number):
            fitness_values.append(self.calculate_fitness(index))

        new_populations: List[Chromosome] = []
        for index in range(self.population_number):
            parent_index = self.__select(fitness_values)
            new_population = self.__cross_over(
                self.populations[parent_index],
                self.populations[parent_index + 1],
            )
            new_population = self.__mutation(new_population)
            new_populations.append(new_population)

        self.populations = new_populations

    def __check_boundary(self, value: float, boundary: List[float]):
        """Verify that the value is within the boundary.

        Args:
            value (float): The value of PID or eta.
            boundary (List[float]): The Boundary of the value, it has
                to be in this form: [min_boundary, max_boundary].

        Returns:
            float: The value within boundary.

        """
        if value < boundary[0]:
            value = boundary[0]
        elif value > boundary[1]:
            value = boundary[1]

        return value

    def __mutation(self, chromosome: Chromosome) -> Chromosome:
        """Mutate the chromosome with the probability of self.mutation_probability.

        Args:
            chromosome (Chromosome): The Chromosome that contain PID and eta value,
                read more @ `./Chromosome.py`.

        Returns:
            Chromosome: The Chromosome that could have mutated and within the boundary.

        """
        value_scale_number = uniform(-0.3, 0.3)
        if random() < self.mutation_probability * 0.25:
            chromosome.kp += random() * value_scale_number
            chromosome.kp = self.__check_boundary(
                chromosome.kp,
                self.pid_boundary,
            )

        elif random() < self.mutation_probability * 0.5:
            chromosome.ki += random() * value_scale_number
            chromosome.ki = self.__check_boundary(
                chromosome.ki,
                self.pid_boundary,
            )

        elif random() < self.mutation_probability * 0.75:
            chromosome.kd += random() * value_scale_number
            chromosome.kd = self.__check_boundary(
                chromosome.kd,
                self.pid_boundary,
            )

        elif random() < self.mutation_probability:
            chromosome.eta += 4 * random() * value_scale_number
            chromosome.eta = self.__check_boundary(
                chromosome.eta,
                self.eta_boundary,
            )

        return chromosome

    def __cross_over(
        self,
        parent_1: Chromosome,
        parent_2: Chromosome,
    ) -> Chromosome:
        """Cross over two parents (chromosomes).

        Args:
            parent_1 (Chromosome): A chromosome that ready to cross over.
            parent_2 (Chromosome): Another chromosome that ready to cross over.

        Returns:
            Chromosome: The child that parent_1 and parent_2 cross overed with.
        """
        if random() > self.crossover_rate:
            return parent_1
        else:
            random_number = random()
            if random_number < 1 / 5:
                return Chromosome(
                    parent_2.kp,
                    parent_1.ki,
                    parent_1.kd,
                    parent_2.eta,
                )
            elif random_number < 2 / 5:
                return Chromosome(
                    parent_1.kp,
                    parent_2.ki,
                    parent_1.kd,
                    parent_2.eta,
                )
            elif random_number < 3 / 5:
                return Chromosome(
                    parent_1.kp,
                    parent_1.ki,
                    parent_2.kd,
                    parent_1.eta,
                )
            elif random_number < 4 / 5:
                return Chromosome(
                    parent_2.kp,
                    parent_1.ki,
                    parent_2.kd,
                    parent_1.eta,
                )
            else:
                return parent_2

    def __select(self, fitness_values: List[float], k: int = 2) -> int:
        """Select the best gene (population index) by fitness_values.

        Args:
            fitness_values (List[float]): The populations' score.
            k (int, optional): How many B's are used to cross over. Defaults to 2.

        Returns:
            int: The best gene (population index).
        """
        selection_index: int = randint(0, len(fitness_values) - 1)
        for index in randint(0, len(fitness_values) - 1, k):
            if fitness_values[index] < fitness_values[selection_index]:
                selection_index = index

        return selection_index

    def calculate_fitness(self, index: int) -> float:
        """Calculate the control system fitness.

        Args:
            index (int): The population's index that ready to run the
                control system.

        Returns:
            float: the fitness of the population and control system.
        """
        control_system = ControlSystem(
            chromosome=self.populations[index],
            config=self.control_system_config,
        )

        control_system.run()
        return control_system.get_fitness_value()
