#include "net.hpp"

std::string presetPath = "";
std::string dataPath = "iris/bezdekIris.txt";

int main(){
	Perceptron p(1, 0.5, 100);

	p.train(dataPath);

	//for(uint16_t i = 0; i < inputs.size(); i++) p.train(inputs[i], wished_outputs[i]);

	p.predict({1.2247,8.7779,-2.2135,-0.80647});

	return 0;
}