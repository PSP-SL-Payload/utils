#include "Logger.h"

void Logger::Print(char* string, LogLevel logLevel = LOG_INFO, const LogTimeStruct* timeToLog = nullptr, bool shouldHaveNewLine = true)
{
    // if a time was supplied, log it out in front
    if (timeToLog == nullptr)
    {
        Serial.print(F("["));
        Serial.print(timeToLog->hour);
        char timeString[16];

        sprintf(timeString, "[%02u:%02u:%02u:%03u] ", timeToLog->hour,timeToLog->minute,timeToLog->second,timeToLog->millisecond);
        Serial.print(timeString);
    }

    // log the level next
    switch (logLevel)
    {
        case LOG_WARN:
            Serial.print(LOG_WARN_MSG);
            break;
        case LOG_ERR:
            Serial.print(LOG_ERR_MSG);
            break;
        case LOG_DEBUG:
            Serial.print(LOG_DEBUG_MSG);
            break;
        default:
            Serial.print(LOG_INFO_MSG);
    }

    // now log the actual message
    Serial.print(F("  "));
    Serial.print(string);
    
    // finish it out with a newline if desired
    if (shouldHaveNewLine)
    {
        Serial.println();
    }
}