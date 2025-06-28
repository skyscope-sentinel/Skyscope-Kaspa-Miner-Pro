import os
import time
import sys

class DisplayManager:
    """
    Manages the CLI display for the SKYSCOPE Miner.
    Provides methods to update and print statistics in a user-friendly format.
    """
    def __init__(self, user_kaspa_address: str):
        self.start_time = time.time()
        self.kaspa_address = user_kaspa_address
        self.stats = {
            "hashrate_mhs": 0.0,
            "accepted_shares": 0,
            "rejected_shares": 0,
            "stale_shares": 0, # Added for more detail
            "total_kas_mined_net_user": 0.0, # Net KAS for user after dev fee & owner allocation
            "virtual_skyscope_mined": 0.0,
            "dev_fee_kas_cumulative": 0.0,
            "owner_kas_cumulative": 0.0, # KAS allocated to owner so far
            "owner_kas_target_remaining": 0.0, # KAS remaining for owner's target
            "uptime_seconds": 0,
            "kaspad_connected": False,
            "last_block_template_time": None,
            "errors": 0,
            "current_difficulty": "N/A" # Placeholder for block difficulty
        }
        self.last_print_time = 0
        self.print_interval = 1.0 # seconds, how often to allow re-printing stats

    def _clear_screen_alternative(self):
        """Alternative to os.system('cls') or os.system('clear') for more controlled refresh."""
        # Move cursor to home position (0,0)
        sys.stdout.write('\033[H')
        # Clear screen from cursor down
        sys.stdout.write('\033[J')
        sys.stdout.flush()

    def update_stat(self, key: str, value):
        """Updates a single statistic."""
        if key in self.stats:
            self.stats[key] = value
        else:
            print(f"Warning (DisplayManager): Unknown stat key '{key}'")

    def increment_stat(self, key: str, value_to_add=1):
        """Increments a specific statistic by a given value."""
        if key in self.stats and isinstance(self.stats[key], (int, float)):
            self.stats[key] += value_to_add
        else:
            print(f"Warning (DisplayManager): Cannot increment unknown or non-numeric stat key '{key}'")

    def set_kaspad_connected(self, connected: bool):
        self.stats["kaspad_connected"] = connected
        if connected and self.stats["last_block_template_time"] is None: # First connection
             self.stats["last_block_template_time"] = time.time()


    def print_dashboard(self, force_print: bool = False):
        """
        Prints the mining dashboard to the console.
        Uses ANSI escape codes for a basic in-place update effect if possible.
        Throttles printing to once per self.print_interval unless force_print is True.
        """
        current_time = time.time()
        if not force_print and (current_time - self.last_print_time < self.print_interval):
            return
        self.last_print_time = current_time

        self.stats["uptime_seconds"] = int(current_time - self.start_time)

        # Simple clear for now, can be improved with curses or platform-specific calls
        # if os.name == 'nt':
        #     os.system('cls')
        # else:
        #     os.system('clear')
        self._clear_screen_alternative()


        uptime_str = time.strftime('%H:%M:%S', time.gmtime(self.stats["uptime_seconds"]))
        connection_status = "Connected" if self.stats["kaspad_connected"] else "Disconnected"
        connection_color = "\033[92m" if self.stats["kaspad_connected"] else "\033[91m" # Green / Red

        header = (
            f"\033[1m\033[96mSKYSCOPE KASPA MINER\033[0m (Target: \033[93m{self.kaspa_address[:10]}...{self.kaspa_address[-5:]}\033[0m)\n"
            f"Uptime: \033[94m{uptime_str}\033[0m | Kaspad: {connection_color}{connection_status}\033[0m | Errors: \033[91m{self.stats['errors']}\033[0m\n"
            f"--------------------------------------------------------------------"
        )

        mining_stats = (
            f"Hashrate (Est. MH/s): \033[1m\033[92m{self.stats['hashrate_mhs']:.2f}\033[0m\n"
            f"Accepted Shares:      \033[92m{self.stats['accepted_shares']}\033[0m\n"
            f"Rejected Shares:      \033[91m{self.stats['rejected_shares']}\033[0m\n"
            f"Stale Shares:         \033[93m{self.stats['stale_shares']}\033[0m\n"
            f"Current Difficulty:   \033[94m{self.stats['current_difficulty']}\033[0m"
        )

        earnings_stats = (
            f"Virtual SKYSCOPE Mined: \033[1m\033[95m{self.stats['virtual_skyscope_mined']:,.2f}\033[0m\n"
            f"Net KAS Mined (User):   \033[1m\033[92m{self.stats['total_kas_mined_net_user']:,.8f}\033[0m KAS\n"
            f"Dev Fee Paid (10%):     \033[90m{self.stats['dev_fee_kas_cumulative']:,.8f}\033[0m KAS\n"
            f"Owner Allocation Paid:  \033[90m{self.stats['owner_kas_cumulative']:,.4f}\033[0m KAS\n"
            f"Owner Target Remaining: \033[93m{self.stats['owner_kas_target_remaining']:,.2f}\033[0m KAS (USD Value Based)"
        )

        if self.stats["last_block_template_time"]:
            time_since_last_block = int(time.time() - self.stats["last_block_template_time"])
            last_block_info = f"Last Block Template:    \033[90m{time_since_last_block}s ago\033[0m"
        else:
            last_block_info = "Last Block Template:    \033[90mWaiting...\033[0m"

        full_display = (
            f"{header}\n"
            f"\033[4mMining Performance\033[0m\n{mining_stats}\n"
            f"{last_block_info}\n\n"
            f"\033[4mEarnings Overview\033[0m\n{earnings_stats}\n"
            f"--------------------------------------------------------------------\n"
            f"\033[90mConceptual 'skyscope-hash-Q' RAM optimization active if configured.\033[0m\n"
            f"\033[90mPress Ctrl+C to stop the miner.\033[0m"
        )

        sys.stdout.write(full_display)
        sys.stdout.flush()

    def log_message(self, message: str, level: str = "INFO"):
        """
        Prints a log message to the console, could be expanded for file logging.
        For CLI, we might just print it below the dashboard or on a separate line.
        For now, simple print.
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(f"\n[{timestamp}] [{level}] {message}")
        # Potentially call print_dashboard(force_print=True) after a log message to refresh screen above it
        # but this might get messy if messages are frequent. Better to have a dedicated log area or file.


if __name__ == '__main__':
    test_address = "kaspa:qqggvdrxjqdgwql4aac8hg0pq2v4z5p46l86f98hq7ax29k7x55v7sycs9kvm"
    display = DisplayManager(user_kaspa_address=test_address)
    print("--- DisplayManager Conceptual Test ---")
    print("Dashboard will update in place (if terminal supports ANSI escapes).")

    try:
        display.set_kaspad_connected(True)
        display.update_stat("current_difficulty", "1.23 M")
        display.update_stat("owner_kas_target_remaining", 500000.00) # 50k USD worth at $0.10/KAS

        for i in range(10): # Simulate 10 updates
            display.increment_stat("hashrate_mhs", random.uniform(0.5, 2.0) * (i+1) * 0.1 ) # Simulate changing hashrate
            display.increment_stat("accepted_shares", random.randint(1,5))
            if i % 5 == 0 and i > 0:
                display.increment_stat("rejected_shares")
                display.increment_stat("errors")
            if i % 3 == 0 and i > 0:
                 display.increment_stat("stale_shares")

            kas_mined_this_tick_user = random.uniform(0.001, 0.005)
            dev_fee_this_tick = kas_mined_this_tick_user / 9 * 1 # 10% of gross, user gets 90%
            owner_kas_this_tick = random.uniform(0.01, 0.05) if display.stats["owner_kas_target_remaining"] > 1 else 0

            display.increment_stat("total_kas_mined_net_user", kas_mined_this_tick_user)
            display.increment_stat("dev_fee_kas_cumulative", dev_fee_this_tick)

            if display.stats["owner_kas_target_remaining"] > 0:
                actual_owner_alloc = min(owner_kas_this_tick, display.stats["owner_kas_target_remaining"])
                display.increment_stat("owner_kas_cumulative", actual_owner_alloc)
                display.update_stat("owner_kas_target_remaining", display.stats["owner_kas_target_remaining"] - actual_owner_alloc)


            display.increment_stat("virtual_skyscope_mined", (kas_mined_this_tick_user + dev_fee_this_tick + owner_kas_this_tick) * 100) # Based on gross KAS concept

            if i % 4 == 0: # Simulate losing connection
                 display.set_kaspad_connected(False)
                 display.log_message("Kaspad connection lost!", "ERROR")
            elif not display.stats["kaspad_connected"]:
                 display.set_kaspad_connected(True)
                 display.log_message("Kaspad reconnected.", "INFO")
                 display.update_stat("last_block_template_time", time.time())


            display.print_dashboard(force_print=True) # Force print for test updates
            time.sleep(1.1) # Sleep longer than print_interval to see updates

        display.set_kaspad_connected(False) # Final state
        display.print_dashboard(force_print=True)

    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    finally:
        # Reset cursor color and clear any remaining formatting
        sys.stdout.write("\033[0m")
        # os.system('cls' if os.name == 'nt' else 'clear') # Clear screen on exit
        print("\n--- Test Complete ---")
