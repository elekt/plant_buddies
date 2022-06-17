import sys

from poly_grouper.evolutionary_grouper import EvolutionaryGrouper
import logging

if __name__ == '__main__':
    grouper = EvolutionaryGrouper()

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s -- %(message)s",
    )

    fitness_0 = grouper._fitness(['bab', 'póréhagyma', 'kukorica', 'korai burgonya', 'tök', 'kapor', 'cukkini', 'répa', 'retek', 'saláta'])
    fitness_1 = grouper._fitness(['kelkáposzta', 'paradicsom', 'retek', 'fokhagyma', 'cékla', 'cukkini', 'uborka', 'napraforgó', 'bab', 'kapor'])
    fitness_2 = grouper._fitness(['kukorica', 'bab', 'korai burgonya', 'napraforgó', 'kapor', 'borsó', 'cékla', 'rukkola', 'káposzta', 'cukkini'])


    # max = 0
    # for i in range(100):
    #     poly_culture = grouper.polyculutre
    #     fitness = grouper._fitness(poly_culture)
    #     if fitness > max:
    #         # max = fitness
    #         print(fitness)
    #         print(poly_culture)
