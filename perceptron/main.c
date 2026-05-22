#include "net.h"

char presetPath[] = "";
//char dataPath[] = "data/2ddatabase.txt";
char dataPath[] = "data/iris.data";

int main(){
	srand(time(NULL));

	Perceptron p;
	perceptronInit(&p, 1, 0.65, 100);

	perceptronTrain(&p, dataPath);

	return 0;
}