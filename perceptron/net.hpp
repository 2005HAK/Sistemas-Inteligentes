#include <iostream>
#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <random>
#include <chrono>
#include <algorithm>
#include <filesystem>

extern std::string folderEpochs;

class Neuron {
	private:
		std::vector<double> weights;
		double bias;
		double learning_rate;
		uint32_t input_size;

	public:
		Neuron(double learning_rate);

		uint8_t run(std::vector<double> inputs, int8_t wished_output = -1);

		double compute_output(std::vector<double> inputs);

		uint8_t is_activated(double output){ return output >= 0.0 ? 1 : 0; }

		void update_weights(std::vector<double> inputs, uint8_t wished_output, uint8_t activated);

		std::vector<double> get_weights() const { return this->weights; }

		double get_bias() const { return this->bias; }

		void set_bias(double new_bias) { this->bias = new_bias; }

		void set_weights(std::vector<double> new_weights) { this->weights = new_weights; }

		void setInputSize(uint32_t new_input_size) { this->input_size = new_input_size; }
};

class Perceptron{
	private:
		std::vector<Neuron> neurons;
		double learning_rate;
		uint32_t input_size;
		uint16_t qtd_neurons;
		uint32_t max_epochs;

	public:
		Perceptron(uint16_t qtd_neurons, double learning_rate, uint32_t max_epochs = 100);

		void load_preset(std::string path);

		uint32_t getDataFromFile(std::vector<std::vector<double>>& inputs, std::vector<std::vector<uint8_t>>& wished_outputs, std::string dataPath);

		void resetNeurons();

		uint32_t countClasses(std::vector<std::vector<uint8_t>>& wished_outputs);

		void divisionDataset(std::vector<std::vector<double>>& inputs, std::vector<std::vector<uint8_t>>& wished_outputs, std::vector<std::vector<double>>& trainData, std::vector<std::vector<uint8_t>>& trainOutputs, std::vector<std::vector<double>>& testData, std::vector<std::vector<uint8_t>>& testOutputs, int8_t show = 0);

		void train(std::string dataPath);

		std::vector<double> netTest(std::vector<std::vector<double>>& dataTest, std::vector<std::vector<uint8_t>>& dataTestOutputs);

		std::vector<uint8_t> predict(std::vector<double> inputs);
};