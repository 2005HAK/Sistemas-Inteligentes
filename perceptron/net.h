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

typedef struct{
	double *weights;
	double bias;
	double learningRate;
	uint32_t inputSize;
} Neuron;


typedef struct{
	Neuron *neurons;
	double learningRate;
	uint32_t inputSize;
	uint16_t qtdNeurons;
	uint32_t maxEpochs;
} Perceptron;

void neuronInit(Neuron *n, double learningRate);
uint8_t neuronRun(Neuron *n, double *inputs, int8_t wishedOutput);
double neuronComputeOutput(Neuron *n, double *inputs);
void neuronUpdateWeights(Neuron *n, double *inputs, uint8_t wishedOutput, uint8_t activated);
uint8_t neuronIsActivated(double output);
void neuronSetInputSize(Neuron *n, uint32_t newInputSize);
void neuronFree(Neuron *n);

void perceptronInit(Perceptron *p, uint16_t qtdNeurons, double learningRate, uint32_t maxEpochs);
void perceptronLoadPreset(Perceptron *p, const char *path);
uint32_t perceptronGetDataFromFile(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, const char *path, uint32_t *countClasses, uint32_t *dataSize);
void perceptronResetNeurons(Perceptron *p);
void perceptronDivisionDataSet(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t **trainIndexes, uint32_t **testIndexes, uint32_t *countClasses, uint32_t *dataSize, uint8_t show);
void perceptronTrain(Perceptron *p, const char *path);
double perceptronNetTest(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t *testIndexes, uint32_t testDataSize);
uint8_t *perceptronPredict(Perceptron *p, double *inputs);
void perceptronFree(Perceptron *p);

void shuffleIndexes(uint32_t *indexes, uint32_t size);

#endif