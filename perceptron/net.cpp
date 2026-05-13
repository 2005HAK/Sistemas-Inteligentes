#include "net.hpp"

std::string folderEpochs = "epochs";

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
		double bias = 0.0;
		std::stringstream ss(line);
		std::string temp;
		std::vector<std::string> tokens;

		while(std::getline(ss, temp, ' ')) tokens.push_back(temp);

		if(!tokens.empty()) bias = std::stod(tokens.back());

		for(size_t j = 0; j < tokens.size() - 1; j++){
			try{ weights.push_back(std::stod(tokens[j]));
			} catch(const std::exception& e) {}
		}

		if(!weights.empty()){
			this->neurons[i].set_weights(weights);
			this->neurons[i].set_bias(bias);
			this->neurons[i].setInputSize(weights.size());
			i++;
		}
	}
}

uint32_t Perceptron::getDataFromFile(std::vector<std::vector<double>>& inputs, std::vector<std::vector<uint8_t>>& wished_outputs, std::string dataPath){
	std::ifstream data(dataPath);

	if(!data.is_open()){
		std::cerr << "Error opening data file: " << dataPath << std::endl;
		return 0;
	}
	std::cout << "Loading training data from: " << dataPath << std::endl;

	std::string line;

	while(std::getline(data, line)) {
		if(line.empty()) continue;

		std::vector<double> values;
		std::stringstream ss(line);
		std::string temp;
		std::vector<std::string> tokens;

		while(std::getline(ss, temp, ',')) tokens.push_back(temp);

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

	return inputs.empty() ? 0 : inputs[0].size();
}

void Perceptron::resetNeurons(){
	for(uint16_t i = 0; i < this->qtd_neurons; i++){
		this->neurons[i].setInputSize(this->input_size);
		this->neurons[i].set_bias(0.0);
		this->neurons[i].set_weights(std::vector<double>(this->input_size, 0.0));
	}
}

uint32_t Perceptron::countClasses(std::vector<std::vector<uint8_t>>& wished_outputs){
	std::vector<std::vector<uint8_t>> unique_classes;

	for(const auto& output : wished_outputs) if(std::find(unique_classes.begin(), unique_classes.end(), output) == unique_classes.end()) unique_classes.push_back(output);

	return unique_classes.size();
}

void Perceptron::divisionDataset(std::vector<std::vector<double>>& inputs, std::vector<std::vector<uint8_t>>& wished_outputs, std::vector<std::vector<double>>& dataTrain, std::vector<std::vector<uint8_t>>& dataTrainOutputs, std::vector<std::vector<double>>& dataTest, std::vector<std::vector<uint8_t>>& dataTestOutputs, int8_t show){
	uint32_t numberOfClasses = this->countClasses(wished_outputs);

	uint32_t trainSize = (inputs.size() / numberOfClasses) * (2.0 / 3.0), testSize = (inputs.size() / numberOfClasses) - trainSize;
	uint32_t countTrain = 0, countTest = 0;

	for(uint32_t i = 0; i < inputs.size(); i++){
		if(countTrain < trainSize){
			dataTrain.push_back(inputs[i]);
			dataTrainOutputs.push_back(wished_outputs[i]);
			countTrain++;
		} else if(countTest < testSize){
			dataTest.push_back(inputs[i]);
			dataTestOutputs.push_back(wished_outputs[i]);
			countTest++;
		} else {
			countTrain = 0;
			countTest = 0;
			dataTrain.push_back(inputs[i]);
			dataTrainOutputs.push_back(wished_outputs[i]);
			countTrain++;
		}
	}
	
	if(show == 1){
		std::ofstream trainFile("train_data.txt"), testFile("test_data.txt");

		for(size_t i = 0; i < dataTrain.size(); i++){
			for(size_t j = 0; j < dataTrain[i].size(); j++) trainFile << dataTrain[i][j] << (j < dataTrain[i].size() - 1 ? "," : "");
			trainFile << ",";

			for(size_t j = 0; j < dataTrainOutputs[i].size(); j++) trainFile << static_cast<int>(dataTrainOutputs[i][j]) << (j < dataTrainOutputs[i].size() - 1 ? "," : "");
			trainFile << std::endl;
		}

		for(size_t i = 0; i < dataTest.size(); i++){
			for(size_t j = 0; j < dataTest[i].size(); j++) testFile << dataTest[i][j] << (j < dataTest[i].size() - 1 ? "," : "");
			testFile << ",";

			for(size_t j = 0; j < dataTestOutputs[i].size(); j++) testFile << static_cast<int>(dataTestOutputs[i][j]) << (j < dataTestOutputs[i].size() - 1 ? "," : "");
			testFile << std::endl;
		}
	} else if(show == 2){
		std::cout << "Training data size: " << dataTrain.size() << " samples" << std::endl;
		std::cout << "Testing data size: " << dataTest.size() << " samples" << std::endl;

		std::cout << "Data to be used for training" << std::endl;
		for(uint32_t i = 0; i < dataTrain.size(); i++){
			std::cout << "Sample " << i + 1 << ": Inputs: [";
			for(size_t j = 0; j < dataTrain[i].size(); j++){
				std::cout << dataTrain[i][j];
				if(j < dataTrain[i].size() - 1) std::cout << ", ";
			}
			std::cout << "] - Wished Output: [";
			for(size_t j = 0; j < dataTrainOutputs[i].size(); j++){
				std::cout << static_cast<int>(dataTrainOutputs[i][j]);
				if(j < dataTrainOutputs[i].size() - 1) std::cout << ", ";
			}
			std::cout << "]" << std::endl;
		}

		std::cout << "Data to be used for testing" << std::endl;
		for(uint32_t i = 0; i < dataTest.size(); i++){
			std::cout << "Sample " << i + 1 << ": Inputs: [";
			for(size_t j = 0; j < dataTest[i].size(); j++){
				std::cout << dataTest[i][j];
				if(j < dataTest[i].size() - 1) std::cout << ", ";
			}
			std::cout << "] - Wished Output: [";
			for(size_t j = 0; j < dataTestOutputs[i].size(); j++){
				std::cout << static_cast<int>(dataTestOutputs[i][j]);
				if(j < dataTestOutputs[i].size() - 1) std::cout << ", ";
			}
			std::cout << "]" << std::endl;
		}
	}
}

void Perceptron::train(std::string dataPath){
	std::vector<std::vector<double>> inputs;
	std::vector<std::vector<uint8_t>> wished_outputs;

	this->input_size = this->getDataFromFile(inputs, wished_outputs, dataPath);

	if(this->input_size == 0){
		std::cerr << "No valid training data found in: " << dataPath << std::endl;
		return;
	}

	this->resetNeurons();

	std::vector<std::vector<double>> dataTrain, dataTest;
	std::vector<std::vector<uint8_t>> dataTrainOutputs, dataTestOutputs;

	this->divisionDataset(inputs, wished_outputs, dataTrain, dataTrainOutputs, dataTest, dataTestOutputs);

	uint32_t epochs = 0;

	std::filesystem::create_directories(folderEpochs);

	while(epochs < this->max_epochs) {
		if(dataTrain.size() != dataTrainOutputs.size()){
			std::cerr << "Training data and outputs size mismatch!" << std::endl;
			return;
		}

		epochs++;

		unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
		std::shuffle(dataTrain.begin(), dataTrain.end(), std::default_random_engine(seed));
		std::shuffle(dataTrainOutputs.begin(), dataTrainOutputs.end(), std::default_random_engine(seed));

		for(uint32_t i = 0; i < dataTrain.size(); i++) for(uint16_t j = 0; j < this->qtd_neurons; j++) this->neurons[j].run(dataTrain[i], dataTrainOutputs[i][j]);

		std::vector<double> testResults = this->netTest(dataTest, dataTestOutputs);

		std::string filename = folderEpochs + "/epoch_" + std::to_string(epochs) + ".txt";
		std::ofstream file(filename);

		for(uint16_t j = 0; j < this->qtd_neurons; j++) {
			for(double w : this->neurons[j].get_weights()) file << w << " ";
			file << this->neurons[j].get_bias() << " ";
			file << std::endl;
			file << "Epoch: " << epochs << " - Accuracy: " << testResults[0] * 100.0 << "% (" << static_cast<uint32_t>(testResults[1]) << " samples)" << std::endl;
			file.close();
		}
	}
}

std::vector<double> Perceptron::netTest(std::vector<std::vector<double>>& dataTest, std::vector<std::vector<uint8_t>>& dataTestOutputs){
	uint32_t correct = 0;

	for(uint32_t i = 0; i < dataTest.size(); i++){
		std::vector<uint8_t> prediction = this->predict(dataTest[i]);
		uint32_t matchCount = 0;

		for(uint16_t j = 0; j < this->qtd_neurons; j++){
			if(prediction[j] != dataTestOutputs[i][j]) break; 
			matchCount++;
		}

		if(matchCount == this->qtd_neurons) correct++;
	}

	return std::vector<double>{static_cast<double>(correct) / static_cast<double>(dataTest.size()), static_cast<double>(dataTest.size())};
}

std::vector<uint8_t> Perceptron::predict(std::vector<double> inputs){
	std::vector<uint8_t> outputs;

	for(uint16_t i = 0; i < this->qtd_neurons; i++) outputs.push_back(this->neurons[i].run(inputs));

	return outputs;
}
