#ifndef NET_H
#define NET_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/stat.h>

// Path to save the epochs generated during training
extern char folderEpochs[];

// Neuron functions

/**
 * @brief Structure representing a single neuron in the perceptron network
 * 
 * @var weights: An array of weights corresponding to each input
 * @var bias: The bias term for the neuron
 * @var learningRate: The learning rate used for weight updates during training
 * @var inputSize: The number of inputs the neuron expects
 */
typedef struct{
	double *weights;
	double bias;
	double learningRate;
	uint32_t inputSize;
} Neuron;

/**
 * @brief Initializes a neuron with the specified learning rate and sets its weights and bias to zero
 * 
 * @param n: A pointer to the neuron to be initialized
 * @param learningRate: The learning rate to be set for the neuron
 */
void neuronInit(Neuron *n, double learningRate);

/**
 * @brief Runs the neuron with the given inputs and updates its weights if a wished output is provided
 * 
 * @param n: A pointer to the neuron to be run
 * @param inputs: An array of input values to be fed into the neuron
 * @param wishedOutput: The desired output for the given inputs (set to -1 if no weight update is needed)
 * 
 * @return The output of the neuron after activation (1 if activated, 0 otherwise)
 */
uint8_t neuronRun(Neuron *n, double *inputs, int8_t wishedOutput);

/**
 * @brief Computes the output of the neuron before activation based on the inputs and the neuron's weights and bias
 * 
 * @param n: A pointer to the neuron for which the output is to be computed
 * @param inputs: An array of input values to be fed into the neuron
 * 
 * @return The output of the neuron before activation
 */
double neuronComputeOutput(Neuron *n, double *inputs);

/**
 * @brief Updates the weights and bias of the neuron based on the error between the wished output and the actual output
 * 
 * @param n: A pointer to the neuron to be updated
 * @param inputs: An array of input values to be fed into the neuron
 * @param wishedOutput: The desired output for the given inputs
 * @param activated: The actual output of the neuron after activation
 */
void neuronUpdateWeights(Neuron *n, double *inputs, uint8_t wishedOutput, uint8_t activated);

/**
 * @brief Determines whether the neuron is activated based on its output before activation
 * 
 * @param output: The output of the neuron before activation
 * 
 * @return 1 if the neuron is activated, 0 otherwise
 */
uint8_t neuronIsActivated(double output);

/**
 * @brief Sets the input size for the neuron and initializes its weights and bias to zero
 * 
 * @param n: A pointer to the neuron for which the input size is to be set
 * @param newInputSize: The new input size for the neuron
 */
void neuronSetInputSize(Neuron *n, uint32_t newInputSize);

/**
 * @brief Frees the memory allocated for the neuron's weights and resets its parameters
 * 
 * @param n: A pointer to the neuron to be freed
 */
void neuronFree(Neuron *n);

// End neuron functions

// Perceptron functions

/**
 * @brief Structure representing the perceptron network
 * 
 * @param neurons: An array of neurons in the network
 * @param learningRate: The learning rate used for training the network
 * @param inputSize: The number of inputs each neuron in the network expects
 * @param qtdNeurons: The number of neurons in the network
 * @param maxEpochs: The maximum number of epochs for training the network
 */
typedef struct{
	Neuron *neurons;
	double learningRate;
	uint32_t inputSize;
	uint16_t qtdNeurons;
	uint32_t maxEpochs;
} Perceptron;

/**
 * @brief Initializes the perceptron network with the specified number of neurons, learning rate, and maximum epochs for training
 * 
 * @param p: A pointer to the perceptron network to be initialized
 * @param qtdNeurons: The number of neurons to be included in the network
 * @param learningRate: The learning rate to be set for the network
 * @param maxEpochs: The maximum number of epochs for training the network
 */
void perceptronInit(Perceptron *p, uint16_t qtdNeurons, double learningRate, uint32_t maxEpochs);

/**
 * @brief Loads a preset configuration for the perceptron network from a specified file path, initializing the neurons's weights and biases accordingly
 * @param p: A pointer to the perceptron network
 * @param path: The file path from which to load the preset
 */
void perceptronLoadPreset(Perceptron *p, const char *path);

/**
 * @brief Loads training data from a specified file path, extracting the input features and corresponding wished outputs, and counts the number of unique 
 *        classes in the dataset
 * 
 * @param p: A pointer to the perceptron network
 * @param inputs: A pointer to a matrix that will be allocated and filled with the input features from the dataset
 * @param wishedOutputs: A pointer to a matrix that will be allocated and filled with the wished output labels corresponding to the input features
 * @param path: The file path from which to load the training data
 * @param countClasses: A pointer to a variable that will be set to the number of unique classes found in the dataset
 * @param dataSize: A pointer to a variable that will be set to the total number of data samples loaded from the file
 * 
 * @return The size of inputs. If the function fails to load data, it returns 0.
 */
uint32_t perceptronGetDataFromFile(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, const char *path, uint32_t *countClasses, uint32_t *dataSize);

/**
 * @brief Divides the dataset into training and testing sets.
 * 
 * @param p: A pointer to the perceptron network
 * @param inputs: A pointer to the matrix containing the input features of the dataset
 * @param wishedOutputs: A pointer to the matrix containing the wished output labels corresponding to the input features
 * @param trainIndexes: A pointer to an array that will be allocated and filled with the indexes of the samples selected for training
 * @param testIndexes: A pointer to an array that will be allocated and filled with the indexes of the samples selected for testing
 * @param countClasses: A pointer to a variable containing the number of unique classes in the dataset
 * @param dataSize: A pointer to a variable containing the total number of data samples in the dataset
 * @param show: A flag indicating whether to display the divided data (0 for no display, 1 for saving to files, 2 for printing to console)
 */
void perceptronDivisionDataSet(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t **trainIndexes, uint32_t **testIndexes, uint32_t *countClasses, uint32_t *dataSize, uint8_t show);

/**
 * @brief Trains the perceptron network using the training data loaded from a specified file path, iterating through epochs and updating the neurons's
 *        weights based on the training samples, while also evaluating the network's accuracy on a test set after each epoch
 * 
 * @param p: A pointer to the perceptron network to be trained
 * @param path: The file path from which to load the training data
 */
void perceptronTrain(Perceptron *p, const char *path);

/**
 * @brief Tests the perceptron network using a specified test set, calculating the accuracy of the network's predictions compared to the wished outputs
 * 
 * @param p: A pointer to the perceptron network to be tested
 * @param inputs: A pointer to the matrix containing the input features of the test set
 * @param wishedOutputs: A pointer to the matrix containing the wished output labels corresponding to the input features of the test set
 * @param testIndexes: An array containing the indexes of the samples in the test set
 * @param testDataSize: The total number of samples in the test set
 * 
 * @return The accuracy of the perceptron network on the test set, represented as a value between 0 and 1
 */
double perceptronNetTest(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t *testIndexes, uint32_t testDataSize);

/**
 * @brief Predicts the output of the perceptron network for a given set of input features, returning an array of predicted class labels based on the 
 *        activation of the neurons
 * 
 * @param p: A pointer to the perceptron network to be used for prediction
 * @param inputs: An array of input features for which to predict the output class labels
 * 
 * @return An array of predicted class labels corresponding to the input features, where each element represents the predicted class for a neuron in the network
 */
uint8_t *perceptronPredict(Perceptron *p, double *inputs);

/**
 * @brief Resets the weights and biases of all neurons in the perceptron network to zero, effectively reinitializing the network for training
 * 
 * @param p: A pointer to the perceptron network to be reset
 */
void perceptronResetNeurons(Perceptron *p);

/**
 * @brief Frees the memory allocated for the perceptron network's neurons and resets its parameters
 * 
 * @param p: A pointer to the perceptron network to be freed
 */
void perceptronFree(Perceptron *p);

// End perceptron functions

// Utility functions

/**
 * @brief Shuffles an array of indexes
 * 
 * @param indexes: An array of indexes to be shuffled
 * @param size: The size of the indexes array
 */
void shuffleIndexes(uint32_t *indexes, uint32_t size);

#endif