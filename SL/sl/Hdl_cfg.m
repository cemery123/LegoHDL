classdef Hdl_cfg
 properties(Constant = true)
     TARGET_LANGUAGE = {
            %'SystemVerilog'  %generate sv language
            'Verilog'        %generate v language
            'VHDL'           %generate VHDL language
            };
     is_regenerate_SLforg = 1;
 end
end