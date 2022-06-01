#include "UnitConversions.h"



/**
 * @brief Converts celsius into fahrenheit
 * 
 * @param celsius
 * 
 * @return float converted to fahrenheit
 */
float Conversions::CelsiusToFahrenheit(float celsius)
{
    return celsius * 1.8 + 32;
}


/**
 * @brief Converts fahrenheit into celcius
 * 
 * @param fahrenheit
 * 
 * @return float converted to celsius
 */
float Conversions::FahrenheitToCelsius(float fahrenheit)
{
    return (fahrenheit - 32) * (5 / 9);
}


/**
 * @brief Converts meters into feet
 * 
 * @param meters
 * 
 * @return float converted to feet
 */
static float MetersToFeet(float meters)
{
    return meters * 3.28084;
}


/**
 * @brief Converts feet into meters
 * 
 * @param feet
 * 
 * @return float converted to meters
 */
static float FeetToMeters(float feet)
{
    return feet / 3.28084;
}