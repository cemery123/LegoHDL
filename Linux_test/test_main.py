import os
import iverilog_sh
import vivado_sh
import vivado_tcl
import yosys_sh

def list_files_in_directory(directory):
    files = os.listdir(directory)

    file_list = []

    # 遍历文件和子目录
    for file in files:
        full_path = os.path.join(directory, file)
        file_list.append(full_path)


    return file_list

def get_verilog_files(directory):
    all_files = os.listdir(directory)

    verilog_files = [file for file in all_files if file.endswith('.v') and file not in ['Subsystem', 'Subsystem_tb']]

    return verilog_files

def handle_main(directory_path):
    files_list = list_files_in_directory(directory_path)
    latest_file = max(files_list, key=os.path.getctime)
    print(f"创建时间最晚的文件是: {latest_file}")
    path = latest_file + '/Verilog_hdlsrc'
    #path = files_list[len(files_list)-1]
    files = os.listdir(path)
    print(path)
    Error_log_Filename = path+'/error_log'
    if not os.path.exists(Error_log_Filename):
        with open(Error_log_Filename, 'w') as file:
            # 如果文件不存在，创建一个空文件
            pass
    else:
        print("has exsisted")
    for file in files:
        try:
            dirname = path + '/' + file
            Verilog_files = get_verilog_files(dirname)
            V_file = dirname + '/Subsystem.v'
            with open(V_file, 'r') as file:
                content = file.read()
                index = content.find('timescale 1 ns / 1 ns')
                if index != -1:
                    with open(V_file, 'w') as file:
                        include_statements = [f'`include "{verilog_file}"' for verilog_file in Verilog_files if
                                      verilog_file not in ['Subsystem.v', 'Subsystem_tb.v', 'Subsystem_org.v']]
                        updated_content = content[:index+21] +'\n'+ '\n'.join(
                            include_statements) + '\n' + content[index+21:]
                        file.write(updated_content)
                else:
                    print("Not found timescale")
            #change tb files
            tb_file = dirname + '/Subsystem_tb.v'
            with open(tb_file, 'r') as file:
                content = file.read()
                index = content.find('timescale 1 ns / 1 ns')
                if index != -1:
                    with open(tb_file, 'w') as file:
                        include_testbench = dirname + '/Subsystem.v'
                        include_statements = '`include '+'"'+include_testbench+'"'
                        updated_content = content[:index+21] + '\n' +include_statements + '\n' + content[index+21:]
                        file.write(updated_content)
                else:
                    print("Not found timescale")
            yosys_sh.dir_maker(dirname)
            yosys_sh.yosys_syn_written_ys(dirname)
            yosys_sh.yosys_sby(dirname,Verilog_files)
            iverilog_result = iverilog_sh.iverilog_test(V_file,dirname+'/Subsystem_tb.v',dirname)
            vivado_tcl.vivado_tcl_write(dirname)
            print('tcl written')
            if iverilog_result.find('**************TEST COMPLETED (PASSED)**************') != -1:
                iverilog_result_value = 1
                print('Iverilog test pass')
            else:
                iverilog_result_value = 0
                f = open(Error_log_Filename, "a")
                f.write(dirname + ',' + 'Iverilog simulation is wrong\n')
                f.close()
                print('error log written is down')
            Vivado_result = vivado_sh.vivado_test(dirname)
            if Vivado_result.find('**************TEST COMPLETED (PASSED)**************') != -1:
                Vivado_result_value = 1
                print('Iverilog test pass')
            else:
                Vivado_result_value = 0
                f = open(Error_log_Filename, "a")
                f.write(dirname + ',' + 'Vivado simulation is wrong\n')
                f.close()
                print('error log written is down')
            if iverilog_result_value == Vivado_result_value:
                print('It is equivalent!')
            else:
                f = open(Error_log_Filename, "a")
                f.write(dirname+','+'Iverilog and Vivado simulation is wrong\n')
                f.close()
                print('error log written is down')
            yosys_sh.yosys_syn(dirname)
            yosys_sh.yosys_handle(dirname)
            yosys_sh.changeName(dirname)
            ret = yosys_sh.equiv_yosy(dirname)
            print(ret)
            done_index = ret.find('DONE (')
            if done_index != -1:
                result_variable = ret[done_index + 6:done_index + 10]
                print("Found 'DONE ', result:", result_variable)
                if result_variable == 'FAIL':
                    f = open(Error_log_Filename, "a")
                    f.write(dirname + ',' + 'Yosys syn is wrong\n')
                    f.close()
                    print('error log written is down')
            else:
                print("'DONE ' not found in the string.")
        except Exception as e:
            print(f"there are some erros: {e}")
            print('no design files')
        finally:
            print('done')

def cp_orgfile(directory_path):
    files_list = list_files_in_directory(directory_path)
    latest_file = max(files_list, key=os.path.getctime)
    print(f"创建时间最晚的文件是: {latest_file}")
    path = latest_file+'/Verilog_hdlsrc'
    #path = files_list[len(files_list) - 1]
    files = os.listdir(path)
    n = 1
    print(path)
    for file in files:
        try:
            dirname = path + '/' + file
            V_file = dirname + '/Subsystem.v'
            # copy subsystem.v for yosys
            copy_cmd = 'cp ' + V_file + ' ' + dirname + '/Subsystem_org.v'
            result = os.popen(copy_cmd).read()
            print(result)
        except Exception as e:
            print(f"there are some erros: {e}")
            print('no design files')
        finally:
            print('done')
            n = n+1
    print(n)

if __name__ == '__main__':
    directory_path = "/doc/xzh/resamplesource"
    cp_orgfile(directory_path)
    handle_main(directory_path)
