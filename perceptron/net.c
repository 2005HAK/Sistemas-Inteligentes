#include "net.h"

char folderEpochs[] = "epochs";

// Neuron functions

void neuronInit(Neuron *n, double learningRate){
	n->inputSize = 0;
	n->weights = NULL;
	n->bias = 0.0;
	n->learningRate = learningRate;
}

void neuronRun(Neuron *n, double *inputs, int8_t wishedOutput){
	double output = neuronComputeOutput(n, inputs);
	uint8_t activated = neuronIsActivated(output);

	if(wishedOutput != -1) neuronUpdateWeights(n, inputs, wishedOutput, activated);

	return activated;
}

double neuronComputeOutput(Neuron *n, double *inputs){
	double sum = n->bias;

	for(uint32_t i = 0; i < n->inputSize; i++) sum += inputs[i] * n->weights[i];

	return sum;
}

void neuronUpdateWeights(Neuron *n, double *inputs, uint8_t wishedOutput, uint8_t activated){
	int8_t error = wishedOutput - activated;

	for(uint32_t i = 0; i < n->inputSize; i++) n->weights[i] += error * inputs[i] * n->learningRate;

	n->bias += error * n->learningRate;
}

uint8_t neuronIsActivated(double output){
	return output >= 0.0 ? 1 : 0;
}

void neuronSetInputSize(Neuron *n, uint32_t newInputSize){
	n->inputSize = newInputSize;
	n->weights = (double*)realloc(n->weights, newInputSize * sizeof(double));

	for(uint32_t i = 0; i < newInputSize; i++) n->weights[i] = 0.0;
}

void neuronFree(Neuron *n){
	if(n->weights) free(n->weights);
	n->weights = NULL;
	n->inputSize = 0;
}

// End neuron functions

void perceptronInit(Perceptron *p, uint16_t qtdNeurons, double learningRate, uint32_t maxEpochs){
	p->qtd_neurons = qtdNeurons;
	p->learning_rate = learningRate;
	p->max_epochs = maxEpochs;
	p->input_size = 0;
	p->neurons = (Neuron*)malloc(qtdNeurons * sizeof(Neuron));

	for(uint16_t i = 0; i < qtdNeurons; i++) neuronInit(&p->neurons[i], learningRate);
}

void perceptronLoadPreset(Perceptron *p, const char *path){
	FILE *file = fopen(path, "r");
	if(!file){
		fprintf(stderr, "Error opening preset file: %s\n", path);
		return;
	}

	printf("Loading preset from: %s\n", path);

	char line[1024];
	uint16_t i = 0;

	while(fgets(line, sizeof(line), file) && i < p->qtdNeurons){
		if(line[0] == '\n') continue;
		
		double *weights = (double*)malloc(p->inputSize * sizeof(double));
		double bias = 0.0;
		char *token = strtok(line, ' ');

		for(uint32_t i = 0; i < p->inputSize; i++){
			if(token) weights[i] = atof(token);
			else weights[i] = 0.0;

			if(i == p->inputSize - 1) {
				token = strtok(NULL, '\n');
				if(token) bias = atof(token);
				else bias = 0.0;
			}
			
			token = strtok(NULL, ' ');
		}

		if(weights){
			p->neurons[i].weights = weights;
			p->neurons[i].bias = bias;
			neuronSetInputSize(&p->neurons[i], p->inputSize);
			i++;
		}
	}

	fclose(file);

	printf("Preset loaded successfully.\n");
}

void perceptronGetDataFromFile(Perceptron *p, double ***inputs, uint8_t ***wished_outputs, const char *path){
	FILE *data = fopen(path, "r");

	if(!data){
		fprintf(stderr, "Error opening data file: %s\n", path);
		return;
	}

	printf("Loading training data from: %s\n", path);

	char line[1024];

	while(fgets(line, sizeof(line), data)){
		if(line[0] == '\n') continue;

		double *values;
		char *token = strtok(line, ',');
		uint32_t inputCount = 0;

		do{
			inputCount++;
			values = (double*)realloc(values, inputCount * sizeof(double));
			if(token) values[inputCount - 1] = atof(token);
			else values[inputCount - 1] = 0.0;

			token = strtok(NULL, ',');
		} while(token);

		
	}
}

void perceptronFree(Perceptron *p){
	for(uint16_t i = 0; i < p->qtdNeurons; i++) neuronFree(&p->neurons[i]);
	free(p->neurons);
	p->neurons = NULL;
	p->inputSize = 0;
	p->qtdNeurons = 0;
}

void perceptronResetNeurons(Perceptron *p){
	for(uint16_t i = 0; i < p->qtdNeurons; i++){
		neuronSetInputSize(&p->neurons[i], p->inputSize);
		p->neurons[i].bias = 0.0;
		for(uint32_t j = 0; j < p->inputSize; j++) p->neurons[i].weights[j] = 0.0;
	}
}

void shuffleIndexes(uint32_t *indexes, uint32_t size){
	if (size <= 1) return;
	for(uint32_t i = size - 1; i > 0; i--){
		uint32_t j = rand() % (i + 1);
		uint32_t temp = indexes[i];
		indexes[i] = indexes[j];
		indexes[j] = temp;
	}
}