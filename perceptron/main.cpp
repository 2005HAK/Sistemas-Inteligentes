
#include "net.hpp"

std::string presetPath = "";
std::string dataPath = "2ddatabase.txt";

int main(){
	Perceptron p(1, 0.5, 5);

	//load_preset("epochs/epoch_5.txt");

	p.train(dataPath);

	//std::cout << "Predicted output: " << (int)(p.predict({2.8, 1.9}))[0] << std::endl;

	return 0;
}