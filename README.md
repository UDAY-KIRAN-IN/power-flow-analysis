# Power Flow Analysis using Pandapower

## Overview
This project simulates a small electrical distribution network using 
Python and pandapower, then analyzes the results to identify voltage 
issues and equipment loading levels — the same type of analysis 
performed by grid/network engineers at DNOs (Distribution Network 
Operators).

## Network Structure
- **Bus 1 (20 kV)** — Connected to the external grid (power source)
- **Transformer** — Steps voltage down from 20 kV to 0.4 kV
- **Bus 2 (0.4 kV)** — Load Side 1, connected to Load 1 (100 kW)
- **Line 1** — 0.5 km cable connecting Bus 2 to Bus 3
- **Bus 3 (0.4 kV)** — Load Side 2, connected to Load 2 (50 kW)

## Network Diagram
![Network Diagram](output/network_diagram.png)

## Key Finding
The power flow simulation revealed that **Bus 3 experiences a voltage 
drop to 86% of nominal (0.86 pu)** — below the acceptable range of 
95-105% typically used in distribution networks. This indicates the 
line connecting Bus 2 to Bus 3 may be undersized or too long for the 
combined load it's carrying, a common real-world issue when extending 
grid connections to new customers.

## Results Summary
| Component | Loading % |
|---|---|
| Transformer | 44.3% |
| Line 1 | 63.6% |

## Tools Used
- Python
- pandapower (network modeling and power flow simulation)
- matplotlib (visualization)

## What I Learned
- How to model buses, transformers, and lines using pandapower's 
  standard component library
- How to interpret power flow results (voltage magnitude, loading %, 
  power losses)
- How to identify voltage violations, a key task in distribution 
  network planning

## Project Structure
```
project-3-power-flow-analysis/
├── power_flow_analysis.py    # Main script — builds and simulates the network
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── output/
    └── network_diagram.png   # Generated network visualization
```