#ifndef CIRCUIT__H
#define CIRCUIT__H

#include <fstream>
#include <iostream>
#include <regex>
#include <unordered_map>
#include <unordered_set>

#include "errors.h"
#include "global.h"

namespace qflex {

struct QflexGate {
  std::string name;
  std::size_t cycle;
  std::vector<std::size_t> qubits;
  std::vector<double> params;
  std::string raw;

  std::ostream &operator<<(std::ostream &out) const;
  friend std::ostream &operator<<(std::ostream &out, const QflexGate &gate);
};

struct QflexCircuit {
  std::size_t num_active_qubits{0};
  std::size_t depth{0};
  std::vector<QflexGate> gates;

  void clear();
  void load(std::istream &istream);
  void load(std::istream &&istream);
  void load(const std::string &filename);
};

}  // namespace qflex

#endif
