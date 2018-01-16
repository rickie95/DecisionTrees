import csv
import random
import matplotlib.pyplot as plt


class DataSet:

    def __init__(self, path, target=None):
        """ Costructor\n
            path: name of dataset [dataset.csv]\n
            target: position of target attribute (use array notation)\n
        """
        self.name = str(path.split(".")[0])
        self.attributes = []  # a list of attributes
        self.examples = []  # a list of examples
        self.target_pos = target
        example = []  # a list of values

        with open("datasets/"+path) as file:
            reader = csv.reader(file, delimiter=',', quotechar='|')
            attrib = True
            for row in reader:
                if attrib:
                    self.attributes = [data for data in row]
                    attrib = False
                else:
                    for data in row:
                        example.append(data.strip())
                    self.examples.append(example.copy())
                    example.clear()
            file.close()

        random.shuffle(self.examples)
        if self.target_pos is None:
            self.target_pos = len(self.attributes)-1
        self.target = self.attributes[self.target_pos]

    def print(self):
        print("Obbiettivo: " + self.target)
        print(self.attributes)
        for row in self.examples:
            print(row)

    def posTarget(self):
        """ Return target's position."""
        return self.attributes.index(self.target)

    def get_sets(self, proportion=0.8):
        """Creates training and test datasets.
            Return training, test.
        """

        choosen = []

        def split(set):
            """ Split a set in two subsets. The proportion is inherited by get_sets() method.
                Return a major and a minor set
            """
            major = set.copy()
            minor = []
            num_of_examples = int(((len(set) - 1) * (1-proportion)))
            # prima il minor
            while len(minor) < num_of_examples:  # devo aver scelto tutti gli esempi
                    try:
                        ind = random.randrange(0, len(set) - 1)
                        choosen.index(ind)
                        # L'ho gia inserito
                    except ValueError:  # Non l'ho scelto, lo inserisco nel minor e lo tolgo dal major
                        minor.append(set[ind])
                        major.remove(set[ind])
                        choosen.append(ind)
            return major, minor

        training, test = split(self.examples)
        random.shuffle(training)
        random.shuffle(test)
        return training, test

    def decisions(self):
        """ Create a list of unique class IDs
        """
        return list(x for x in set([e[self.attributes.index(self.target)] for e in self.examples]))

    def plot_results(self, nodes, accuracy):
        """ Plots accuracy score by nodes number.
            If there exist multiple values for the same number of node uses the medium value.
            All values are rounded to 4th decimal."""
        couples = []
        for n in nodes:
            duplicates =[index for index, value in enumerate(nodes) if value == n]  # indici dei nodi
            if len(duplicates) > 1:
                couples.append((n, sum([accuracy[ind] for ind in duplicates])/len(duplicates)))
                for d in duplicates:  # molto brutto
                    nodes[d] = -1
                    accuracy[d] = -1
                for i in range(len(duplicates)):
                    nodes.remove(-1)
                    accuracy.remove(-1)
            else:
                couples.append((n, accuracy[nodes.index(n)]))

        couples.sort()  # ordinate per numero di nodi
        nodes.clear()
        accuracy.clear()

        nodes, accuracy = zip(*couples)
        plt.plot(nodes, accuracy)

        plt.xlabel("Number of nodes")
        plt.ylabel("Accuracy")
        # plt.ylim([0, 1])
        plt.title("Dataset: " + self.name)
        plt.show()
