import os
def vivado_test(dir):
    vivdao_syn(dir)
    result_value =vivdao_simulation(dir)
    print(result_value)
    index_start = result_value.find('## current_wave_config')
    index_end = result_value.find('$finish called at time')
    return result_value[index_start:index_end]
def vivdao_syn(dir):
    cd_dir = 'cd ' + dir
    vivado_cmd_rtl = cd_dir + '\n' + '/doc/Xilinx/Vivado/2023.2/bin/vivado -mode batch -source ' + dir + '/' + 'vivado_rtl2syn.tcl'
    print(vivado_cmd_rtl)
    ret = os.popen(vivado_cmd_rtl).read()
    print(ret)
def vivdao_simulation(dir):
    cd_dir = 'cd ' + dir
    vivado_cmd_sim = cd_dir + '\n' + '/doc/Xilinx/Vivado/2023.2/bin/vivado -mode batch -source ' + dir + '/' + 'vivado_sim.tcl'
    print(vivado_cmd_sim)
    result = os.popen(vivado_cmd_sim).read()
    return result
    return result