import os

def dir_maker(dirname):
    cmd = 'mkdir ' + dirname +'/yosys'
    cmd_1 = 'touch '+ dirname+'/yosys/yosys_sub.ys'
    os.popen(cmd)
    os.popen(cmd_1)

def yosys_syn_written_ys(dirname):
    system_syn = '#!/usr/bin/env yosys'+'\n'+\
        'read_verilog '+dirname+'/Subsystem_org.v'+'\n'+ \
        'hierarchy -top Subsystem'+'\n' + \
        'proc; fsm; opt; memory; opt' + '\n' + \
        'techmap; opt' + '\n' + \
        'write_verilog '+dirname+'/Subsystem_yosys.v'+'\n'
    ysfile_name = dirname+'/yosys/yosys_sub.ys'
    with open(ysfile_name, 'w') as f:
        f.write(system_syn)
        f.close()
    print('ys written is down')

def yosys_syn(dirname):
    ysfile_name = dirname + '/yosys/yosys_sub.ys'
    ys_command = 'yosys -s '+ ysfile_name
    re = os.popen(ys_command).read()
    print(re)
def yosys_handle(dirname):
    r1 = os.popen('cp '+ dirname+'/Subsystem_yosys.v'+' '+ dirname+'/yosys/Subsystem_yosys.v').read()
    r2 = os.popen('cp ' + dirname + '/Subsystem.v' + ' ' + dirname + '/yosys/Subsystem.v').read()
    r3 = os.popen('cp ' + dirname + '/top.v' + ' ' + dirname + '/yosys/top.v').read()
    print(r1,r2,r3)

def changeName(dirname):
    changeTop_1(dirname + '/yosys/Subsystem.v')
    changeTop_2(dirname+'/yosys/Subsystem_yosys.v')

def changeTop_1(dir):
    file_path = dir  # 替换为实际文件路径

    try:
        with open(file_path, 'r') as file:
            # 读取文件内容
            content = file.read()

            # 替换字符串
            new_content = content.replace("Subsystem", "Subsystem_1")

        # 写回文件
        with open(file_path, 'w') as file:
            file.write(new_content)

        print(f"成功替换文件中的 'Subsystem' 为 'Subsystem_1'。")

    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")
    except Exception as e:
        print(f"发生了一个异常: {e}")

def changeTop_2(dir):
    file_path = dir  # 替换为实际文件路径

    try:
        with open(file_path, 'r') as file:
            # 读取文件内容
            content = file.read()

            # 替换字符串
            new_content = content.replace("Subsystem", "Subsystem_2")

        # 写回文件
        with open(file_path, 'w') as file:
            file.write(new_content)

        print(f"成功替换文件中的 'Subsystem' 为 'Subsystem_2'。")

    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")
    except Exception as e:
        print(f"发生了一个异常: {e}")

def yosys_sby(dirname,files):
    include_statements = [f'{dirname}/{verilog_file}' for verilog_file in files if
                          verilog_file not in ['Subsystem.v', 'Subsystem_tb.v', 'Subsystem_org.v']]
    sby_text = '[options]'+'\n'+\
            'multiclock on'+'\n'+\
            'mode prove'+'\n'+\
            'aigsmt none'+'\n'+\
            '[engines]'+'\n'+\
            'abc pdr'+'\n'+\
            '[script]'+'\n'+\
            'read -formal '+dirname+'/yosys/Subsystem.v'+'\n'+\
            'read -formal '+dirname+'/yosys/Subsystem_yosys.v'+'\n'+\
            'read -formal '+dirname + '/yosys/top.v'+'\n'+\
            'prep -top top'+'\n'+\
            '[files]'+'\n'+\
            dirname+'/Subsystem.v'+'\n'+\
            dirname+'/Subsystem_yosys.v'+'\n'+\
            dirname+'/top.v'+'\n'+'\n'.join(include_statements)

    top_assert = 'module top  (Hdl_out_1, Hdl_out_2, ce_out_1, ce_out_2, clk, reset, clk_enable);'+'\n'+\
                 'output wire [7:0] Hdl_out_1;'+'\n'+\
                 'output wire [7:0] Hdl_out_2;'+'\n'+ \
                 'output wire [7:0] ce_out_1;' + '\n' + \
                 'output wire [7:0] ce_out_2;' + '\n' + \
                 'input wire clk;' + '\n' + \
                 'input wire reset;'+'\n'+\
                 'input wire clk_enable;'+'\n'+\
                 'Subsystem_1 Subsystem_1 (.Hdl_out(Hdl_out_1), .ce_out(ce_out_1), .clk(clk), .reset(reset), .clk_enable(clk_enable));'+'\n'+\
                 'Subsystem_2 Subsystem_2 (.Hdl_out(Hdl_out_2), .ce_out(ce_out_2), .clk(clk), .reset(reset), .clk_enable(clk_enable));'+'\n'+\
                 'always'+'\n'+\
                     '@(posedge clk) begin'+'\n'+\
                       'assert ((Hdl_out_1 == Hdl_out_2));'+'\n'+\
                 'end'+'\n'+\
                 'endmodule'


    sbyfile_name = dirname + '/yosys/yosys_sub.sby'
    with open(sbyfile_name, 'w') as f:
        f.write(sby_text)
        f.close()
        print('sby written is down')
    topfile_name = dirname + '/top.v'
    with open(topfile_name, 'w') as f1:
        f1.write(top_assert)
        f1.close()
        print('top written is down')

def equiv_yosy(dirname):
    cd_dir = 'cd ' + dirname
    compare = 'sby -f '+ dirname+ '/yosys/yosys_sub.sby'
    os.popen(cd_dir)
    ret = os.popen(compare).read()
    return ret
