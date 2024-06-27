function ret = change_modelDataTypeStr(h)
    open_system(h);
    blocks = find_system(h, 'FindAll', 'on', 'SearchDepth', 1, 'Type', 'block');
    for i = 1:length(blocks)
        try
            set_param(blocks(i), 'OutDataTypeStr', 'uint8');
        catch e
            disp('This block do not have Settings config for OutDataTypeStr');
        end
    end
    save_system(h);
    ret = 1;
end