%% contorl Slforge to generate simulink modle
disp('### SLforge running begin')
try
   sgtest
catch e
    disp(e)
end
% 指定文件夹路径
folderPath = 'D:\slsf_randgen\slsf\reportsneo';
stmp = Get_file_name(folderPath);
stmp = stmp{length(stmp)};
Hdl_folderPath = ['D:\slsf_randgen\slsf\reportsneo','\',stmp,'\','success'];
Slx_list = Get_file_name(Hdl_folderPath);
for i = 1:length(Slx_list)
    modelpath = [Hdl_folderPath,'\',Slx_list{i}];
    h =load_system(modelpath);
    %set_param(h,'Check for presence of reals in generated HDL code','None');
    [token, remaining] = strtok(Slx_list{i}, '.');
    prefix = strrep(token, '.', '');
    disp(prefix);
    disp('**While loading simulink model to check it will take some time**');
 try
    outBlocks = find_system(h, 'BlockType', 'Outport');
    if isempty(outBlocks)
        b=Simulink.findBlocks(h);
        randomInteger = randi(length(b));
        out_handle = add_block('simulink/ Sinks/ Out1',[prefix,'/','Hdl_out']);
        add_line(h,out_handle,b{randomInteger});
    end
     b=Simulink.findBlocks(h);
     randomInteger = randi(length(b));
     out_handle = add_block('simulink/Sinks/Out1',[prefix,'/','Hdl_out']);
     out_port_handle = get_param(out_handle,'PortHandles');
     out_port_handle = out_port_handle.Inport;
     outputPortHandle = get_param(b(randomInteger), 'PortHandles');
     outputPortHandle = outputPortHandle.Outport;
     if ~isempty(outputPortHandle)
        add_line(h,outputPortHandle(1),out_port_handle);
     else
         disp('**recheck and choose**')
         for i = 1:length(b)
              outputPortHandle = get_param(b(i), 'PortHandles');
              outputPortHandle = outputPortHandle.Outport;
              if isempty(outputPortHandle)
              else
                 add_line(h,outputPortHandle(1),out_port_handle);
                 break;
              end
         end
     end
 catch 
     disp('no need to add anything')
 end
     %% HDL Code generation%%
     % before hdl generation to generate stimuli files create a subsystem
     %slicedStrings = split(Slx_list{i}, '.');
     save_system(prefix);
     is_changed = change_modelDataTypeStr(prefix);
     if is_changed == 1
         disp('All has changed')
     else
         disp('there are some errors')
     end
     load_system(prefix);
     sub_Stimuli_model_name = [prefix,'_sub'];
     new_system(sub_Stimuli_model_name);
     sub_str_arry = [sub_Stimuli_model_name,'/Subsystem'];
     add_block('built-in/Subsystem',sub_str_arry)
     Simulink.BlockDiagram.copyContentsToSubsystem...
     (h,sub_str_arry);
     model_save_path = [Hdl_folderPath,'\',sub_Stimuli_model_name,'.slx'];
     save_system(sub_Stimuli_model_name,model_save_path);
     disp('***save sucessful, next step is generate hdl code, please attention target language***')
     load_system(sub_Stimuli_model_name);
     try
     % Use hdlset_param to set the parameter on the model.
     hdlset_param(sub_Stimuli_model_name,'TreatRealsInGeneratedCodeAs','Warning')
     Hdl_src_path = [Hdl_folderPath,'\','hdlsrc'];
     if ~exist(Hdl_src_path, 'dir')
        mkdir(Hdl_src_path);
        disp(['floder ', Hdl_src_path, ' do not exist, creating it.']);
     else
        disp(['folder ', Hdl_src_path, ' has been existed.']);
     end
     makehdl(sub_str_arry, 'TargetLanguage', 'Verilog','TargetDirectory',Hdl_src_path)
     catch e
         disp('***** there are some errors *****')
         disp(e)
     end
     try
         %generate stimuli file
     makehdltb(sub_str_arry,'TargetLanguage','Verilog',...
          'UseFileIOInTestBench','off','TargetDirectory',Hdl_src_path);
     catch e
          disp('***** there are some errors in generating testbench*****')
     end
     disp('**close_system and save**')
     save_system(sub_Stimuli_model_name);
     close_system(sub_Stimuli_model_name);
     close_system(prefix);
end
function ret = Get_file_name(dirroad)
dirInfo = dir(dirroad);
fileNames = {};
for i = 1:length(dirInfo)
    if ~strcmp(dirInfo(i).name, '.') && ~strcmp(dirInfo(i).name, '..')
        fileNames{end+1} = dirInfo(i).name;
    end
end

disp('文件名列表：');
disp(fileNames);
ret = fileNames;
end