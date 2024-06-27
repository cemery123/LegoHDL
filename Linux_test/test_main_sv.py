import os
import vivado_tcl_sv
 import iverilog_sh_sv
 import vivado_sh


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

if __name__ == '__main__':
    directory_path = "/doc/xzh/resamplesource"
    files_list = list_files_in_directory(directory_path)
    latest_file = max(files_list, key=os.path.getctime)
    print(f"创建时间最晚的文件是: {latest_file}")
    path = latest_file + '/Verilog_hdlsrc'
    files = os.listdir(path)
    Error_log_Filename = path + '/error_log'
    if not os.path.exists(Error_log_Filename):
        with open(Error_log_Filename, 'w') as file:
            # 如果文件不存在，创建一个空文件
            pass
    else:
        print("has exsisted")
    for file in files:
        try:
            dirname = path + '/' + file
            verilog_files = get_verilog_files(dirname)
            result_string = ' '.join([f"{dirname}/{name}" for name in verilog_files])
            vivado_tcl_sv.vivado_tcl_write(dirname,result_string)
            print('tcl written')
            iverilog_result = iverilog_sh_sv.iverilog_test(dirname)
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
                f.write(dirname + ',' + 'Iverilog and Vivado simulation is wrong\n')
                f.close()
                print('error log written is down')
        except Exception as e:
            print(f"there are some erros: {e}")
            print('no design files')
        finally:
            print('done')

    print(1)