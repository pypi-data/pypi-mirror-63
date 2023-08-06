from numpy import array, matmul, tanh


class Phenotype:

    def __init__(self, weights, input_nodes, hidden_layers_nodes, output_nodes, use_bias):
        self.layers = []
        self.bias_layers = []

        grouped_nodes = [input_nodes] + hidden_layers_nodes + [output_nodes]
        weights_offset = 0

        for index in range(len(grouped_nodes) - 1):
            number_of_weights_per_layer = grouped_nodes[index] * grouped_nodes[index + 1]
            weights_per_layer = weights[weights_offset:weights_offset + number_of_weights_per_layer]
            weights_offset += number_of_weights_per_layer

            layer_matrix = array(weights_per_layer)
            layer_matrix = layer_matrix.reshape(grouped_nodes[index], grouped_nodes[index + 1])
            self.layers.append(layer_matrix)

        if use_bias:
            number_of_bias_weights = sum(hidden_layers_nodes) + output_nodes
            bias_weights = weights[weights_offset:weights_offset + number_of_bias_weights]

            bias_weights_offset = 0
            for units in grouped_nodes[1:]:
                selected_bias_weights = bias_weights[bias_weights_offset:bias_weights_offset + units]
                bias_weights_offset += units
                bias_matrix = array(selected_bias_weights).reshape(1, units)
                self.bias_layers.append(bias_matrix)

        self.input_nodes = input_nodes
        self.hidden_layers_nodes = hidden_layers_nodes
        self.output_nodes = output_nodes
        self.use_bias = use_bias

    @staticmethod
    def get_phenotype_from_genotype(genotype, input_nodes, hidden_layer_nodes, output_nodes, bias_weights=False):
        weights = genotype.weights
        return Phenotype(weights, input_nodes, hidden_layer_nodes, output_nodes, bias_weights)

    @staticmethod
    def get_prediction(phenotype, input_values, activation_function=tanh):
        number_of_layers = len(phenotype.hidden_layers_nodes) + 1

        result = input_values
        if phenotype.use_bias:
            for index in range(number_of_layers):
                result = activation_function(matmul(result, phenotype.layers[index]) + phenotype.bias_layers[index])

            return result
        else:
            for index in range(number_of_layers):
                result = activation_function(matmul(result, phenotype.layers[index]))

            return result
