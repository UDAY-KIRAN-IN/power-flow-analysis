import pandapower as pp
import json
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
plt.savefig("output/network_diagram.png", dpi=200)
print("\nDiagram saved to output/network_diagram.png")