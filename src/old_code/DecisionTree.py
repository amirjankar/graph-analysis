import math
import pandas

"""
@author: Brendan Moore
"""


class Node:
    def __init__(self, indexes):
        """
        Constructs a node.
        :param indexes: The indexes (rows) of this node.
        """
        self.leaf = False
        self.children = {}
        self.attribute = None
        self.indexes = indexes
        self.category = None

    def is_leaf(self):
        """
        Returns whether or not this node is a leaf node.
        :return: True if leaf
        """
        return self.leaf

    def get_child(self, id):
        """
        Gets a child node of this node given its id.
        :param id: The data value used to split from its parent. For example, if its parent is split at
                   hair color, the children would have ids of blonde, brown, red, etc.
        :return: The child node
        """
        try:    # If the data is numerical
            int(id)
            for k in sorted(self.children.keys(), reverse=True):
                if id >= k:
                    return self.children[k]
            return self.children[sorted(self.children.keys())[0]]
        except ValueError:   # if the data is categorical
            return self.children[id]

    def get_attribute(self):
        """
        Returns the attribute used to split this node.
        :return: the attribute as a string
        """
        if not self.is_leaf():
            return self.attribute
        else:
            raise Exception("Leaf nodes have no attribute.")

    def get_indexes(self):
        """
        Gets the indexes associated with this node. Indexes refer to row values.
        :return: a list of indexes
        """
        return self.indexes

    def get_category(self):
        """
        Gets the category of this node if it is a leaf node.
        :return: the category as a string
        """
        return self.category

    def all_same_class(self, labels):
        """
        Returns true if all the data in this node is of the same class.
        :param labels: a dataframe representing the values of the attribute to be learned
        :return: True if all the labels are the same
        """
        same = True
        for i in range(1, len(self.indexes)):
            in1 = self.indexes[i-1]
            in2 = self.indexes[i]
            if not labels[in1] == labels[in2]:
                same = False
                break
        if same:
            self.category = labels[0]
        return same

    @staticmethod
    def get_entropy(labels):
        """
        Gets the entropy of the data in this node
        :param labels: a dataframe representing the values of the attribute to be learned
        :return: the entropy as a float
        """
        already = {}
        logs = []
        total = labels.size
        for label in labels:
            if label not in already.keys():
                already[label] = 1
            else:
                already[label] += 1
        for i in already.keys():
            logs.append((already[i] / total) * math.log2(already[i] / total))
        sum = 0
        for i in logs:
            sum += i
        return -sum


class Data:
    def __init__(self, path, to_learn, split=0.75):
        """
        Creates a data object containing the original dataset and its divisions into training and test data
        :param path: a file path to the dataset. Should be a .csv file
        :param to_learn: the attribute to learn, as a string
        :param split: a number from 0 to 1 representing the proportion of data to be put in the training set
        """
        self.data = pandas.read_csv(path, sep=",")
        self.x_train, self.x_test, self.y_train, self.y_test = self.split_data(to_learn, split)

    def split_data(self, to_learn, split):
        """
        Splits the data into training and test data and labels
        :param to_learn: the attribute to learn, as a string
        :param split: a number from 0 to 1 representing the proportion of data to be put in the training set
        :return: training data, test data, training labels, test labels
        """
        labels = self.data.loc[:, to_learn]
        split_index = int(self.data.shape[0] * split)
        x_train = self.data.iloc[:split_index, :].drop(to_learn, axis=1)
        x_test = self.data.iloc[split_index:self.data.shape[0], :].drop(to_learn, axis=1)

        y_train = labels.iloc[:split_index]
        y_test = labels.iloc[split_index:self.data.shape[0]]

        return x_train, x_test, y_train, y_test


class DecisionTree:
    def __init__(self, data, labels, RANGES=5):
        """
        Constructs a DecisionTree
        :param data: the test data
        :param labels: the test labels
        :param RANGES: the number of ranges to split numerical data into
        """
        self.data = data
        self.labels = labels
        self.root = None
        self.RANGES = RANGES

    def information_gain(self, parent_node, children_tuples):
        """
        Calculates the information gain from a parent node to its children nodes
        :param parent_node: a node
        :param children_tuples: a list of tuples in the form (Node, data value)
        :return: the information gain, as a float
        """
        parent_indexes = parent_node.get_indexes()
        total_entropy = parent_node.get_entropy(self.labels[parent_indexes])
        children_entropy = 0
        for t in children_tuples:
            child = t[0]
            indexes = child.get_indexes()
            entropy = child.get_entropy(self.labels[indexes])
            children_entropy += (entropy * (len(indexes) / len(parent_indexes)))
        return total_entropy - children_entropy

    def get_ranked_splits(self, splits):
        """
        Takes a list of splits and ranks them according to information gain
        :param splits: a list of tuples in the form (parent Node, list of children tuples, attribute)
        :return: a ranked list of splits
        """
        return sorted(splits, key=lambda x: self.information_gain(x[0], x[1]), reverse=True)

    def build_tree(self):
        """
        Builds a DecisionTree
        :return: the root of the DecisionTree
        """
        root = Node(list(range(self.data.shape[0])))
        self.build_tree_helper(root)
        self.root = root
        return root

    def build_tree_helper(self, node):
        """
        Helper function for build_tree
        :param node: a Node
        :return: a Node
        """
        if node.all_same_class(self.labels):
            node.leaf = True
            return node

        splits = []

        for attr in self.data.loc[:]:
            nodes = {}

            try:    # If the attribute is numerical
                int(self.data.iloc[0][attr])

                ranges = []
                low = math.inf
                high = -math.inf
                for i in self.data.loc[:, attr]:
                    if i > high:
                        high = i
                    if i < low:
                        low = i
                increment = (high - low) / self.RANGES
                ranges.append([-math.inf, low])
                while low < high:
                    prev = low
                    low += increment
                    ranges.append([prev, low])
                ranges.append([high, math.inf])

                for r in ranges:
                    # The low end of a range is the key. The values are the data points in that range.
                    nodes[r[0]] = []

                for index in node.get_indexes():
                    data_point = self.data.loc[index, attr]
                    for r in reversed(ranges):
                        if data_point >= r[0]:
                            nodes[r[0]].append(index)
                            break
            except ValueError:  # If the attribute is not numerical
                for index in node.get_indexes():
                    data_point = self.data.loc[index, attr]
                    if data_point in nodes.keys():
                        nodes[data_point].append(index)
                    else:
                        nodes[data_point] = [index]

            children = []
            for k in nodes.keys():
                if nodes[k]:
                    children.append((Node(nodes[k]), k))
            if len(children) > 1:
                splits.append((node, children, attr))

        if not splits:
            counts = {}
            for i in node.get_indexes():
                if self.labels[i] in counts.keys():
                    counts[self.labels[i]] += 1
                else:
                    counts[self.labels[i]] = 1

            max_label = None
            max_count = 0
            for k in counts.keys():
                if counts[k] > max_count:
                    max_count = counts[k]
                    max_label = k

            node.category = max_label
            node.leaf = True
            return node

        ranked_splits = self.get_ranked_splits(splits)
        node.attribute = ranked_splits[0][2]

        for t in ranked_splits[0][1]:
            node.children[t[1]] = self.build_tree_helper(t[0])

        return node

    def classify(self, data_point):
        """
        Classifies a data point using the built DecisionTree
        :param data_point: a row of data
        :return: the predicted category of the data point
        """
        if not self.root:
            raise Exception("You must build the tree before classifying.")

        current_node = self.root
        while not current_node.is_leaf():
            current_node = current_node.get_child(data_point[current_node.get_attribute()])
        return current_node.get_category()


if __name__ == "__main__":
    # Tests
    data = Data("airline-safety.csv", "fatal_accidents_00_14", split=0.75)
    dt = DecisionTree(data.x_train, data.y_train, RANGES=5)
    dt.build_tree()
    print("Prediction   Actual")
    x = 0
    correct = 0
    for dp in data.x_test.iterrows():
        prediction = dt.classify(dp[1])
        actual = data.y_test.iloc[x]
        if prediction == actual:
            correct += 1
        print(prediction, "\t", actual)
        x += 1
    print("Percent correct: ", correct / data.y_test.shape[0])
