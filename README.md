
# LegoHDL

LegoHDL is the code of TCAD (Transactions on Computer-Aided Design of Integrated Circuits and Systems).

## Requirements

1. Two test machines (Windows and Linux)
2. Matlab 2023b and above
3. Python 3.11 and above
4. Iverilog, Yosys, Vivado, and Quartus
5. FTP transfer capability on your Linux server

## Running LegoHDL

The main file to run LegoHDL is `GUIDANCE_main.py`. You can use the following command to run it:

```sh
python GUIDANCE_main.py
```

### Important Considerations

1. **Python-Matlab Engine Compatibility**: Ensure that your Python version is compatible with the Matlab engine. If you are unfamiliar with using the Matlab engine in Python, please read the [Matlab Engine for Python documentation](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html).

2. **CPS Model Configuration**: To achieve optimal performance, configure your CPS model's size and category appropriately.

3. **FPGA Synthesis Tools Configuration**: Correctly configure the FPGA synthesis tools (Iverilog, Yosys, Vivado, and Quartus) on your test machines.

### Generating HDL Code

If you need to generate another HDL language, revise the `Hdl_cfg.m` file according to your requirements.
