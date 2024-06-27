import os
def vivado_tcl_write(dir_name):

        rtl2syn = 'read_verilog '+dir_name+'/Subsystem.v'+'\n'+\
                    'synth_design -part xc7k70t -top Subsystem'+'\n'+\
                    'write_verilog -force '+dir_name+'/'+'Subsystem_vivado.v'
        tcl_rtl = dir_name + '/' + 'vivado_rtl2syn.tcl'
        f = open(tcl_rtl, "w")
        f.write(rtl2syn)
        f.close()
        filename =dir_name+ '/'+'Subsystem_vivado.v'
        filename_testbench = dir_name + '/' +'Subsystem_tb.v'
        excute = 'create_project -force sim_132'+' /doc/xzh/vivado_test'+'\n'
        add_file = 'add_files -norecurse '+filename+'\n'+'add_files -fileset sim_1 -norecurse '+filename_testbench+'\n'
        set_head = 'set_property is_global_include true [get_files '+filename+']\n'
        sim = \
            'import_files -force -norecurse'+'\n'+'update_compile_order -fileset sources_1'+'\n'+'update_compile_order -fileset sim_1'+'\n'+\
             'set_property top Subsystem_tb [get_filesets sim_1]'+'\n'+'set_property top_lib xil_defaultlib [get_filesets sim_1]'+'\n'+\
            'launch_simulation'+'\n'+'open_vcd /doc/xzh/vivado_test/xsim_dump_1.vcd'+'\n'+'log_vcd /testbench/*'+'\n'+'run 10ns'+'\n'+'close_vcd'
        word = excute+add_file+set_head
        #open_object = 'open_project /doc/xzh/vivado_test/sim_'+str(i)+'.xpr\n'
        sim_word = word+sim
        tcl_name = dir_name+'/'+'vivado_sim.tcl'
        f = open(tcl_name,"w")
        f.write(sim_word)
        f.close()
        print(tcl_name)
        print('tcl written is down')
