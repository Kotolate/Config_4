import struct
import json
import argparse

LOAD_CONSTANT = 90
READ_MEMORY = 1
WRITE_MEMORY = 62
SQRT = 137

class UVM:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size

    def execute(self, binary_path, result_path, memory_range):
        with open(binary_path, 'rb') as binary_file:
            binary_data = binary_file.read()

        i = 0
        while i < len(binary_data):
            command, = struct.unpack(">B", binary_data[i:i+1])
            i += 1

            if command == LOAD_CONSTANT:
                b, c = struct.unpack(">I I", binary_data[i:i+8])
                self.memory[b] = c
                i += 8
            elif command == READ_MEMORY:
                b, c, d = struct.unpack(">I I H", binary_data[i:i+10])
                addr = self.memory[c] + d
                if 0 <= addr < len(self.memory):
                    self.memory[b] = self.memory[addr]
                else:
                    raise ValueError(f"Memory address out of bounds: {addr}")
                i += 10
            elif command == WRITE_MEMORY:
                b, c = struct.unpack(">I I", binary_data[i:i+8])
                if 0 <= b < len(self.memory) and 0 <= c < len(self.memory):
                    self.memory[b] = self.memory[c]
                else:
                    raise ValueError("Memory address out of bounds")
                i += 8
            elif command == SQRT:
                b, c, d = struct.unpack(">I H I", binary_data[i:i+10])
                addr = self.memory[d]
                if 0 <= addr < len(self.memory):
                    source_value = self.memory[addr]
                    if source_value >= 0:
                        self.memory[b + c] = int(source_value**0.5)
                    else:
                        raise ValueError("Cannot calculate sqrt of negative number")
                else:
                    raise ValueError(f"Memory address out of bounds: {addr}")
                i += 10
            else:
                raise ValueError(f"Unknown command: {command}")

        start, end = memory_range
        result = {f"memory[{addr}]": value for addr, value in enumerate(self.memory[start:end])}
        with open(result_path, 'w') as result_file:
            json.dump(result, result_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, help="Path to the binary file")
    parser.add_argument("--result", required=True, help="Path to the result file")
    parser.add_argument("--range", required=True, help="Memory range (start:end)")
    args = parser.parse_args()
    start, end = map(int, args.range.split(':'))
    memory_range = (start, end)

    uvm = UVM()
    uvm.execute(args.binary, args.result, memory_range)

