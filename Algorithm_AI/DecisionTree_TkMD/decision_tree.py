from typing import Optional, Tuple

import numpy as np

from utils import get_midpoint_list, read_csv_file


class TreeNode:
    def __init__(
        self,
        left_node: Optional["TreeNode"] = None,
        right_node: Optional["TreeNode"] = None,
        feature_value_index: int = None,
        feature_value_threshold_lte: float = None,
        variance_reduction: float = None,
        leaf_value: float = None,
    ):
        """A class for the nodes that exist on the tree

        Args:
            left_node (Optional[&quot;TreeNode&quot;], optional): A node less than or equal to the feature_value_threshold_lte. Defaults to None.
            right_node (Optional[&quot;TreeNode&quot;], optional): A node greater than the feature_value_threshold_lte. Defaults to None.
            feature_value_index (int, optional): the index of the list to be compared. Defaults to None.
                ex.
                if the feature_value_index is 2 and the
                input list is : [ 0, 1, 0, 2 ]
                                        ^
                                        |
                    this is the value that the feature_value_index tells you to reference in forward prop
            feature_value_threshold_lte (float, optional): The less than or equal to value to compare the feature_value to. Defaults to None.
            variance_reduction (float, optional): visual purposes only, the variance reduction when building the tree for this node. Defaults to None.
            leaf_value (float, optional): if all of the values above are None, than this should be populated. This indicates the end of a branch. Defaults to None.
        """
        # Child Nodes
        self.left_node = left_node
        self.right_node = right_node
        # Active Node Data
        self.feature_value_index = feature_value_index
        self.feature_value_threshold_lte = feature_value_threshold_lte
        self.variance_reduction = variance_reduction
        # Lead Node Data
        self.leaf_value = leaf_value


class DecisionTree:
    def __init__(
        self,
        min_split_length: int = 2,
        max_depth: int = 2,
        require_variance_reduction_greater_than_0: bool = True,
    ):
        """Decision trees are like if else branches that are generated in code. Just as some new programmers may write code saying...

        if this:
            if this:
                if this:
                else:
            else:
                if this:
                else:

        we too can have computers write and follow similar logic in decision making

        Args:
            min_split_length (int, optional): The minimum values to decide for. Defaults to 2.
                2 is a good number, because that gives most accurate; however, if large and plottable data, 3+ may be good too
            max_depth (int, optional): How deep we want our tree to go. Defaults to 2.
            require_variance_reduction_greater_than_0 (bool, optional): A delimiter for what we consider good or bad variance. Defaults to True.
                data that is floating does best with < ( student grades, probability, etc.. )
                data that is binary does best with <=  ( boolean algebra, yes or no options, etc.. )
        """
        self.root: TreeNode = None

        self.min_split_length: int = min_split_length
        self.max_depth: int = max_depth
        self.require_variance_reduction_greater_than_0 = (
            require_variance_reduction_greater_than_0
        )

    def _calculate_variance_reduction(
        self,
        dataset_outputs: np.array,
        left_dataset_outputs: np.array,
        right_dataset_outputs: np.array,
    ) -> float:
        """A hidden function used to calcuate variance

        Args:
            dataset_outputs (np.array): The list of options given before splitting.
                ex.
                [ 0 , 0 , 1 ]
            left_dataset_outputs (np.array): The left sublist of the list above
                ex.
                [ 0, 0 ]
            right_dataset_outputs (np.array): The right sublist of the list above
                ex.
                [ 1 ]

        Returns:
            float: the calculated variance reduction
        """
        # Grabbing the weight of the left and right, this is so we can make sure we are
        # A. Not exceeding the variance of dataset_outputs
        # B. Making sure that both left and right are treated with equal weight
        left_node_weight = len(left_dataset_outputs) / len(dataset_outputs)
        right_node_weight = len(right_dataset_outputs) / len(dataset_outputs)
        # Formula :
        # var(output) - ( var(left_output) * left_weight + var(right_output) * right_weight )
        return np.var(dataset_outputs) - (
            np.var(left_dataset_outputs) * left_node_weight
            + np.var(right_dataset_outputs) * right_node_weight
        )

    def _get_tree_split(self, dataset: np.array) -> Tuple[float, int, float]:
        """A hidden function to figure out where is best in a given list to split

        Args:
            dataset (np.array): the list of data to split

        Returns:
            Tuple[float, int, float]:
                best_variance_reduction (float): The maximum variance per split ( note, the best variance possible is var(dataset) )
                best_feature_index (int): The index of the list where we want to look at for the node of the decision tree
                best_unique_feature_threshold (float): A value to be compared to an indexed value of the dataset
        """
        # Finding the amount of input data per dataset
        _, dataset_input_features = np.shape(dataset[:, :-1])

        # It's all uphere from now
        best_variance_reduction = float("-inf")
        # -1 to help indicate that something went wrong
        best_feature_index = -1
        # It's all uphere from now
        best_unique_feature_threshold = float("-inf")

        # itterating over all of the input values
        for feature_index in range(dataset_input_features):
            # Grabbing the midpoint of the list, this is to help even out our tree and if given a set of [ 0 , 1 ]
            # be able to pick .5, for more gray data in practice
            unique_feature_values = get_midpoint_list(
                np.unique(dataset[:, feature_index])
            )

            # Itterating over the unique_feature_values
            for unique_feature_threshold in unique_feature_values:
                # splitting our dataset into values to the left of the feature value and values to the right of the feature value
                left_dataset = np.array(
                    [
                        value
                        for value in dataset
                        if value[feature_index] <= unique_feature_threshold
                    ]
                )
                right_dataset = np.array(
                    [
                        value
                        for value in dataset
                        if value[feature_index] > unique_feature_threshold
                    ]
                )

                # If either left or right is empty than there is no split, only a leaf to the branch
                if (len(left_dataset) <= 0) or (len(right_dataset) <= 0):
                    continue

                # Quick way to grab all of the outputs of each dataset
                dataset_outputs, left_dataset_outputs, right_dataset_outputs = (
                    dataset[:, -1],
                    left_dataset[:, -1],
                    right_dataset[:, -1],
                )

                feature_variance_reduction = self._calculate_variance_reduction(
                    dataset_outputs=dataset_outputs,
                    left_dataset_outputs=left_dataset_outputs,
                    right_dataset_outputs=right_dataset_outputs,
                )

                # checking if our feature variance is greater than or equal to the best variance, and if so adjusting out return values
                if feature_variance_reduction < best_variance_reduction:
                    continue

                best_variance_reduction = feature_variance_reduction
                best_feature_index = feature_index
                best_unique_feature_threshold = unique_feature_threshold

        return (
            best_variance_reduction,
            best_feature_index,
            best_unique_feature_threshold,
        )

    def _build_recursive_tree(self, dataset: np.array, depth: int = 0) -> TreeNode:
        """A recursive function to build the decision tree!

        Args:
            dataset (np.array): the data that a node should be recieving
            depth (int, optional): How far the tree go. Defaults to 0.
                ex.
                    depth 1
                       +-- A
                    0 -+-- B

                    depth of 2
                              +-- C
                       +-- A -+-- D
                    0 -|
                       +-- B -+-- E
                              +-- F
        Returns:
            TreeNode: Do not be decieved, because this is recursion.
                While this is 1 value returned, this value continus 2 TreeNodes (unless is a leaf node)
        """
        # Grabing the inputs and outputs
        dataset_inputs = dataset[:, :-1]
        dataset_outputs = dataset[:, -1]

        # checking if we have reached a leaf / end of our tree
        if (len(dataset_inputs) < self.min_split_length) or (depth > self.max_depth):
            return TreeNode(leaf_value=np.mean(dataset_outputs))

        # Finding the best place to split the branch that we are on
        (
            best_variance_reduction,
            best_feature_index,
            best_unique_feature_threshold,
        ) = self._get_tree_split(dataset=dataset)

        # Find if we have a leaf node becuase our variance is <= 0 ( or < 0 depending on the tree )
        # *NOTE*
        # data that is floating does best with < ( student grades, probability, etc.. )
        # data that is binary does best with <=  ( boolean algebra, yes or no options, etc.. )
        if self.require_variance_reduction_greater_than_0 and (
            best_variance_reduction <= 0
        ):
            return TreeNode(leaf_value=np.mean(dataset_outputs))
        if best_variance_reduction < 0:
            return TreeNode(leaf_value=np.mean(dataset_outputs))

        # If we have not created a leaf at this point, then we can create the child node to this branch

        # starting with the left dataset first so we can reduce the amount of memory that we are holding onto
        left_dataset = np.array(
            [
                value
                for value in dataset
                if value[best_feature_index] <= best_unique_feature_threshold
            ]
        )

        left_tree = self._build_recursive_tree(dataset=left_dataset, depth=depth + 1)

        # now building the right dataset
        right_dataset = np.array(
            [
                value
                for value in dataset
                if value[best_feature_index] > best_unique_feature_threshold
            ]
        )

        right_tree = self._build_recursive_tree(dataset=right_dataset, depth=depth + 1)

        # After we have recursively built our tree, then we are done and can return the branch.
        # This means that for a tree of :
        #               +-- C
        #        +-- A -+-- D
        #     0 -|
        #        +-- B -+-- E
        #               +-- F
        # we can expect the flow of.
        # Start : 0
        #   Create : A
        #       Create : C
        #       Finishes : C ( left node )
        #       Create : D
        #       Finishes : D ( right node )
        #   Finishes : A ( left node )
        #   Create : B
        #       Create : E
        #       Finishes : E ( left node )
        #       Create : F
        #       Finishes : F ( right node )
        #   Finishes : B ( right node )
        # Finishes : 0
        return TreeNode(
            left_node=left_tree,
            right_node=right_tree,
            feature_value_index=best_feature_index,
            feature_value_threshold_lte=best_unique_feature_threshold,
            variance_reduction=best_variance_reduction,
        )

    def build_tree(self, dataset: np.array, depth: int = 0):
        """Some abstraction from the recursive build tree since we need to assign it's output to the classes root

        Args:
            dataset (np.array): A dataset to model the tree of off
            depth (int, optional): How far the tree go. Defaults to 0.
                ex.
                    depth 1
                       +-- A
                    0 -+-- B

                    depth of 2
                              +-- C
                       +-- A -+-- D
                    0 -|
                       +-- B -+-- E
                              +-- F
        """
        self.root = self._build_recursive_tree(dataset=dataset, depth=depth)

    def make_prediction(self, dataset: np.array, tree: TreeNode = None) -> float:
        """A method to traverse the tree with trained or untrained data. Similar to building the tree, this method is recursively called

        Args:
            dataset (np.array): A dataset of only the inputs
            tree (TreeNode, optional): WHEN FIRST CALLING THIS SHOULD BE None !!!! Defaults to None.

        Returns:
            (float): The decision trees predicted value
        """
        # if there is no tree, then we are at the very beginning and should use the root
        if not tree:
            tree = self.root

        # if there is a leaf, then we reached the end of the tree and can return the leaf's value
        if tree.leaf_value != None:
            return tree.leaf_value

        # finding the featured value at a given branch and checking if that value is less than the forked value
        # if so, then we want the left branch
        # if not, then we want the right branch
        feature_val = dataset[tree.feature_value_index]
        if feature_val <= tree.feature_value_threshold_lte:
            return self.make_prediction(dataset, tree.left_node)
        else:
            return self.make_prediction(dataset, tree.right_node)

    def print_tree(self, tree: TreeNode = None, indent="  "):
        """A recursive method to print the tree

        Args:
            tree (TreeNode, optional): WHEN FIRST CALLING THIS SHOULD BE None !!!! Defaults to None.
            indent (str, optional): The spacing to put before the stringed value. Defaults to "  ".
        """
        # if there is no tree, then we are at the very beginning and should use the root
        if not tree:
            tree: TreeNode = self.root

        # if there is a leaf, then we reached the end of the tree and can return the leaf's value
        if tree.leaf_value is not None:
            print(tree.leaf_value)

        # printing the an indicator about which branch we are on and its threshold + variance reduction
        else:
            print(
                f"Dataset[{tree.feature_value_index}] <= {tree.feature_value_threshold_lte} ? ( Variance Reduction {tree.variance_reduction} )"
            )
            print(f"{indent}Left  : ", end="")
            self.print_tree(tree.left_node, indent + "  ")
            print(f"{indent}Right : ", end="")
            self.print_tree(tree.right_node, indent + "  ")

def main():
    # WARNING - I am not a licened doctor and this is only for entertainment purposes.
    # Please do not consult this app as medical advice. Dataset can be found here :
    # https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning
    diseases_csv = read_csv_file("DiseaseSymptoms.csv")[1:]
    np_diseases_csv = np.array(diseases_csv)[:, :-1].astype(int)

    # A depth of 25 was chosen because we have 43 rows in our csv. This means that at very least we would need 43 / 2 of a depth to capture all possible outputs
    # Because this dataset is boolean, I want to accept variances that are 0
    non_medically_licensed_doctor = DecisionTree(
        max_depth=25, require_variance_reduction_greater_than_0=False
    )
    non_medically_licensed_doctor.build_tree(np_diseases_csv)

    non_medically_licensed_doctor.print_tree()
    """
    Running the code should output something similar to this...

Dataset[90] <= 0.5 ? ( Variance Reduction 20.5 )
  Left  : Dataset[56] <= 0.5 ? ( Variance Reduction 15.47142857142856 )
    Left  : Dataset[2] <= 0.5 ? ( Variance Reduction 12.097971552257277 )
      Left  : Dataset[123] <= 0.5 ? ( Variance Reduction 13.11340679522499 )
        Left  : Dataset[112] <= 0.5 ? ( Variance Reduction 10.209375000000023 )
          Left  : Dataset[54] <= 0.5 ? ( Variance Reduction 12.721111111111085 )
            Left  : Dataset[101] <= 0.5 ? ( Variance Reduction 14.820987654321002 )
              Left  : Dataset[44] <= 0.5 ? ( Variance Reduction 16.111413043478237 )
                Left  : Dataset[120] <= 0.5 ? ( Variance Reduction 14.869908919058275 )
                  Left  : Dataset[83] <= 0.5 ? ( Variance Reduction 12.532405393649398 )
                    Left  : Dataset[131] <= 0.5 ? ( Variance Reduction 13.358171745152362 )
                      Left  : Dataset[116] <= 0.5 ? ( Variance Reduction 20.942307692307693 )
                        Left  : Dataset[23] <= 0.5 ? ( Variance Reduction 21.086605701990315 )
                          Left  : Dataset[110] <= 0.5 ? ( Variance Reduction 30.561983471074385 )
                            Left  : Dataset[45] <= 0.5 ? ( Variance Reduction 4.1984126984126995 )
                              Left  : Dataset[124] <= 0.5 ? ( Variance Reduction 4.911564625850339 )
                                Left  : Dataset[41] <= 0.5 ? ( Variance Reduction 2.7222222222222223 )
                                  Left  : Dataset[109] <= 0.5 ? ( Variance Reduction 4.083333333333334 )
                                    Left  : Dataset[82] <= 0.5 ? ( Variance Reduction 3.5555555555555554 )
                                      Left  : Dataset[122] <= 0.5 ? ( Variance Reduction 9.0 )
                                        Left  : 0.0
                                        Right : 6.0
                                      Right : 7.0
                                    Right : 9.0
                                  Right : Dataset[127] <= 0.5 ? ( Variance Reduction 1.0 )
                                    Left  : 10.0
                                    Right : 8.0
                                Right : 13.0
                              Right : Dataset[125] <= 0.5 ? ( Variance Reduction 2.25 )
                                Left  : 11.0
                                Right : 14.0
                            Right : Dataset[72] <= 0.5 ? ( Variance Reduction 49.0 )
                              Left  : 30.0
                              Right : 16.0
                          Right : Dataset[122] <= 0.5 ? ( Variance Reduction 25.0 )
                            Left  : 29.0
                            Right : 19.0
                        Right : 31.0
                      Right : Dataset[69] <= 0.5 ? ( Variance Reduction 1.96 )
                        Left  : Dataset[130] <= 0.5 ? ( Variance Reduction 0.75 )
                          Left  : 25.0
                          Right : Dataset[122] <= 0.5 ? ( Variance Reduction 0.5 )
                            Left  : 22.0
                            Right : Dataset[107] <= 0.5 ? ( Variance Reduction 0.25 )
                              Left  : 23.0
                              Right : 24.0
                        Right : 20.0
                    Right : Dataset[130] <= 0.5 ? ( Variance Reduction 0.5 )
                      Left  : Dataset[117] <= 0.5 ? ( Variance Reduction 0.25 )
                        Left  : 28.0
                        Right : 27.0
                      Right : 26.0
                  Right : 37.0
                Right : 39.0
              Right : Dataset[122] <= 0.5 ? ( Variance Reduction 98.0 )
                Left  : Dataset[103] <= 0.5 ? ( Variance Reduction 1.0 )
                  Left  : 38.0
                  Right : 40.0
                Right : 18.0
            Right : Dataset[126] <= 0.5 ? ( Variance Reduction 0.5 )
              Left  : Dataset[127] <= 0.5 ? ( Variance Reduction 0.25 )
                Left  : 34.0
                Right : 33.0
              Right : 32.0
          Right : Dataset[106] <= 0.5 ? ( Variance Reduction 0.25 )
            Left  : 35.0
            Right : 36.0
        Right : 2.0
      Right : Dataset[122] <= 0.5 ? ( Variance Reduction 20.25 )
        Left  : 12.0
        Right : 3.0
    Right : Dataset[41] <= 0.5 ? ( Variance Reduction 51.36111111111111 )
      Left  : Dataset[74] <= 0.5 ? ( Variance Reduction 2.7222222222222228 )
        Left  : Dataset[131] <= 0.5 ? ( Variance Reduction 0.25 )
          Left  : 5.0
          Right : 4.0
        Right : 1.0
      Right : Dataset[130] <= 0.5 ? ( Variance Reduction 5.555555555555555 )
        Left  : Dataset[131] <= 0.5 ? ( Variance Reduction 1.0 )
          Left  : 17.0
          Right : 15.0
        Right : 21.0
  Right : Dataset[128] <= 0.5 ? ( Variance Reduction 0.25 )
    Left  : 42.0
    Right : 41.0
    """

if __name__ == "__main__":
    main()