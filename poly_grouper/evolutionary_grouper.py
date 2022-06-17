import logging

import pandas as pd
from typing import List
import numpy as np
import itertools

types_path = "data/types.csv"
companions_path = "data/companions.csv"

DROPPED_PLANTS = ["paprika", "körömvirág", "brokkoli", "hajdina", "büdöske", "szamóca", "bazsalikom", "padlizsán", "luffatök", "sarkantyúka", "paszternák"]

class EvolutionaryGrouper:

    def __init__(self):
        self.df_types = pd.read_csv(types_path, index_col=0)
        self.df_companions = pd.read_csv(companions_path, index_col=0)

        self.df_companions = self.df_companions.replace({1: -1})
        self.df_companions = self.df_companions.fillna(0.5)

        self.df_companions = self.df_companions.drop(DROPPED_PLANTS)
        self.df_companions = self.df_companions.drop(DROPPED_PLANTS, axis=1)
        self.df_types = self.df_types.drop(DROPPED_PLANTS)

        assert all(self.df_companions.index == self.df_companions.columns)
        assert set(self.df_companions.index) == set(self.df_types.index)

        self.FITNESS_SCORE_MAX = 100

    @property
    def polyculutre(self):
        return self._get_policulture(
            n_iter=200,
            n_gen=10,
            n_pop=30,
            r_cross=0.7,
            r_mut=0.2,
        )

    def _fitness(self, plant_group: List):
        """
        Function to evaluate a a plant group as buddies

        Parts of evaluating fitness:
        - different plant family combinations
        - score of how well each plant prefers to be with the other
        - to have a range in light and water needs

        Args:
            plant_group: a list of plants as a candidate for buddies

        Returns: fitness value
        """

        family_match = len(self.df_types[self.df_types.index.isin(plant_group)]['family'].unique()) / len(plant_group)
        logging.info(plant_group)
        logging.info(f"\nfamily_match: {family_match:.2f}")

        ##
        companions_score_max = 2 * (len(plant_group)**2)
        score_companions = self.df_companions[self.df_companions.index.isin(plant_group)][plant_group].sum().sum() / companions_score_max
        logging.info(f"score_companions: {score_companions:.2f}")


        # TODO water and light  shall have min len(plant_group) / 3 False in each column
        ##
        water_needs = self.df_types[self.df_types.index.isin(plant_group)][["water_full", "water_mid", "water_low"]].isna().apply(pd.Series.value_counts).sum(axis=1).to_dict().get(False, 0) / (len(plant_group)*3)
        logging.info(f"water_needs: {water_needs:.2f}")

        ##
        light_needs = self.df_types[self.df_types.index.isin(plant_group)][["light_full", "light_mid", "light_low"]].isna().apply(pd.Series.value_counts).sum(axis=1).to_dict().get(False, 0) / (len(plant_group)*3)
        logging.info(f"light_needs: {light_needs:.2f}")

        # IMPORTANCE companion no -1, family, rest
        fitness = self.FITNESS_SCORE_MAX * (0*water_needs + 0*light_needs + 0.3*family_match + 0.7*score_companions)
        logging.info(f"Fitness: {fitness:.2f}")
        # print()

        return fitness

    @staticmethod
    def _selection(pop, scores):
        k = int(0.3 * len(pop))
        selection_ix = np.random.randint(len(pop))
        for ix in np.random.randint(0, len(pop), k - 1):
            if scores[ix] < scores[selection_ix]:
                selection_ix = ix
        return pop[selection_ix]


    @staticmethod
    def _crossover(p1: List, p2: List, r_cross: float):
        c1, c2 = p1.copy(), p2.copy()
        if np.random.rand() < r_cross:
            pt = np.random.randint(1, len(p1) - 2)
            c1 = list(itertools.chain(p1[:pt], p2[pt:]))
            c2 = list(itertools.chain(p2[:pt], p1[pt:]))
        return [c1, c2]

    def _mutation(self, bitstring: List, r_mut: float):
        for i in range(len(bitstring)):
            if np.random.rand() < r_mut:
                new_gene = np.random.choice(self.df_companions.index)
                bitstring[i] = new_gene

    def _get_policulture(self, n_iter: int, n_gen: int, n_pop: int, r_cross: float, r_mut: float):
        """
        Genetic algorithm for creating and evaluating possible plant groups

        Args:
            n_iter: number of times a population is updated
            n_gen: size of the gene (number of plants in group)
            n_pop: size of the population
            r_cross: Chance of making crossover from 2 selected entity
            r_mut: Chance of mutation of an entity after crossover

        Returns: Best found plant group
        """
        assert n_pop % 2 == 0

        pop = [
            np.random.choice(self.df_companions.index, size=n_gen)
            for _ in range(n_pop)
        ]
        best, best_eval = None, 0
        for gen in range(n_iter):
            scores = [self._fitness(c) for c in pop]
            for i in range(n_pop):
                if scores[i] > best_eval:
                    best, best_eval = pop[i], scores[i]

            selected = [self._selection(pop, scores) for _ in range(n_pop)]
            children = []
            for i in range(0, n_pop, 2):
                p1, p2 = selected[i], selected[i + 1]
                for c in self._crossover(p1, p2, r_cross):
                    self._mutation(c, r_mut)
                    children.append(c)
            pop = children

        return best
