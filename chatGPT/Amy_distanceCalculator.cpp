#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>

using namespace std;

bool getInputAndValidate(double coords[2][2]);
void calculateSlope(double coords[2][2]);
void calculateManhattanDistance(double coords[2][2]);
void calculateEuclideanDistance(double coords[2][2]);

int main() {
    double coords[2][2];
    char option;
    bool validInput;

    cout << "***************************************" << endl;
    cout << "* Welcome to the Distance Calculator *" << endl;
    cout << "***************************************" << endl;
    cout << "Slope - (s/S)" << endl;
    cout << "Manhattan Distance - (m/M)" << endl;
    cout << "Euclidean Distance - (e/E)" << endl;
    cout << "Quit - (q/Q)" << endl;

    // User selects which calculation they want
    cout << "Enter an Option: ";
    cin >> option;

    // Sets outputs to 3 decimals
    cout << fixed << setprecision(3);

    // Validate and get input
    validInput = getInputAndValidate(coords);
    if (!validInput) {
        cout << "Error: Invalid input" << endl;
        return 0;
    }

    // Processing based on user option
    switch (option) {
        case 's':
        case 'S':
            calculateSlope(coords);
            break;
        case 'm':
        case 'M':
            calculateManhattanDistance(coords);
            break;
        case 'e':
        case 'E':
            calculateEuclideanDistance(coords);
            break;
        case 'q':
        case 'Q':
            cout << "Thank you for using the Distance Calculator" << endl;
            break;
        default:
            cout << "Error: Invalid selection" << endl;
    }

    return 0;
}

bool getInputAndValidate(double coords[2][2]) {
    for (int i = 0; i < 2; ++i) {
        cout << "Enter x" << i + 1 << " value: ";
        cin >> coords[i][0];
        if (coords[i][0] > 100 || !cin) {
            return false;
        }

        cout << "Enter y" << i + 1 << " value: ";
        cin >> coords[i][1];
        if (coords[i][1] > 150 || !cin) {
            return false;
        }
    }
    return true;
}

void calculateSlope(double coords[2][2]) {
    double slope, yInt;
    if (coords[1][0] == coords[0][0]) {
        cout << "Error: Division by zero, x1 cannot be equal to x2 for slope calculation." << endl;
        return;
    }
    slope = (coords[1][1] - coords[0][1]) / (coords[1][0] - coords[0][0]);
    yInt = coords[0][1] - (slope * coords[0][0]);
    cout << "Slope: " << slope << endl;
    cout << "Y-intercept: " << yInt << endl;
}

void calculateManhattanDistance(double coords[2][2]) {
    double manDist = abs(coords[1][0] - coords[0][0]) + abs(coords[1][1] - coords[0][1]);
    cout << "Manhattan Distance: " << manDist << endl;
}

void calculateEuclideanDistance(double coords[2][2]) {
    double eucDist = sqrt((coords[1][0] - coords[0][0]) * (coords[1][0] - coords[0][0]) + (coords[1][1] - coords[0][1]) * (coords[1][1] - coords[0][1]));
    cout << "Euclidean Distance: " << eucDist << endl;
}
