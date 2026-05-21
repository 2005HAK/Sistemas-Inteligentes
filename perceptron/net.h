#ifndef NET_H
#define NET_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

extern char folderEpochs;

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
void neuronRun(Neuron *n, double *inputs, int8_t wishedOutput);
double neuronComputeOutput(Neuron *n, double *inputs);
void neuronUpdateWeights(Neuron *n, double *inputs, uint8_t wishedOutput, uint8_t activated);
uint8_t neuronIsActivated(double output);
void neuronSetInputSize(Neuron *n, uint32_t newInputSize);
void neuronFree(Neuron *n);

void perceptronInit(Perceptron *p, uint16_t qtdNeurons, double learningRate, uint32_t maxEpochs);
void perceptronLoadPreset(Perceptron *p, const char *path);
void perceptronGetDataFromFile(Perceptron *p, double ***inputs, uint8_t ***wished_outputs, const char *path);
void perceptronFree(Perceptron *p);
void perceptronResetNeurons(Perceptron *p);

void shuffleIndexes(uint32_t *indexes, uint32_t size);

#endif