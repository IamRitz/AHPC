import m5
from m5.objects import *

import argparse

# Function to create the gem5 system based on command-line arguments
def create_system(args):
    system = System()

    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "".join([str(args.cpu_clock), 'MHz'])
    system.clk_domain.voltage_domain = VoltageDomain()


    if(args.cpu_type == 'AtomicSimpleCPU'):
        system.mem_mode = "atomic"  # Use Atomic Access
    else:
        system.mem_mode = "timing"  # Use timing accesses
    system.mem_ranges = [AddrRange("1GiB")]  # Create an address range

    # Example: Setting CPU type and clock frequency
    if args.cpu_type == 'TimingSimpleCPU':
        system.cpu = X86TimingSimpleCPU()
    elif args.cpu_type == 'O3CPU':
        system.cpu = X86O3CPU()
    elif args.cpu_type == 'AtomicSimpleCPU':
        system.cpu = X86AtomicSimpleCPU()

    # Create a memory bus, a system crossbar, in this case
    system.membus = SystemXBar()

    # Hook the CPU ports up to the membus
    system.cpu.icache_port = system.membus.cpu_side_ports
    system.cpu.dcache_port = system.membus.cpu_side_ports

    # create the interrupt controller for the CPU and connect to the membus
    system.cpu.createInterruptController()

    # For X86 only we make sure the interrupts care connect to memory.
    # Note: these are directly connected to the memory bus and are not cached.
    # For other ISA you should remove the following three lines.
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

    system.mem_ctrl = MemCtrl()

    # Create a DDR3/DDR4 memory controller and connect it to the membus
    if args.mem_type == 'DDR3_1600_8x8':
        system.mem_ctrl.dram = DDR3_1600_8x8()
    elif args.mem_type == 'DDR3_2133_8x8':
        system.mem_ctrl.dram = DDR3_2133_8x8()
    elif args.mem_type == 'DDR4_2400_8x8':
        system.mem_ctrl.dram = DDR4_2400_8x8()

    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    # Connect the system up to the membus
    system.system_port = system.membus.cpu_side_ports

    return system

# Parsing command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument('--cpu-type', choices=['TimingSimpleCPU', 'O3CPU', 'AtomicSimpleCPU'], default='TimingSimpleCPU')
parser.add_argument('--cpu-clock', type=int, default=600)
parser.add_argument('--mem-type', choices=['DDR3_1600_8x8', 'DDR4_2400_8x8', 'DDR3_2133_8x8'], default='DDR3_1600_8x8')

args = parser.parse_args()

# Function to create and setup System parameters
system = create_system(args)


# Binary to benchmark
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "Binaries/",
    "mm.1",
)

system.workload = SEWorkload.init_compatible(binary)

# Create a process for a Matrix-Multiplication application
process = Process()

# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [binary]

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)

# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
