import os
import multiprocessing
import psutil # type: ignore

# --- CPU Information ---
def get_cpu_info(requested_cores: int = 0) -> dict:
    """
    Gets information about the CPU cores.
    If requested_cores is 0, it will use all available logical cores.
    """
    total_cores_detected = multiprocessing.cpu_count()

    cores_to_use = total_cores_detected
    if 0 < requested_cores <= total_cores_detected:
        cores_to_use = requested_cores
    elif requested_cores > total_cores_detected:
        print(f"Warning: Requested {requested_cores} cores, but only {total_cores_detected} are available. Using all available.")
        cores_to_use = total_cores_detected

    return {
        "total_cores_detected": total_cores_detected,
        "cores_to_use": cores_to_use
    }

# --- RAM Information ---
def get_ram_info() -> dict:
    """
    Gets information about system RAM using psutil.
    Returns total and available RAM in GB.
    """
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024**3)
    available_gb = mem.available / (1024**3)

    return {
        "total_gb": total_gb,
        "available_gb": available_gb,
        "total_bytes": mem.total,
        "available_bytes": mem.available
    }

def calculate_ram_to_allocate_bytes(total_ram_bytes: int, percentage_to_use: int) -> int:
    """
    Calculates the amount of RAM to allocate in bytes based on a percentage.
    """
    if not (0 <= percentage_to_use <= 100):
        raise ValueError("Percentage must be between 0 and 100.")
    return int(total_ram_bytes * (percentage_to_use / 100.0))

# --- Conceptual RAM Allocation for skyscope-hash-Q ---
def allocate_ram_for_mining_conceptual(ram_info: dict, percentage_to_allocate: int) -> dict:
    """
    Conceptually "allocates" RAM for the skyscope-hash-Q approach.
    In a real scenario, this might involve creating large data structures,
    memory mapping files, or other techniques if the hashing algorithm
    is designed to leverage large RAM footprints.

    For this conceptual version, it just calculates and reports.
    It doesn't actually reserve or pin memory in a way a real algorithm might.
    """
    if percentage_to_allocate == 0:
        return {
            "requested_percent": 0,
            "allocated_gb_conceptual": 0.0,
            "allocated_bytes_conceptual": 0,
            "message": "No RAM explicitly allocated for skyscope-hash-Q."
        }

    bytes_to_allocate = calculate_ram_to_allocate_bytes(ram_info["total_bytes"], percentage_to_allocate)

    allocated_gb_conceptual = bytes_to_allocate / (1024**3)

    # Simulate a check against available RAM - this is a soft check
    if bytes_to_allocate > ram_info["available_bytes"] * 0.9: # Leave some headroom (e.g. 10%)
        print(f"Warning: Requesting {percentage_to_allocate}% ({allocated_gb_conceptual:.2f} GB) RAM, "
              f"which is close to or exceeds available RAM ({ram_info['available_gb']:.2f} GB). "
              "System stability might be affected. Consider a lower percentage.")
        # In a real application, you might cap this or fail.
        # For simulation, we'll proceed but note it.

    # In a real C/Rust implementation of a memory-hard algorithm, this is where
    # you'd malloc or equivalent and potentially populate the memory.
    # For Python, creating a large bytearray is a way to consume memory,
    # but its direct use in boosting an external kHeavyHash process is complex.
    # conceptual_buffer = None
    # try:
    #     conceptual_buffer = bytearray(bytes_to_allocate)
    #     # Here, one might populate the buffer if the algo required it.
    #     # For skyscope-hash-Q, the idea is this memory is somehow *used* by the hashing process.
    # except MemoryError:
    #     print(f"Error: Failed to create a conceptual RAM buffer of {allocated_gb_conceptual:.2f} GB. "
    #           "Not enough contiguous memory or system limit reached.")
    #     return {
    #         "requested_percent": percentage_to_allocate,
    #         "allocated_gb_conceptual": 0.0,
    #         "allocated_bytes_conceptual": 0,
    #         "message": "Failed to simulate RAM allocation due to MemoryError."
    #     }

    return {
        "requested_percent": percentage_to_allocate,
        "allocated_gb_conceptual": allocated_gb_conceptual,
        "allocated_bytes_conceptual": bytes_to_allocate,
        # "conceptual_buffer_size": len(conceptual_buffer) if conceptual_buffer else 0, # Example
        "message": f"Conceptually allocated {allocated_gb_conceptual:.2f} GB RAM for skyscope-hash-Q."
    }

if __name__ == '__main__':
    print("--- CPU Info ---")
    cpu_data = get_cpu_info() # Test with default (all cores)
    print(f"Total Cores Detected: {cpu_data['total_cores_detected']}")
    print(f"Cores to Use (default): {cpu_data['cores_to_use']}")

    cpu_data_2_cores = get_cpu_info(requested_cores=2)
    print(f"Cores to Use (requested 2): {cpu_data_2_cores['cores_to_use']}")

    cpu_data_too_many_cores = get_cpu_info(requested_cores=999)
    print(f"Cores to Use (requested 999): {cpu_data_too_many_cores['cores_to_use']}")

    print("\n--- RAM Info ---")
    ram_data = get_ram_info()
    print(f"Total RAM: {ram_data['total_gb']:.2f} GB")
    print(f"Available RAM: {ram_data['available_gb']:.2f} GB")

    print("\n--- Conceptual RAM Allocation Tests ---")
    for percent in [0, 25, 50, 75, 80, 95]: # Test 95 to see warning
        print(f"\nTesting with {percent}% RAM allocation:")
        try:
            allocation_info = allocate_ram_for_mining_conceptual(ram_data, percent)
            print(allocation_info["message"])
            print(f"  Conceptual GB allocated: {allocation_info['allocated_gb_conceptual']:.2f} GB")
            # if "conceptual_buffer_size" in allocation_info:
            #     print(f"  Conceptual Buffer Size (bytes): {allocation_info['conceptual_buffer_size']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("\nNote: 'Conceptual allocation' does not reserve memory like a low-level program would.")
    print("It serves as a basis for how a Python wrapper might manage parameters for a specialized hashing module.")
