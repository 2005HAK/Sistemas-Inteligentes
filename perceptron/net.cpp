#include "net.hpp"

Neuron::Neuron(double learning_rate){
	this->input_size = 0;
	this->weights = std::vector<double>();
	this->bias = 0.0;
	this->learning_rate = learning_rate;
}

uint8_t Neuron::run(std::vector<double> inputs, int8_t wished_output){
	double output = this->compute_output(inputs);
	uint8_t activated = this->is_activated(output);

	if(wished_output != -1) this->update_weights(inputs, wished_output, activated);

	return activated;
}

double Neuron::compute_output(std::vector<double> inputs){
	double sum = this->bias;

	for(uint32_t i = 0; i < this->input_size; i++) sum += inputs[i] * this->weights[i];

	return sum;
}

void Neuron::update_weights(std::vector<double> inputs, uint8_t wished_output, uint8_t activated){
	int8_t error = wished_output - activated;

	for(uint32_t i = 0; i < this->input_size; i++) this->weights[i] += error * inputs[i] * this->learning_rate;

	this->bias += error * this->learning_rate;
}

Perceptron::Perceptron(uint16_t qtd_neurons, double learning_rate, uint32_t max_epochs){
	this->qtd_neurons = qtd_neurons;
	this->learning_rate = learning_rate;
	this->max_epochs = max_epochs;

	for(uint16_t i = 0; i < qtd_neurons; i++) this->neurons.push_back(Neuron(learning_rate));
}

void Perceptron::load_preset(std::string path){
	std::ifstream file(path);

	if(!file.is_open()){
		std::cerr << "Error opening preset file: " << path << std::endl;
		return;
	}

	std::cout << "Loading preset from: " << path << std::endl;

	std::string line;
	uint16_t i = 0;

	while(std::getline(file, line) && i < this->qtd_neurons) {
		if (line.empty()) continue;

		std::vector<double> weights;
		std::stringstream ss(line);
		std::string temp;

		while(ss >> temp){
			try{ weights.push_back(std::stod(temp));
			} catch (const std::exception& e) {}
		}

		if(!weights.empty()){
			this->neurons[i].set_weights(weights);
			this->neurons[i].setInputSize(weights.size());
			i++;
		}
	}
}

void Perceptron::train(std::string data_path){
	std::ifstream data(data_path);

	if(!data.is_open()){
		std::cerr << "Error opening data file: " << data_path << std::endl;
		return;
	}

	std::cout << "Loading training data from: " << data_path << std::endl;

	std::vector<std::vector<double>> inputs;
	std::vector<std::vector<uint8_t>> wished_outputs;

	std::string line;

	while(std::getline(data, line)) {
		if(line.empty()) continue;

		std::vector<double> values;
		std::stringstream ss(line);
		std::string temp;
		std::vector<std::string> tokens;

		while(std::getline(ss, temp, ',')) {
			tokens.push_back(temp);
		}

		if(tokens.empty()) continue;

		for(size_t i = 0; i < tokens.size() - 1; i++){
			try{ values.push_back(std::stod(tokens[i]));
			} catch(const std::exception& e) {}
		}

		if(!tokens.empty() && !values.empty()){
			try{
				uint32_t class_value = std::stoul(tokens.back());
				std::vector<uint8_t> valueOut(this->qtd_neurons, 0);
				
				for(int i = this->qtd_neurons - 1; i >= 0; i--) valueOut[i] = (class_value >> (this->qtd_neurons - 1 - i)) & 1;
				
				inputs.push_back(values);
				wished_outputs.push_back(valueOut);
			} catch(const std::exception& e){}
		}
	}

	this->input_size = inputs[0].size();

	// Sets the input size and initializes the weights
	for(uint16_t i = 0; i < this->qtd_neurons; i++) {
		this->neurons[i].setInputSize(this->input_size);
		this->neurons[i].set_weights(std::vector<double>(this->input_size, 0.0));
	}

	uint32_t epochs = 0;
	
	std::string folder_name = "epochs";
	std::filesystem::create_directories(folder_name);

	while(epochs < this->max_epochs) {
		epochs++;

		uint16_t errors_in_epoch = 0;

		unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
		std::shuffle(inputs.begin(), inputs.end(), std::default_random_engine(seed));
		std::shuffle(wished_outputs.begin(), wished_outputs.end(), std::default_random_engine(seed));

		for(uint32_t i = 0; i < inputs.size(); i++) {
			for(uint16_t j = 0; j < this->qtd_neurons; j++){
				if(wished_outputs[i][j] != this->neurons[j].run(inputs[i], wished_outputs[i][j])) {
					errors_in_epoch++;
				}
			}
		}

		std::string filename = folder_name + "/epoch_" + std::to_string(epochs) + ".txt";
		std::ofstream file(filename);
		
		for(uint16_t j = 0; j < this->qtd_neurons; j++) {
			for(double w : this->neurons[j].get_weights()) file << w << " ";
			file << this->neurons[j].get_bias() << " ";
			file << std::endl;
		}
		
		std::cout << "Epoch " << epochs << " completed. Current weights:" << std::endl;
		
		for(uint16_t j = 0; j < this->qtd_neurons; j++) {
			for(double w : this->neurons[j].get_weights()) std::cout << w << " ";
			std::cout << this->neurons[j].get_bias() << " ";
			std::cout << std::endl;
		}
		
		std::cout << "Epoch " << epochs << ": " << errors_in_epoch << " errors." << std::endl;
	}
}

void Perceptron::predict(std::vector<double> inputs){
	std::vector<uint8_t> outputs;

	for(uint16_t i = 0; i < this->qtd_neurons; i++){
		std::cout << "Neuron " << i << " weights: ";
		for(double w : this->neurons[i].get_weights()) std::cout << w << " ";
		std::cout << "bias: " << this->neurons[i].get_bias() << std::endl;
		outputs.push_back(this->neurons[i].run(inputs));
	}

	std::cout << "Predicted outputs: ";
	for(uint16_t i = 0; i < this->qtd_neurons; i++) std::cout << (int)outputs[i] << " ";
	std::cout << std::endl;
}
