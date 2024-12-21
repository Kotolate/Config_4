import argparse
import json
import struct

def assemble_instruction(line):
    fields = line.split()
    command = int(fields[0])


    if command == 90:
        b = int(fields[1])
        c = int(fields[2])
        return struct.pack(">B I I", command, b, c)
    elif command == 1:
        b = int(fields[1])
        c = int(fields[2])
        d = int(fields[3])
        return struct.pack(">B I I H", command, b, c, d)
    elif command == 62:
        b = int(fields[1])
        c = int(fields[2])
        return struct.pack(">B I I", command, b, c)
    elif command == 137:
        b = int(fields[1])
        c = int(fields[2])
        d = int(fields[3])
        return struct.pack(">B I H I", command, b, c, d)
    else:
        raise ValueError(f"Unknown command: {command}")

def assemble(input_path, output_path, log_path):
    binary_data = bytearray()
    log_data = []

    with open(input_path, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            instruction = assemble_instruction(line)
            binary_data.extend(instruction)

            log_entry = {"instruction": line, "binary": instruction.hex()}
            log_data.append(log_entry)

    with open(output_path, 'wb') as output_file:
        output_file.write(binary_data)

    with open(log_path, 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for UVM")
    parser.add_argument("--input", required=True, help="Path to the input assembly file")
    parser.add_argument("--output", required=True, help="Path to the output binary file")
    parser.add_argument("--log", required=True, help="Path to the log file")
    args = parser.parse_args()

    assemble(args.input, args.output, args.log)
