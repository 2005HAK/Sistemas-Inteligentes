#include "net.h"

char folderEpochs[] = "epochs";

// Neuron functions

void neuronInit(Neuron *n, double learningRate){
	n->inputSize = 0;
	n->weights = NULL;
	n->bias = 0.0;
	n->learningRate = learningRate;
}

uint8_t neuronRun(Neuron *n, double *inputs, int8_t wishedOutput){
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
	n->bias = 0.0;
}

void neuronFree(Neuron *n){
	if(n->weights) free(n->weights);
	n->weights = NULL;
	n->inputSize = 0;
}

// End neuron functions

// Perceptron functions

void perceptronInit(Perceptron *p, uint16_t qtdNeurons, double learningRate, uint32_t maxEpochs){
	p->qtdNeurons = qtdNeurons;
	p->learningRate = learningRate;
	p->maxEpochs = maxEpochs;
	p->inputSize = 0;
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
		char *token = strtok(line, " ");

		for(uint32_t i = 0; i < p->inputSize; i++){
			if(token) weights[i] = atof(token);
			else weights[i] = 0.0;

			if(i == p->inputSize - 1) {
				token = strtok(NULL, "\n");
				if(token) bias = atof(token);
				else bias = 0.0;
			}
			
			token = strtok(NULL, " ");
		}

		if(weights){
			p->neurons[i].weights = weights;
			p->neurons[i].bias = bias;
			p->neurons[i].inputSize = p->inputSize;
			i++;
		}
	}

	fclose(file);

	printf("Preset loaded successfully.\n");
}

uint32_t perceptronGetDataFromFile(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, const char *path, uint32_t *countClasses, uint32_t *dataSize){
	FILE *data = fopen(path, "r");

	if(!data){
		fprintf(stderr, "Error opening data file: %s\n", path);
		return 0;
	}

	printf("Loading training data from: %s\n", path);

	char line[1024];
	uint32_t dataCount = 0;
	uint8_t *uniqueClasses = NULL;
	uint32_t inputCount = 0;

	while(fgets(line, sizeof(line), data)){
		if(line[0] == '\n') continue;

		dataCount++;
		double *values = NULL;
		char *token = strtok(line, ",");
		inputCount = 0;

		do{
			inputCount++;
			values = (double*)realloc(values, inputCount * sizeof(double));
			if(token) values[inputCount - 1] = atof(token);
			else values[inputCount - 1] = 0.0;

			token = strtok(NULL, ",");
		} while(token);
		
		if(values){
			uint32_t classValue = (uint32_t)values[inputCount - 1];

			if(!uniqueClasses){
				uniqueClasses = (uint8_t*)malloc(sizeof(uint8_t));
				uniqueClasses[*countClasses] = classValue;
				(*countClasses)++;
			} else {
				uint8_t isUnique = 1;

				for(uint32_t j = 0; j < *countClasses; j++){
					if(uniqueClasses[j] == classValue) {
						isUnique = 0;
						break;
					}
				}

				if(isUnique){
					uniqueClasses = (uint8_t*)realloc(uniqueClasses, ((*countClasses) + 1) * sizeof(uint8_t));
					uniqueClasses[*countClasses] = classValue;
					(*countClasses)++;
				}
			}

			values = (double*)realloc(values, (inputCount - 1) * sizeof(double));

			uint8_t *valueOut = (uint8_t*)malloc(p->qtdNeurons * sizeof(uint8_t));

			for(uint16_t i = 0; i < p->qtdNeurons; i++) valueOut[i] = (classValue >> (p->qtdNeurons - 1 - i)) & 1;

			*inputs = (double**)realloc(*inputs, dataCount * sizeof(double*));
			(*inputs)[dataCount - 1] = values;
			*wishedOutputs = (uint8_t**)realloc(*wishedOutputs, dataCount * sizeof(uint8_t*));
			(*wishedOutputs)[dataCount - 1] = valueOut;
		}
	}

	free(uniqueClasses);

	*dataSize = dataCount;
	return inputCount - 1;
}

void perceptronDivisionDataSet(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t **trainIndexes, uint32_t **testIndexes, uint32_t *countClasses, uint32_t *dataSize, uint8_t show){
	uint32_t trainSize = ((*dataSize) / (*countClasses)) * (2.0 / 3.0), testSize = ((*dataSize) / (*countClasses)) - trainSize;
	uint32_t countTrain = 0, countTest = 0, indexTrain = 0, indexTest = 0;

	for(uint32_t i = 0; i < (*dataSize); i++){
		if(countTrain < trainSize){
			*trainIndexes = (uint32_t*)realloc(*trainIndexes, (indexTrain + 1) * sizeof(uint32_t));
			(*trainIndexes)[indexTrain] = i;
			countTrain++;
			indexTrain++;
		} else if(countTest < testSize){
			*testIndexes = (uint32_t*)realloc(*testIndexes, (indexTest + 1) * sizeof(uint32_t));
			(*testIndexes)[indexTest] = i;
			countTest++;
			indexTest++;
		} else{
			countTrain = 0;
			countTest = 0;
			*trainIndexes = (uint32_t*)realloc(*trainIndexes, (indexTrain + 1) * sizeof(uint32_t));
			(*trainIndexes)[indexTrain] = i;
			indexTrain++;
		}
	}

	if(show == 1){
		FILE *trainFile = fopen("train_data.txt", "w"), *testFile = fopen("test_data.txt", "w");

		for(uint32_t i = 0; i < indexTrain; i++){
			for(uint32_t j = 0; j < p->inputSize; j++){
				fprintf(trainFile, "%.2f ", (*inputs)[(*trainIndexes)[i]][j]);
				fprintf(trainFile, j < p->inputSize - 1 ? "," : "; ");
			}
			for(uint32_t j = 0; j < p->qtdNeurons; j++){
				fprintf(trainFile, "%d ", (*wishedOutputs)[(*trainIndexes)[i]][j]);
				fprintf(trainFile, j < p->qtdNeurons - 1 ? "," : ";");
			}
			fprintf(trainFile, "\n");
		}

		for(uint32_t i = 0; i < indexTest; i++){
			for(uint32_t j = 0; j < p->inputSize; j++){
				fprintf(testFile, "%.2f ", (*inputs)[(*testIndexes)[i]][j]);
				fprintf(testFile, j < p->inputSize - 1 ? "," : "; ");
			}
			for(uint32_t j = 0; j < p->qtdNeurons; j++){
				fprintf(testFile, "%d ", (*wishedOutputs)[(*testIndexes)[i]][j]);
				fprintf(testFile, j < p->qtdNeurons - 1 ? "," : ";\n");
			}
		}

		fclose(trainFile);
		fclose(testFile);
	} else if(show == 2){
		printf("Training data size: %d samples\n", trainSize);
		printf("Test data size: %d samples\n", testSize);
		
		printf("Data to be used for training:\n");
		for(uint32_t i = 0; i < indexTrain; i++){
			printf("Sample %d: Inputs: [", i + 1);
			for(uint32_t j = 0; j < p->inputSize; j++){
				printf("%.2f ", (*inputs)[(*trainIndexes)[i]][j]);
				printf(j < p->inputSize - 1 ? ", " : "]");
			}

			printf(" - Wished Outputs: [");

			for(uint32_t j = 0; j < p->qtdNeurons; j++){
				printf("%d ", (*wishedOutputs)[(*trainIndexes)[i]][j]);
				printf(j < p->qtdNeurons - 1 ? ", " : "]\n");
			}
		}

		printf("Data to be used for testing:\n");
		for(uint32_t i = 0; i < indexTest; i++){
			for(uint32_t j = 0; j < p->inputSize; j++){
				printf("%.2f ", (*inputs)[(*testIndexes)[i]][j]);
				printf(j < p->inputSize - 1 ? ", " : "]");
			}
			printf(" - Wished Outputs: [");
			for(uint32_t j = 0; j < p->qtdNeurons; j++){
				printf("%d ", (*wishedOutputs)[(*testIndexes)[i]][j]);
				printf(j < p->qtdNeurons - 1 ? ", " : "]\n");
			}
		}
	}

}

void perceptronTrain(Perceptron *p, const char *path){
	double **inputs = NULL;
	uint8_t **wishedOutputs = NULL;
	uint32_t countClasses = 0, dataSize = 0, epochs = 0;

	p->inputSize = perceptronGetDataFromFile(p, &inputs, &wishedOutputs, path, &countClasses, &dataSize);

	if(p->inputSize == 0){
		fprintf(stderr, "Error: Failed to load data from file %s\n", path);
		return;
	}

	perceptronResetNeurons(p);

	uint32_t *trainIndexes = NULL, *testIndexes = NULL;

	perceptronDivisionDataSet(p, &inputs, &wishedOutputs, &trainIndexes, &testIndexes, &countClasses, &dataSize, 0);

	mkdir(folderEpochs, 0755);

	while(epochs < p->maxEpochs){
		if(!inputs || !wishedOutputs) {
			fprintf(stderr, "Error: Failed to initialize training data\n");
			return;
		}

		epochs++;

		shuffleIndexes(trainIndexes, dataSize * (2.0 / 3.0));

		for(uint32_t i = 0; i < dataSize * (2.0 / 3.0); i++) for(uint32_t j = 0; j < p->qtdNeurons; j++) neuronRun(&p->neurons[j], inputs[trainIndexes[i]], wishedOutputs[trainIndexes[i]][j]);

		double accuracy = perceptronNetTest(p, &inputs, &wishedOutputs, testIndexes, dataSize * (1.0 / 3.0));

		char epochFilename[256];
		snprintf(epochFilename, sizeof(epochFilename), "%s/epoch_%d.txt", folderEpochs, epochs);
		FILE *epochFile = fopen(epochFilename, "w");
		if(epochFile){
			for(uint16_t i = 0; i < p->qtdNeurons; i++){
				for(uint32_t j = 0; j < p->inputSize; j++){
					fprintf(epochFile, "%.2f ", p->neurons[i].weights[j]);
				}
				fprintf(epochFile, "%.2f\n", p->neurons[i].bias);
				fprintf(stderr, "Epoch: %d - Accuracy: %.2f%% (%d samples)\n", epochs, accuracy * 100, (int)(dataSize * (1.0 / 3.0)));
			}
			fclose(epochFile);
		}
	}
}

double perceptronNetTest(Perceptron *p, double ***inputs, uint8_t ***wishedOutputs, uint32_t *testIndexes, uint32_t testDataSize){
	uint32_t correct = 0;

	for(uint32_t i = 0; i < testDataSize; i++){
		uint8_t *prediction = perceptronPredict(p, (*inputs)[testIndexes[i]]);
		uint32_t matchCount = 0;

		for(uint16_t j = 0; j < p->qtdNeurons; j++){
			if(prediction[j] != (*wishedOutputs)[testIndexes[i]][j]) break;
			matchCount++;
		}
		free(prediction);
		if(matchCount == p->qtdNeurons) correct++;
	}

	return (double)correct / testDataSize;
}

uint8_t *perceptronPredict(Perceptron *p, double *inputs){
	uint8_t *outputs = (uint8_t *)malloc(p->qtdNeurons * sizeof(uint8_t));
	if(!outputs) return NULL;

	for(uint16_t i = 0; i < p->qtdNeurons; i++){
		uint8_t output = neuronRun(&p->neurons[i], inputs, -1);
		outputs[i] = output;
	}

	return outputs;
}

void perceptronResetNeurons(Perceptron *p){
	for(uint16_t i = 0; i < p->qtdNeurons; i++) neuronSetInputSize(&p->neurons[i], p->inputSize);
}

void perceptronFree(Perceptron *p){
	for(uint16_t i = 0; i < p->qtdNeurons; i++) neuronFree(&p->neurons[i]);
	free(p->neurons);
	p->neurons = NULL;
	p->inputSize = 0;
	p->qtdNeurons = 0;
}


// End perceptron functions

void shuffleIndexes(uint32_t *indexes, uint32_t size){
	if (size <= 1) return;
	for(uint32_t i = size - 1; i > 0; i--){
		uint32_t j = rand() % (i + 1);
		uint32_t temp = indexes[i];
		indexes[i] = indexes[j];
		indexes[j] = temp;
	}
}