import math
import random
import statistics
from typing import List, Tuple

import numpy as np

from decision_tree import DecisionTree


class RandomForest:
    def __init__(
        self,
        dataset: list,
        tree_count: int,
        min_split_length: int = 2,
        max_depth: int = 2,
        require_variance_reduction_greater_than_0: bool = True,
        seed: int = 0,
    ):
        """Decision trees are good; however, they are prone to over fitting.
        This class is a combination of many decision tress to help solve that problem

        Args:
            dataset (list): A list of data that you want to train the trees on
            tree_count (int): How many decision trees populate in the forest
            min_split_length (int, optional): config settings for DecisionTree brought up 1 level. Defaults to 2.
            max_depth (int, optional): config settings for DecisionTree brought up 1 level. Defaults to 2.
            require_variance_reduction_greater_than_0 (bool, optional): config settings for DecisionTree brought up 1 level. Defaults to True.
            seed (int, optional): random is good, but controlled random is better, this allows for repeatable results. Defaults to 0.
        """
        self.dataset = dataset
        self.tree_count = tree_count
        self.min_split_length = min_split_length
        self.max_depth = max_depth
        self.require_variance_reduction_greater_than_0 = (
            require_variance_reduction_greater_than_0
        )
        self.seed = seed
        self.forest: List[DecisionTree] = []

        if self.seed != 0:
            random.seed(self.seed)

        # People have found that Log(dataset[0]) or sqrt(dataset[0]) return good results.
        # in this example after some trial and error I've found sqrt(dataset[0]) // 2 to be a better fit
        knock_out_features_size = int(math.sqrt(len(dataset[0]))) // 2

        # Creating all of the trees in our forest!
        for _ in range(self.tree_count):
            # initalization of the tree
            tree = DecisionTree(
                min_split_length=self.min_split_length,
                max_depth=self.max_depth,
                require_variance_reduction_greater_than_0=self.require_variance_reduction_greater_than_0,
            )

            # Getting a random set of data from the dataset that is the same size of the dataset
            # *NOTE* if this looks strange, you are right! There will be duplicate values and that is intentional
            random_dataset = [
                dataset[random.randint(0, len(dataset) - 1)]
                for _ in range(len(dataset))
            ]

            # People have found that Log(dataset[0]) or sqrt(dataset[0]) return good results.
            # in this example after some trial and error I've found sqrt(dataset[0]) // 2 to be a better fit
            # we are nulling out the values to help them not be used in data selection. We could also set them all to 1
            # all that matters is that these values are all the same
            knock_out_features = [
                random.randint(0, len(dataset[0]) - 1)
                for _ in range(knock_out_features_size)
            ]
            for dataset_index in range(len(random_dataset)):
                for knockout in knock_out_features:
                    random_dataset[dataset_index][knockout] = 0

            # I've found in this use case that it is more 'realistic' if we have the healthy option be in all trees dataset
            random_dataset.append(dataset[0])

            tree.build_tree(np.array(random_dataset))

            self.forest.append(tree)

    def print_forest(self):
        """The forest is called, and so it's trees are called"""
        for tree in self.forest:
            tree.print_tree()

    def make_prediction(self, dataset: np.array) -> Tuple[float, List[int]]:
        """Getting the predictions of the forest

        Args:
            dataset (np.array): A dataset of only the inputs

        Returns:
            Tuple[float,List[int]]:
                float : the average of the trees
                List[int] : all of the predictions
        """

        predictions = []
        for tree in self.forest:
            prediction = tree.make_prediction(dataset=dataset)
            predictions.append(prediction)

        predictions.sort()

        return statistics.mean(predictions), predictions
