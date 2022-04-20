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
  static void debug(std::string_view _str, bool _newline = true)
  {
    message(BLUE, "Debug", _str, _newline);
  }
  static void info(std::string_view _str, bool _newline = true)
  {
    message(GREEN, "Info", _str, _newline);
  }
  static void warning(std::string_view _str, bool _newline = true)
  {
    message(YELLOW, "Warning", _str, _newline);
  }

  static void error(std::string_view _str, bool _newline = true)
  {
    message(RED, "Error", _str, _newline);
  }
  static void critical(std::string_view _str, bool _newline = true)
  {
    message(RED, "Critical", _str, _newline);
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
  // use atexit to clean up, this will ensure the consloe colours are reset
  // basically I'm using a static init to ensure the function is registered
  struct exitProc
  {
    exitProc() { std::atexit(cleanConsole); }
  };
  // this will be called at instantiation just to regester the at exit
  // function
  inline static exitProc s_cleanup = exitProc();

  static void
  message(std::string_view _colour, std::string_view _level, std::string_view _str, bool _newLine)
  {
    const std::lock_guard<std::mutex> lock(s_printMutex);
    auto tm = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::cout << _colour << std::put_time(std::localtime(&tm), "[%I:%M%p]") << ' ' << _level << ' ' << _str << (_newLine ? '\n' : ' ');
  }
};

void cleanConsole()
{
  std::cout << Logger::RESET << '\n';
}

#endif