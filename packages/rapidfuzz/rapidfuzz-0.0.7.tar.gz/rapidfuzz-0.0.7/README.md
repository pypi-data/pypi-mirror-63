<h1 align="center">
<img src="https://raw.githubusercontent.com/rhasspy/rapidfuzz/master/.github/RapidFuzz.svg?sanitize=true" alt="RapidFuzz" width="400">
</h1>
<h4 align="center">Rapid fuzzy string matching in Python and C++ using the Levenshtein Distance</h4>

<p align="center">
  <a href="https://github.com/rhasspy/rapidfuzz/actions">
    <img src="https://github.com/rhasspy/rapidfuzz/workflows/Python%20package/badge.svg"
         alt="Continous Integration">
  </a>
  <a href="https://github.com/rhasspy/rapidfuzz/blob/dev/LICENSE">
    <img src="https://img.shields.io/github/license/rhasspy/rapidfuzz">
  </a>
</p>

<p align="center">
  <a href="#why-should-you-care">Why Should You Care?</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#license">License</a>
</p>

---

## Why Should You Care?
Since there is already [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) that implements the same string similarity calculations you might wonder why you would want to use RapidFuzz. There are mainly two reasons:
1) It is MIT licensed so in contrast to FuzzyWuzzy it can be used in projects where you do not want to adopt the GPL License
2) While FuzzyWuzzy only used python-Levenshtein for the levenshtein calculations and implements the other functionalities in Python, RapidFuzz's implementation is mostly written in C++ and on Top of this comes with a lot of Algorithmic improvements. This results in a 5-300x Speedup in String Matching.


## Installation
RapidFuzz can be installed using [pip](https://pypi.org/project/rapidfuzz/)
```bash
$ pip install rapidfuzz
```
it requires Python 3.5 or later and a C++ Compiler with C++17 support, which should be given on all current systems


## Usage
```
> from rapidfuzz import fuzz
> from rapidfuzz import process
```

### Simple Ratio

### Partial Ratio

### Token Sort Ratio

### Token Set Ratio

### Process


## Roadmap
- [ ] build python wheels using manylinux container in CI
- [ ] add more Unit tests and run them in CI
- [ ] add more Benchmarks and run them in CI

## License
RapidFuzz is licensed under the MIT license since we believe that everyone should be able to use it without being forced to adopt our license. Thats why the library is based on an older version of fuzzywuzzy that was MIT licensed aswell.
A Fork of this old version of fuzzywuzzy can be found [here](https://github.com/rhasspy/fuzzywuzzy).
