# LegoHDL
LegoHDL is the code of TCAD ( Transactions on Computer-Aided Design of Integrated Circuits and Systems )
# Demand
1. two test machine (windows and linux)
2. Matlab 2023b and above
3. python3.11 and above
4. Iverilog, yosys, Vivado and Quaturs
5. FTP trans in your Linux server
# Run
The main file to run LegoHDL is `GUIDANCE_main.py`, you can use 
`python GUIDANCE_main.py` to run Lego. But one thing may be crucial for you to run LegoHDL, that is you must ensuring that your python version is suitable to your matlab engine. If you do not know how to use matlab engine in python please read [matlab-engine-for-python ](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)
To better run LegoHDL we suggest user to config their CPS model size and category. Further more you should correctly config the FPGA syntheis Iverilog, yosys, Vivado and Quaturs in your test machine.
If you want to generate another HDL language revise `Hdl_cfg.m`
