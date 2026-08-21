import pandapower as pp
import json
import matplotlib.pyplot as mt

net = pp.create_empty_network()

bus1 = pp.create_bus(net, vn_kv=20, name='Bus 1 - Generator side')
bus2 = pp.create_bus(net, vn_kv=0.4, name='Bus 2 - Load side')
bus3 = pp.create_bus(net, vn_kv=0.4, name='Bus 3 - Load side')
line1 = pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=0.5, std_type='NAYY 4x50 SE', name='Line 1')

Transformer = pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, std_type= '0.4 MVA 20/0.4 kV', name= 'Transformer 1' )

load1 = pp.create_load(net, bus=bus2, p_mw=0.1, q_mvar=0.05, name='Load 1')
load2 = pp.create_load(net, bus=bus3, p_mw=0.05, q_mvar=0.02, name='Load 2')
ext_grid1 = pp.create_ext_grid(net, bus=bus1, vm_pu=1.0, name='Grid connection')

pp.runpp(net)

print('Bus voltage results : ')
print(net.res_bus)

print('\nTransformer loading results : ')
print(net.res_trafo)

print('\nLine loading results : ')
print(net.res_line)


import pandapower.plotting as plot
net.bus["geo"] = [
    json.dumps({"type": "Point", "coordinates": [0, 0]}),
    json.dumps({"type": "Point", "coordinates": [2, 0]}),
    json.dumps({"type": "Point", "coordinates": [4, 0]})]
plot.simple_plot(net, plot_loads=True, plot_sgens=True, show_plot=False)

import matplotlib.pyplot as plt
plt.savefig("output/network_diagram.png", dpi=300)
print("\nDiagram saved to output/network_diagram.png")


# ---- VERSION 2: Expanded Branching Network ----

net2 = pp.create_empty_network()

bus1_v2 = pp.create_bus(net2, vn_kv=20, name='Bus 1 - Generator side')
bus2_v2 = pp.create_bus(net2, vn_kv=0.4, name='Bus 2 - Main Feeder')
bus3_v2 = pp.create_bus(net2, vn_kv=0.4, name='Bus 3 - Branch A')
bus4_v2 = pp.create_bus(net2, vn_kv=0.4, name='Bus 4 - Branch B')
bus5_v2 = pp.create_bus(net2, vn_kv=0.4, name='Bus 5 - Branch B End')

trafo_v2 = pp.create_transformer(net2, hv_bus=bus1_v2, lv_bus=bus2_v2, std_type='0.4 MVA 20/0.4 kV', name='Trafo V2')

line1_v2 = pp.create_line(net2, from_bus=bus2_v2, to_bus=bus3_v2, length_km=0.4, std_type='NAYY 4x50 SE', name='Line 1 (Bus2-Bus3)')
line2_v2 = pp.create_line(net2, from_bus=bus2_v2, to_bus=bus4_v2, length_km=0.5, std_type='NAYY 4x50 SE', name='Line2 (Bus2-Bus4)')
line3_v2 = pp.create_line(net2, std_type='NAYY 4x50 SE', from_bus=bus4_v2, to_bus=bus5_v2, length_km=0.6, name='Line 3 (Bus4-Bus5)')

load1_v2 = pp.create_load(net2, bus=bus3_v2, p_mw=0.05, q_mvar=0.02, name='Load 1 (Bus 3)')
load2_v2 = pp.create_load(net2, bus=bus5_v2, p_mw=0.04, q_mvar=0.015, name='Load 2 (Bus 5)')

ext_grid_v2 = pp.create_ext_grid(net2, bus=bus1_v2, vm_pu=1.0, name='Grid Connection V2')

pp.runpp(net2)

print('\n\n========== VERSION 2 RESULTS ===========')
print('\nBus Voltage Results (V2) : ')
print(net2.res_bus)
print('\nTransformer Loading Results (V2) : ')
print(net2.res_trafo)
print('\nLine Loading Results (V2) : ')
print(net2.res_line)

net2.bus['geo'] = [
    json.dumps({'type':'point', 'coordinates':[0,0]}),
    json.dumps({'type':'point', 'coordinates':[2,0]}),
    json.dumps({'type':'point', 'coordinates':[4,1]}),
    json.dumps({'type':'point', 'coordinates':[4,-1]}),
    json.dumps({'type':'point', 'coordinates':[6,-1]})
]

plot.simple_plot(net2, plot_loads=True, plot_sgens=True, show_plot=False)

mt.savefig('output/network_diagram_v2.png', dpi=350)
print('\nDiagram V2 saved to output/network_diagram_v2.png')

print('\n\n===== N-1 CONTINGENCY TEST: Line 2 (Bus2-Bus4) Disabled =====')

net2.line.loc[line2_v2, 'in_service'] = False

pp.runpp(net2)

print('\nBus Voltage Results (After Line 2 Failure)  : ')
print(net2.res_bus)

plot.simple_plot(net2, plot_loads=True, plot_sgens=True, show_plot=False)

plt.savefig('output/network_diagram_v2_line2_failure.png', dpi=350)
print('\nDiagram (Line 2 Failure) saved to output/network_diagram_v2_line2_failure.png')

net2.line.loc[line2_v2, 'in_service'] = True
pp.runpp(net2)
print('\nLine 2 restored — network back to healthy state')
print('\nBus Voltage Results (After Restoring Line 2):')
print(net2.res_bus)

print('\n\n===== SOLAR GENERATION TEST: Adding Solar at Bus 5 =====')

solar_v2 = pp.create_sgen(net2, bus=bus5_v2, p_mw=0.03, q_mvar=0, name='Solar PV at Bus 5')

pp.runpp(net2)

print('\nBus Voltage Results (With Solar at Bus 5) : ')
print(net2.res_bus)

print('\nTransformer Loading Results (With Solar) : ')
print(net2.res_trafo)

print('\nLine Loading Results (With Solar) : ')
print(net2.res_line)

print('\n\n===== SOLAR GENERATION TEST: Adding Solar at Bus 3 too =====')

solar_bus3_v2 = pp.create_sgen(net2, bus=bus3_v2, p_mw=0.03, q_mvar=0, name='Solar PV at Bus 3')

pp.runpp(net2)

print('\nBus Voltage Results (With Solar at Bus 3 AND Bus 5) : ')
print(net2.res_bus)