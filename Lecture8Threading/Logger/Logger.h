#ifndef LOGGER_H_
#define LOGGER_H_
#include <iostream>
#include <string_view>
#include <iomanip>
#include <mutex>
#include <chrono>

void cleanConsole();

class Logger
{
public:
  static void debug(std::string_view _str)
  {
    message(BLUE, "Debug", _str);
  }
  static void info(std::string_view _str)
  {
    message(GREEN, "Info", _str);
  }
  static void warning(std::string_view _str)
  {
    message(YELLOW, "Warning", _str);
  }

  static void error(std::string_view _str)
  {
    message(RED, "Error", _str);
  }
  static void critical(std::string_view _str)
  {
    message(RED, "Critical", _str);
  }
  static constexpr std::string_view RED = "\x1B[31m";
  static constexpr std::string_view GREEN = "\x1B[32m";
  static constexpr std::string_view YELLOW = "\x1B[33m";
  static constexpr std::string_view BLUE = "\x1B[34m";
  static constexpr std::string_view MAGENTA = "\x1B[35m";
  static constexpr std::string_view CYAN = "\x1B[36m";
  static constexpr std::string_view WHITE = "\x1B[37m";
  static constexpr std::string_view RESET = "\033[0m";

private:
  inline static std::mutex s_printMutex;
  inline static bool s_displayTime = true;
  struct exitProc
  {
    exitProc() { std::atexit(cleanConsole); }
  };
  inline static exitProc s_cleanup = exitProc();

  static void
  message(std::string_view _colour, std::string_view _level, std::string_view _str)
  {
    const std::lock_guard<std::mutex> lock(s_printMutex);
    auto tm = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::cout << _colour << std::put_time(std::localtime(&tm), "[%I:%M%p]") << ' ' << _level << ' ' << _str << '\n';
  }
};

void cleanConsole()
{
  std::cout << Logger::RESET << '\n';
}

#endif