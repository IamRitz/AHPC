import os
import shutil

# Define the path to the gem5 binary
gem5_path = '~/Downloads/gem5/build/X86/gem5.opt'

# Define the range of frequencies and step size
start_frequency = 600
end_frequency = 1000
step_size = 200

# List of CPU types and memory systems to test
cpu_types = ['TimingSimpleCPU', 'O3CPU', 'AtomicSimpleCPU']
memory_systems = ['DDR3_1600_8x8', 'DDR4_2400_8x8', 'DDR3_2133_8x8']

# Looping over CPU types, memory systems, and frequencies to run gem5 simulations
for cpu_type in cpu_types:
    for memory_system in memory_systems:
        for frequency in range(start_frequency, end_frequency + step_size, step_size):
            custom_stats_dir = "./Stats/" + "".join([cpu_type, "_", memory_system, "_", str(frequency), "_"])
            os.makedirs(custom_stats_dir, exist_ok=True)
            # Construct the gem5 command line
            cmd = [
                gem5_path,
                '-d ' + custom_stats_dir,
                'config.py', 
                '--cpu-type=' + cpu_type,
                '--cpu-clock=' + str(frequency),
                '--mem-type=' + memory_system,
            ]

            # Run the command
            os.system(' '.join(cmd))
