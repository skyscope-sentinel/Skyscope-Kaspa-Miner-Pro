# SKYSCOPE Kaspa Miner - User Manual

## 1. Introduction

Welcome to SKYSCOPE Miner! This Python-based command-line application is designed for mining Kaspa (KAS) primarily using Intel CPUs. It introduces the conceptual "skyscope-hash-Q" engine, an innovative approach aiming to leverage both your CPU cores and system RAM to potentially enhance Kaspa mining efficiency.

SKYSCOPE Miner provides a user-friendly interface to connect to your `kaspad` node, manage mining operations, and track your earnings with a unique dual display of virtual SKYSCOPE (representing mining effort/efficiency) and actual KAS mined.

**Project Visionary:** Miss Casey Jay Topojani, Skyscope Sentinel Intelligence
**Contact:** skyscopesentinel@gmail.com
**GitHub:** [https://github.com/skyscope-sentinel](https://github.com/skyscope-sentinel) (Link will be active when project is public)
**ABN:** 11287984779

## 2. IMPORTANT DISCLAIMER

*   **Conceptual Technology:** The "skyscope-hash-Q" RAM-boosted mining approach is currently a **conceptual design and research & development goal**. While the miner allows you to allocate RAM, the actual performance benefits from this specific RAM utilization technique for Kaspa's kHeavyHash algorithm require further deep research, development, and rigorous testing. Any performance gains suggested by this feature are illustrative of the concept's aim, not guaranteed outcomes with the current scaffolding.
*   **Software Status:** This manual describes the intended functionality of SKYSCOPE Miner. The initial versions are developmental.
*   **Use at Your Own Risk:** Standard cryptocurrency mining involves risks, including hardware wear and market volatility. Ensure you understand these before proceeding.

## 3. Prerequisites

Before running SKYSCOPE Miner, please ensure you have the following:

*   **Python:** Python 3.8 or newer installed on your system. You can download it from [python.org](https://www.python.org/).
*   **`kaspad` Node:** A running and fully synced Kaspa full node (`kaspad`). The miner needs to connect to this node to get block templates and submit solutions. You can find instructions for installing `kaspad` on the official Kaspa resources. Ensure its RPC/gRPC interface is accessible to the miner (usually `localhost:16110` by default).
*   **Python Dependencies:**
    *   `psutil`: For fetching system information like CPU and RAM usage.
        ```bash
        pip install psutil
        ```
    *   *(Future dependencies like `grpcio` and Kaspa protobufs would be listed here if a direct gRPC implementation is added.)*
*   **Intel CPU:** While it might run on other CPUs, the "skyscope-hash-Q" concept is initially being explored with Intel CPU architectures in mind.

## 4. Installation / Getting the Miner

*   **Coming Soon:** SKYSCOPE Miner will be available for download from the project's GitHub releases page (link to be provided once public).
*   **Manual Setup (for development/testing):**
    1.  Clone the repository: `git clone https://github.com/skyscope-sentinel/skyscope-miner.git` (Example URL)
    2.  Navigate to the directory: `cd skyscope-miner`
    3.  The main script is typically `skyscope_miner/skyscope_miner.py`.

## 5. Configuration & Running the Miner

SKYSCOPE Miner is configured via command-line arguments.

### 5.1. Command-Line Arguments:

*   `kaspa_address` (Required): Your Kaspa wallet address where mining rewards (after fees and owner allocation period) will be sent.
    *   Example: `kaspa:qzrhasap30pzrth070tx6m0nslk03xl0qgmpguex68nmd68g277fuqfsqg0ls`
*   `--node-url` (Optional): URL of your `kaspad` node's gRPC interface.
    *   Default: `127.0.0.1:16110`
    *   Example: `--node-url my.kaspadnode.com:16110`
*   `--cpu-cores` (Optional): Number of CPU cores to use for mining.
    *   Default: `0` (uses all available logical cores).
    *   Example: `--cpu-cores 4` (uses 4 cores).
*   `--ram-percent` (Optional): Percentage of system RAM to conceptually allocate for the "skyscope-hash-Q" boost.
    *   Default: `0` (no explicit RAM allocation for boost beyond standard OS usage).
    *   Choices: `0`, `25`, `50`, `75`, `80`.
    *   Example: `--ram-percent 50`
    *   **Note:** High RAM allocation can impact system stability if not enough RAM is left for the OS and other applications. Use with caution. The actual performance impact is part of ongoing R&D.
*   `--dev-fee-address` (Optional): The Kaspa address for the 10% developer fee.
    *   Default: `kaspa:qqggvdrxjqdgwql4aac8hg0pq2v4z5p46l86f98hq7ax29k7x55v7sycs9kvm` (SKYSCOPE Project's official fee address).
*   `--log-level` (Optional): Set the logging level for console output.
    *   Default: `INFO`
    *   Choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`.
    *   Example: `--log-level DEBUG` (for more verbose output).

### 5.2. Example Command:

```bash
python skyscope_miner/skyscope_miner.py kaspa:youractualkaspaaddressgoeshere --cpu-cores 0 --ram-percent 50 --node-url 127.0.0.1:16110
```

Replace `kaspa:youractualkaspaaddressgoeshere` with your actual Kaspa wallet address.

### 5.3. Running the Miner:

1.  Open your terminal or command prompt.
2.  Navigate to the directory where `skyscope_miner.py` is located (or the root of the cloned repository).
3.  Execute the script using Python, followed by your desired arguments.

## 6. Understanding the Output (CLI Dashboard)

The miner will display a dashboard in your terminal, updating periodically:

*   **Header:** Shows miner name, visionary details, and contact.
*   **Uptime:** How long the miner has been running.
*   **Kaspad Status:** `Connected` or `Disconnected`.
*   **Errors:** Count of critical errors encountered.
*   **Mining Performance:**
    *   `Hashrate (Est. MH/s)`: Your estimated mining speed in Megahashes per second.
    *   `Accepted Shares`: Number of valid work units accepted by the network.
    *   `Rejected Shares`: Shares rejected by the pool/node (e.g., stale, duplicate).
    *   `Stale Shares`: Shares submitted too late.
    *   `Current Difficulty`: The current mining difficulty of the Kaspa network.
*   **Last Block Template:** Time since the last work unit was received from `kaspad`.
*   **Earnings Overview:**
    *   `Virtual SKYSCOPE Mined`: A visual representation of your mining effort/efficiency. This is not a separate tradable token.
    *   `Net KAS Mined (User)`: Estimated Kaspa earned that will go to your wallet (after dev fee and once owner's allocation target is met).
    *   `Dev Fee Paid (10%)`: Cumulative Kaspa allocated to the developer fee.
    *   `Owner Allocation Paid`: Cumulative Kaspa allocated towards the owner's 50,000 USD target.
    *   `Owner Target Remaining`: Remaining KAS needed to fulfill the owner's allocation target (based on current KAS/USD price).
*   **Status Messages:** Informational messages, warnings, or errors.

To stop the miner, press `Ctrl+C`.

## 7. Fee Structure & Owner's Allocation

*   **Developer Fee:** A transparent 10% fee is applied to all KAS rewards generated by the miner. This fee is automatically sent to the developer's Kaspa address (`kaspa:qqggvdrxjqdgwql4aac8hg0pq2v4z5p46l86f98hq7ax29k7x55v7sycs9kvm`) and supports the ongoing development, maintenance, and improvement of SKYSCOPE Miner.
*   **Owner's Allocation:** The miner is programmed to prioritize allocating the first 50,000 USD worth of mined KAS (after the 10% dev fee) to the project visionary's wallet (`kaspa:qqggvdrxjqdgwql4aac8hg0pq2v4z5p46l86f98hq7ax29k7x55v7sycs9kvm` - *Note: This is the same as dev fee address in current setup, confirm if intended to be different*). This is a one-time accumulation target. Once this target is met, all subsequent rewards (after the dev fee) go directly to your user Kaspa address. The KAS equivalent for the USD target is based on a periodically updated KAS/USD price.

## 8. Troubleshooting

*   **Cannot connect to kaspad:**
    *   Ensure `kaspad` is running and fully synced.
    *   Verify the `--node-url` is correct and accessible from the machine running the miner.
    *   Check your firewall settings.
*   **Invalid Kaspa Address:** Ensure your `kaspa_address` starts with `kaspa:` and is correct.
*   **Low Hashrate:** CPU mining performance depends on your CPU model, number of cores used, and potentially the "skyscope-hash-Q" RAM allocation (effectiveness is R&D). Ensure no other CPU-intensive tasks are running.
*   **For other issues or support:** Please check the project's GitHub issues page or contact skyscopesentinel@gmail.com.

Thank you for using SKYSCOPE Miner! We hope it empowers your Kaspa mining journey.
