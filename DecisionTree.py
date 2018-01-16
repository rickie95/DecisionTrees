# coding=utf-8
from cmath import log


# AttribNode
# Modella l'attributo, da cui partono le diramazioni per i figli (altri nodi o foglie)

class AttribNode:

    def __init__(self, attrib_name=None):
        self.figli = []  # lista composta da coppie (nodo, valore)
        self.name = attrib_name

    def add_sub_tree(self, tree, value):  # aggiungo un sottoalbero identificato dall'etichetta
        self.figli.append((tree, value))

    def print(self, tab=0):
        for (tree, value) in self.figli:
            print("\t" * tab + " " + value + " => ", end="")  # condizione=>[scelta|domanda]
            tree.print((tab + 1))

    def test(self, v):
        for tree, value in self.figli:
            if value == v:
                return tree

    def get_name(self):
        return self.name

    def conta_nodi(self):
        n = 0
        for (tree, value) in self.figli:
            n += tree.conta_nodi()
        return n+1


# AnswerLeaf
# Rappresenta la singola risposta (Y/N per la maggior parte dei casi)

class AnswerLeaf:

    def __init__(self, decision):
        self.decision = decision

    def get_choice(self):
        return self.decision

    def print(self, tab=0):
        print(self.get_choice())

    def __repr__(self):
        return self.decision

    def test(self, value):
        return self

    def conta_nodi(self):
        return 0

#   Da Russel,Norvig "Artificial Intelligence: A Modern Approach", cap 18.3
#   L'algoritmo è studiato per distinguere 4 casi:
#   1) Ci sono sia esempi + che -. Scelgo l'attributo che li suddivide meglio
#   2) Tutti gli esempi rimanenti hanno lo stesso "segno". Posso dare una risposta
#   3) Non ci sono più esempi: Viene restituito un valore di maggioranza dato dal nodo parent
#   4) Non rimane alcun attributo, mentre ci sono esempi rimanenti.

class DecisionTree:

    def __init__(self, examples, attributes, target_name, error_threshold=0.3, decisions=None, default=None, verbose=False):
        self.esempi = examples
        self.attributi = attributes
        self.target_name = target_name
        self.target_pos = attributes.index(target_name)
        self.error_threshold = error_threshold
        self.albero = None
        self.verbose = verbose
        self.decisions = decisions or ['Yes', 'No']
        self.default = decisions[0]

    def learn(self):
        self.albero = self.__learn_decision_tree(self.esempi, self.attributi, self.default)

    def __learn_decision_tree(self, esempi, attributi, default):  # we're all adults here
        if len(esempi) == 0:                       # Caso no.3
            return default
        elif self.stessa_classificazione(esempi):  # Caso no.2
            return AnswerLeaf(esempi[0][self.target_pos])
        elif len(attributi) == 0:                  # Caso no.4
            return AnswerLeaf(self.valore_maggioranza(esempi))
        else:                                      # Caso no.1
            # === PRE PRUNING ===
            if self.errori(esempi) < self.error_threshold:
                return AnswerLeaf(self.valore_maggioranza(esempi))
            miglior_attributo = self.scegli_attributo(self.separa_lista(attributi, self.target_name), esempi)
            albero = AttribNode(self.attributi[miglior_attributo])
            m = AnswerLeaf(self.valore_maggioranza(esempi))
            for valore in set([ex[miglior_attributo] for ex in esempi]):  # ottengo le occorenze uniche
                esempi_i = [e for e in esempi if e[miglior_attributo] == valore]  # list comprehension overpower
                sotto_albero = self.__learn_decision_tree(
                    esempi_i, self.separa_lista(attributi, self.attributi[miglior_attributo]), m)
                albero.add_sub_tree(sotto_albero, valore)

            return albero

    def valore_maggioranza(self, esempi):  # Restituisco la classificazione più comune del genitore
        classifica = []
        score = []

        for i in range(0, len(esempi) - 1):
            try:
                index = classifica.index(esempi[i][self.target_pos])  # provo a cercarlo
            except ValueError:
                classifica.append(esempi[i][self.target_pos])  # Se non lo trovo lo aggiungo
                index = len(classifica) - 1
                score.append(0)
            finally:
                score[index] += 1  # sia che lo trovi, sia che lo inserisca

        popular_decision = score.index(max(score))
        return classifica[popular_decision]

    def errori(self, esempi):  # mi conta gli errori rispetto alla valutazione di maggioranza
        valore_magg = self.valore_maggioranza(esempi)
        n_errori = 0
        for e in esempi:
            if e[self.target_pos] != valore_magg:
                n_errori += 1
        return n_errori/len(esempi)

    def stessa_classificazione(self, esempi):
        if len(esempi) == 1:
            return True
        test = esempi[0][self.target_pos]
        for es in esempi:
            if test != es[self.target_pos]:
                return False
        return True

    def entropy(self, p, n):
        t = p + n
        if p == 0:
            return - (n / t) * log(n / t, 2).real
        if n == 0:
            return -(p / t) * log(p / t, 2).real
        return -(p / t) * log(p / t, 2).real - (n / t) * log(n / t, 2).real

    def calcola_guadagno_informazione(self, attributo, esempi):
        valori = []  
        frequenze = []  
        for e in esempi:
            try:
                index = valori.index(e[attributo])  # provo a cercarlo
            except ValueError:
                valori.append(e[attributo])  # Se non lo trovo lo aggiungo
                index = len(valori) - 1
                frequenze.append([0, 0])
            finally:
                frequenze[index][0] += 1  # sia che lo trovi, sia che lo inserisca
                if e[self.target_pos] == self.decisions[0]:  # se è positivo registro
                    (frequenze[index])[1] += 1
        # una volta fatto posso restituire il guadagno per il singolo attributo

        n_esempi = sum(x for x, y in frequenze)
        return 1 - (1 / n_esempi) * sum(occorrenze * self.entropy(pos, occorrenze - pos) for occorrenze, pos in frequenze)

    def scegli_attributo(self, attributi, esempi):
        guadagni = [self.calcola_guadagno_informazione(self.attributi.index(a), esempi) for a in attributi]
        max_gain = max(guadagni)
        m = guadagni.index(max_gain)  # indice del candidato
        m = self.attributi.index(attributi[m])  # indice del candidato nella lista originale
        if self.verbose:
            print("Ho scelto l'attributo " + self.attributi[m] + " con information gain = " + max_gain)
        return m

    @staticmethod
    def separa_lista(lista, target_name):
        lis = [li for li in lista if li != target_name]
        return lis

    def conta_nodi(self):
        if self.albero is None:
            return 0

        return self.albero.conta_nodi()

    def print(self):
        self.albero.print()

    def getAlbero(self):
        return self.albero

    def test(self, test_set):
        if self.albero is None:
            print("Non è presente nessun albero")
        hit = 0
        for e in test_set:
            node = self.albero
            # navigo l'albero fino a trovare la foglia che mi da' la risposta
            while node.__class__.__name__ == "AttribNode":
                attributo = node.get_name()  # mi arriva il nome
                attributo = self.attributi.index(attributo)
                node = node.test(e[attributo])
            if node is not None and e[self.target_pos] == node.get_choice():
                hit += 1
        return hit/len(test_set)  # restituisco la percentuale di test validati correttamente

