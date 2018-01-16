from DecisionTree import *
from DataSet import *
import timeit


def main_routine(dataset):
    print("\n\n ==== Dataset: " + dataset.name + " ====")
    st = timeit.default_timer()

    attributi = dataset.attributes
    accuracy = []
    nodes = []
    m = [0.00, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.20, 0.25, 0.30]  # soglia di errori sul prepruning

    decisions = dataset.decisions()

    print("Attributi " + str(len(attributi)))
    for a in attributi:
        print(a + " ", end="")
    print("\n")

    print("Decisions Set " + str(len(decisions)))
    for d in decisions:
        print(d + " ", end="")
    print("\n")

    print("PHASE == NODES NUMB == ACCURACY")
    for s in range(int(len(m))):

        training_set, test_set = dataset.get_sets()

        albero = DecisionTree(training_set, dataset.attributes, dataset.target, m[s], dataset.decisions())
        albero.learn()
        nodi = albero.conta_nodi()

        # albero.print()
        accuracy.append(albero.test(test_set))
        nodes.append(albero.conta_nodi())

        print('%-12s%-12s%-12s' % (str(s), str(nodi), str(round((accuracy[-1] * 100), 3))))

    et = timeit.default_timer() - st
    print("\nExecution time for this dataset: " + str(round(et, 2)) + "s")

    # Plot data
    dataset.plot_results(nodes, accuracy)

# ====== WARNINGS =======
# 1) Indicare il path del dataset (che deve essere in csv)
# 2) Indicare la posizione dell'attributo obiettivo se diversa da n-1
#
# Se si cambia dataset assicurarsi di aver rispettato tutte le indicazioni


main_routine(DataSet('mushrooms.csv', 0))

main_routine(DataSet('restaurants.csv'))

main_routine(DataSet('kr-vs-kp.csv'))