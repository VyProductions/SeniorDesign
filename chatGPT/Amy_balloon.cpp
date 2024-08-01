#include <iostream>

using namespace std;

/**
 * The Balloon class represents a generic balloon in the program.
 * It contains static members to track the total points, points per balloon,
 * points multiplier, and the total count of balloons.
 * The class serves as a base class for specific types of balloons and
 * defines virtual methods for getting the identifier of the balloon.
 */
class Balloon
{
protected:
    static float PointsPerBalloon;  // Points awarded per balloon
    static float PointsMultiplier;  // Multiplier applied to the points
    static float PointsTotal;       // Total points accumulated
    static int BalloonCount;        // Total count of balloon instances

public:
    Balloon();  // Constructor to initialize the balloon
    virtual ~Balloon() = 0;  // Pure virtual destructor
    static int GetBalloonCount();  // Returns the total number of balloons
    static float GetPointTotal();  // Returns the total points accumulated
    virtual char GetIdentifier() const;  // Returns the identifier of the balloon
};

/**
 * The RedBalloon class represents a specific type of balloon with a unique identifier 'R'.
 * It inherits from the Balloon class and overrides the GetIdentifier method.
 * The destructor increases the points multiplier when a RedBalloon instance is destroyed.
 */
class RedBalloon : public Balloon
{
public:
    virtual char GetIdentifier() const;  // Returns the identifier 'R' for RedBalloon
    ~RedBalloon();  // Destructor for RedBalloon
};

/**
 * The BlueBalloon class represents a specific type of balloon with a unique identifier 'B'.
 * It inherits from the Balloon class and overrides the GetIdentifier method.
 * The destructor increases the points per balloon when a BlueBalloon instance is destroyed.
 */
class BlueBalloon : public Balloon
{
public:
    virtual char GetIdentifier() const;  // Returns the identifier 'B' for BlueBalloon
    ~BlueBalloon();  // Destructor for BlueBalloon
};

/**
 * The YellowBalloon class represents a specific type of balloon with a unique identifier 'Y'.
 * It inherits from the Balloon class and overrides the GetIdentifier method.
 * The destructor provides a specific message when a YellowBalloon instance is destroyed.
 */
class YellowBalloon : public Balloon
{
public:
    virtual char GetIdentifier() const;  // Returns the identifier 'Y' for YellowBalloon
    ~YellowBalloon();  // Destructor for YellowBalloon
};

// Initialize static variables.
float Balloon::PointsPerBalloon = 1.0;
float Balloon::PointsMultiplier = 1.0;
float Balloon::PointsTotal = 1.0;
int Balloon::BalloonCount = 0;

/**
 * Constructor for the Balloon class.
 * Increments the total balloon count when a new balloon instance is created.
 */
Balloon::Balloon()
{
    BalloonCount++;
}

/**
 * Destructor for the Balloon class.
 * Decrements the total balloon count when a balloon instance is destroyed.
 * Updates the total points based on the points per balloon and the points multiplier.
 */
Balloon::~Balloon()
{
    BalloonCount--;
    PointsTotal = PointsPerBalloon * PointsMultiplier;
}

/**
 * Returns the total number of balloon instances.
 */
int Balloon::GetBalloonCount()
{
    return BalloonCount;
}

/**
 * Returns the total points accumulated from all balloons.
 */
float Balloon::GetPointTotal()
{
    return PointsTotal;
}

/**
 * Returns the identifier of the balloon.
 * This is a virtual method and should be overridden by derived classes.
 */
char Balloon::GetIdentifier() const
{
    return '\0';  // Default identifier (null character)
}

/**
 * Returns the identifier 'R' for RedBalloon.
 */
char RedBalloon::GetIdentifier() const
{
    return 'R';
}

/**
 * Destructor for RedBalloon.
 * Increases the points multiplier by 0.1 and prints a pop message.
 */
RedBalloon::~RedBalloon()
{
    PointsMultiplier = PointsMultiplier + 0.1;
    cout << " Red Balloon - *POP* " << endl;
}

/**
 * Returns the identifier 'B' for BlueBalloon.
 */
char BlueBalloon::GetIdentifier() const
{
    return 'B';
}

/**
 * Destructor for BlueBalloon.
 * Increases the points per balloon by 0.1 and prints a pop message.
 */
BlueBalloon::~BlueBalloon()
{
    PointsPerBalloon = PointsPerBalloon + 0.1;
    cout << " Blue Balloon - *POP* " << endl;
}

/**
 * Returns the identifier 'Y' for YellowBalloon.
 */
char YellowBalloon::GetIdentifier() const
{
    return 'Y';
}

/**
 * Destructor for YellowBalloon.
 * Prints a pop message specific to YellowBalloon.
 */
YellowBalloon::~YellowBalloon()
{
    cout << " Yellow Balloon - *POP* " << endl;
}
