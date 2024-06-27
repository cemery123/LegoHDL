# 文件路径
file_path = 'D:\slsf_randgen\slsf\cfg.m'

# 读取原始.m文件
with open(file_path, 'r') as file:
    lines = file.readlines()

# 修改内容
for i, line in enumerate(lines):
    if "'Verilog'" in line:
        lines[i] = "%{}'Verilog'        %generate v language\n".format(line[:line.find("'Verilog'")])
    elif "'SystemVerilog'" in line:
        lines[i] = line[line.find("%") + 1:]  # 删除该行开头的%

# 将修改后的内容写回文件
with open(file_path, 'w') as file:
    file.writelines(lines)

print("cfg.m has been updated.")
