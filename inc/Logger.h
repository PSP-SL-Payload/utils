#ifndef LOGGER_H
#define LOGGER_H
#include <Arduino.h>

#define LOG_INFO_MSG  "[INFO]    "
#define LOG_WARN_MSG  "[WARNING] "
#define LOG_ERR_MSG   "[ERROR]   "
#define LOG_DEBUG_MSG "[DEBUG]   "

/**
 * @brief The logging class for printing statements. This is used to unify and standardize print statements.
 * 
 */
class Logger
{
public:
    enum LogLevel
    {
        LOG_INFO =  0,
        LOG_WARN =  1,
        LOG_ERR =   2,
        LOG_DEBUG = 3
    };

    struct LogTimeStruct
    {
        uint8_t  hour;
        uint8_t  minute;
        uint8_t  second;
        uint16_t millisecond;
    };

    static void Print(char* string, LogLevel logLevel = LOG_INFO, const LogTimeStruct* timeToLog = nullptr, bool shouldHaveNewLine = true);

private:

};

#endif