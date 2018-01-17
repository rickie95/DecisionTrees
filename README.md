# DecisionTrees
ENG

This is a school project about Decision Trees for the Artificial Intelligence course in Computer Science Engineering at University of Florence (Italy).

My assignment was to develop an ID3's variant with tree's complessity check, then test it with some datasets:
  - "Restaurants", a synthetic one created with Norvig's tool on aima-code repo, here on github.
  - "Mushrooms", you can found it on UCI ML Repository
  - "kr-vs-kp", also avaiable on UCI
  
 The algorithm is very similar to the one present on ch18.3 "Aritificial Intelligence: A Modern Approach" by Norvig & Russel.
 
 ## Code
 
```python
 
 # Translated version
 
def __learn_decision_tree(self, examples, attributes, default):
     if len(examples) == 0:                       # Case no.3
         return default
     elif self.same-class(esempi):                # Caso no.2
         return AnswerLeaf(example[0][self.target_pos])
     elif len(attributes)-1 == 0:                 # Case no.4
         return AnswerLeaf(self.majority-value(esempi))
     else:                                        # Case no.1
           # === PRE PRUNING ===
         if self.errors(examples) < self.error_threshold:
             return AnswerLeaf(self.majority-value(examples))
             
         best = self.choose-attrib(self.separate_list(attributes, self.target_name), examples)
         tree = AttribNode(self.attributi[best])
         m = AnswerLeaf(self.majority-value(examples))
         for value in set([ex[best] for ex in examples]):  
             examples_i = [e for e in examples if e[best] == value] 
             sub_tree = self.__learn_decision_tree(
                 examples_i, self.separate_list(attributes, self.attributes[best]), m)
             tree.add_sub_tree(sub_tree, value)

         return tree
         
```
# Install and usage

- Clone repo
- Assuming that you are using venv, create a new enviroment with python3 and install all the packages listed in requirements.txt
- Run main.py
- [Bonus] If you are not using an IDE or you haven't installed Scikit viewer you have to close every plot to see the next one

# Useful info

- There is a short report (in Italian for now) where you can find a very little brief about this implementation and some chart obtained by dataset listed above.
- As you can see, **the project is written with Python 3**. If you want test it you can download and run from your IDE, you can use my virtual enviroment (venv) or create a new one and install the requested packages listed in *requirements.txt*.
- I did not test with Linux/MacOs, you could encountering troubles with pathnames in the code ("/" and "\"). In this scenario, considerate to move datasets in the same script's folder and remove  [ "dataset"+ ] in row 19 from Dataset.py



