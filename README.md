# ByteRV-simulator
This is a simulation of a RISC-V computer in [Digital](https://github.com/hneemann/Digital). Part of the Selsiro project.

## Requirements
- [Digital simulator](https://github.com/hneemann/Digital/)
- Python 3
- [CPU tests framework](https://github.com/quintentruyens/Selsiro-cpu-tests) (using git submodule)

To automatically include the submodule, clone using the `--recurse-submodules` option or run `git submodule update --init` if the repository was already cloned without the option.

## Setup
First generate the control rom for the processor:
```sh
python3 ./rom/generate_control.py
```

Then start Digital, open [src/processor/control.dig](src/processor/control.dig) and set the file path in the advanced settings of the ROM to the newly created [rom/control.bin](rom/control.bin) file. Also change the Library path in the settings (Edit -> Settings -> Advanced -> Library Path) to point to the [lib](lib/) folder.

## Using the simulator
Open [src/main.dig](src/main.dig) in Digital and set the program file in the circuit settings (Edit -> Circuit specific settings -> Advanced -> Program file) to a binary file containing a program to run. Then start the simulation and use the measurement values (Simulation -> Show measurement value table) and the clock to run and track the simulation.

## Running the tests
Run the unit tests to test each individual component or the CPU tests to test the behaviour of the entire CPU. This only works correctly if no other instance of Digital is running.
```sh
python3 ./test/unit_test.py
python3 ./test/cpu_test.py
```