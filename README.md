# Project 3: Firewall Controller with Mininet and POX

## Project Overview

This project implements a **software-defined networking (SDN) controller** using the **POX** controller framework. The controller is designed to manage network flows and block specific traffic based on rules defined in the controller's logic. The project uses **Mininet** to simulate a network topology, where the controller ensures that certain hosts can communicate while restricting traffic for untrusted hosts.

## Key Features

- **Mininet Topology**: A custom network topology created with Mininet that includes multiple hosts and switches.
- **POX Controller**: A firewall controller built using the POX framework, designed to manage flow rules and block specific traffic.
- **Traffic Management**: 
  - Untrusted hosts are blocked from sending ICMP or IP traffic to specified hosts and servers.
  - The controller allows trusted hosts to communicate freely with each other.
- **Flow Rules Management**: The POX controller installs flow rules in the switches' flow tables, ensuring efficient traffic routing.
- **Testing with Mininet Tools**: The project is tested using Mininet's `pingall`, `iperf`, and `dpctl dump-flows` commands to validate the correct behavior of the firewall rules.

## File Descriptions

- **topology.py**: Defines the Mininet topology with multiple hosts and switches. This file creates the network architecture used for testing the firewall controller.
- **project3controller.py**: The POX controller logic responsible for enforcing the firewall rules.
- **stable_controller.py**: An alternative or more stable version of the controller logic with potentially fewer bugs or more optimized performance.
- **123.py**: Helper or supplementary file used during the development process.
- **backup-just-incase.py**: A backup version of the controller logic or related code.

## How It Works

### Firewall Rules:

- **Untrusted Host Restrictions**: 
  - The untrusted host cannot send **ICMP traffic** to trusted hosts (Host 1, Host 2, Host 3) and the server.
  - The untrusted host is also restricted from sending **IP traffic** to these hosts, ensuring that the firewall prevents any form of communication.
- **Allowed Communication**: 
  - Trusted hosts can freely communicate with each other without restrictions.
  - The flow rules installed in the switches allow for efficient routing of traffic between trusted hosts.
  
### Key Mininet Commands:

- **pingall**: Tests ICMP communication between all hosts in the topology. The untrusted host's pings to trusted hosts should fail.
- **iperf**: Measures TCP/UDP performance between hosts. The untrusted host's TCP traffic to trusted hosts should be blocked.
- **dpctl dump-flows**: Dumps the installed flow rules in the switches, showing that the correct rules are in place to enforce the firewall logic.

## Usage Instructions

### Prerequisites

- **Mininet**: Installed and set up on your machine.
- **POX Controller**: Installed in the same directory as the project files.

### Running the Project

1. **Start the POX Controller**:
   ```bash
   ./pox.py project3controller
   ```
   Alternatively, you can use the stable version:
   ```bash
   ./pox.py stable_controller
   ```

2. **Run the Mininet Topology**:
   ```bash
   sudo python3 topology.py
   ```

3. **Clear Mininet Cache** (if needed):
   ```bash
   sudo mn -c
   ```

4. **Testing**:
   - **Ping all hosts** to validate communication:
     ```bash
     pingall
     ```
   - **Dump flow rules** to check the installed flow rules in the switches:
     ```bash
     dpctl dump-flows
     ```
   - **Test network performance** between hosts using `iperf`:
     ```bash
     iperf
     ```

## Results and Screenshots

- The controller was tested successfully using the following tools:
  - **pingall**: Verified that the untrusted host could not send ICMP traffic to trusted hosts and the server.
  - **dpctl dump-flows**: Verified that the correct flow rules were installed to manage traffic.
  - **iperf**: Verified that TCP traffic from the untrusted host was blocked, while trusted hosts could communicate without issues.

## Future Improvements

- **Enhanced Traffic Management**: Further refine the firewall logic to handle more complex traffic scenarios, such as restricting UDP traffic or implementing more granular access control.
- **User Interface**: Add a web interface to dynamically manage the firewall rules through the POX controller.
- **Additional Protocols**: Expand the project to block or allow traffic for additional network protocols (e.g., ARP, DHCP).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This project demonstrates proficiency in **software-defined networking (SDN)** using the **POX** controller and **Mininet**. The implementation showcases advanced network traffic management and demonstrates the power of controller-based networking.

---
