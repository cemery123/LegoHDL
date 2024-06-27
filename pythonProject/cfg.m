classdef cfg
    %CFG User-changable configurations
    %   Change various configure parameters here before calling `sgtest`
    %   script to run an experiment. Refer to the CyPhy 2016 paper to
    %   understand various "phases" of experiment.
    
    properties(Constant = true)
        
        % Frequently-used options
                
        NUM_TESTS = 1000;                       % Number of random models to generate (and use in differntial testing) ����ģ������ԭ150
        
        NUM_BLOCKS = [250 300];                 % ������Χ
        
        COMPARE_SIM_RESULTS = false;         % Compare simulation results obtained by logging signals ("Compare" phases) �ȽϷ�����
        
        CLOSE_MODEL = true;                    % Close models after experiment  ���к�ر�ģ��
        PAUSE_BETWEEN_FIX_ERROR_STEPS = false;
        STOP_IF_ERROR = false;                  % Stop the script when meet the first simulation error �������󱨴�ֹͣ
        STOP_IF_DTC_ERROR = false;           % Data type conversion from typesmart analysis ��������ת������ʱֹͣ
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        SOLVER_TYPE = 'Fixed-step';
%        SOLVER_TYPE = 'Variable-step';
        
        CSMITH_CREATE_C = false;                % Whether to call Csmith to create C files. Set to False if reproducing previous experiment.
        
        SIMULATE_MODELS = true;                 % To invoke "Analyze Model" and "Fix Errors" phase 

        LOG_SIGNALS = false;                         % Log all block-output signals for comparison ("Log Signals" phase). Note: it disregards `USE_PRE_GENERATED_MODEL` setting.

        USE_PRE_GENERATED_MODEL = [];         % If non-empty and a string, then instead of generating random model, will use value of this variable (already generated model) in log signal/comparison phases.   
%          USE_PRE_GENERATED_MODEL = 'sampleModel246';  % Instead of randomly
%          generating model will use this particular model for further
%          phases of CyFuzz

        LOAD_RNG_STATE = false;                  % Set this `true` if we want to create NEW models each time the script is run. Set to `false` if generating same models at each run of the script is desired. For first time running in a new computer set to false, as this will fail first time if set to true.

        SKIP_IF_LAST_CRASHED = false;            % Skip one model if last time Matlab crashed trying to run the same model.
        
        STOP_IF_OTHER_ERROR = true;             % Stop the script for errors not related to simulation e.g. unhandled exceptions or code bug. ALWAYS KEEP IT TRUE to detect my own bugs.

        CLOSE_OK_MODELS = true;                % Close "OK" models (refer to CyPhy paper)
        
        FINAL_CLEAN_UP = true;                 % Will delete models and related artifacts (e.g. binaries) for the model

        GENERATE_TYPESMART_MODELS = false;      % Will create models that respects data-type compatibility between blocks.
        ELIMINATE_FEEDBACK_LOOPS = true;
        
        CHILD_MODEL_NUM_BLOCKS = [1 5];
        SUBSYSTEM_NUM_BLOCKS = [1 5];
        IF_ACTION_SUBSYS_NUM_BLOCKS = [1 5];
        
        MAX_HIERARCHY_LEVELS =3;               % Minimum value is 1 indicating a flat model with no hierarchy.��νṹΪ����

        SAVE_ALL_ERR_MODELS = true;             % Save the models which we can not simulate 
        LOG_ERR_MODEL_NAMES = true;             % Log error model names keyed by their errors
        SAVE_COMPARE_ERR_MODELS = true;         % Save models for which we got signal compare error after diff. testing
        SAVE_SUCC_MODELS = true;                % Save successful simulation models in a folder

        PAUSE_BETWEEN_CYCLE_REMOVING = false;
        PRESENTATION_MODE = false;   % Pause between various CyFuzz phases.
        
        PAUSE_AFTER_THIS_SUBSYSTEM = {};

        USE_SIGNAL_LOGGING_API = true;          % If true, will use hdlsllib's Signal Logging API, otherwise adds Outport blocks to each block of the top level model
        SIMULATION_MODE = {'accelerator'};      % See 'SimulationMode' parameter in http://bit.ly/1WjA4uE
        COMPILER_OPT_VALUES = {'off'};          % Compiler opt. values of Accelerator and Rapid Accelerator modes

        BREAK_AFTER_COMPARE_ERR = true;
        
        SL_SIM_TIMEOUT = 300;                   % After these many seconds give up testing the model and mark as Timed-Out model
        
        % Will only use following SL libraries/blocks. If this is a
        % library, set `is_blk` false. Set true for blocks.
        
        SL_BLOCKLIBS = {
           struct('name', 'Logic and Bit Operations', 'is_blk', false, 'num', 0.05)
           %struct('name', 'Discrete', 'is_blk', false, 'num', 0.05)
%             struct('name', 'Continuous', 'is_blk', false,  'num', 0.1)
             struct('name', 'Math Operations', 'is_blk', false,  'num', 0.83)
%             struct('name', 'Logic and Bit Operations', 'is_blk', false,  'num', 0.08)
            struct('name', 'Sinks', 'is_blk', false, 'num', 0.02)
            struct('name', 'Sources', 'is_blk', false, 'num', 0.02)
            %struct('name', 'hdlsllib/Sources/Constant', 'is_blk', true, 'num', 0.06)
            struct('name', 'hdlsllib/Ports & Subsystems/Subsystem', 'is_blk', true, 'num', 0.04)
           struct('name', 'hdlsllib/Signal Routing/Switch', 'is_blk', true, 'num', 0.04)
         %   struct('name', 'hdlsllib/Ports & Subsystems/Model', 'is_blk', true, 'num', 0.05)
        };
    
        % Won't use following SL blocks in generated models:
    
        SL_BLOCKS_BLACKLIST = {
            'hdlsllib/Sources/From File'
            'hdlsllib/Sources/Signal Editor'
            'hdlsllib/Sources/Signal Builder' % zero output without config
            'hdlsllib/Sources/WaveformGenerator' % zero output without config
            'hdlsllib/Sources/In1' % zero in top level
            'hdlsllib/Sources/FromWorkspace'
            'hdlsllib/Sources/EnumeratedConstant'
            'hdlsllib/Sources/FromSpreadsheet'
            'hdlsllib/Sources/InBusElement'
            'hdlsllib/Discrete/Discrete Derivative'
            'hdlsllib/Discrete/Resettable Delay'                        % For testing DFT analysis
            'hdlsllib/Math Operations/Trigonometric Function'
            'hdlsllib/Math Operations/MatrixMultiply'
            'hdlsllib/Math Operations/Decrement Real World'
            'hdlsllib/Math Operations/Assignment'
            'hdlsllib/Math Operations/Product'
            'hdlsllib/Math Operations/Product of Elements'
            'hdlsllib/Math Operations/Reciprocal Sqrt'
            'hdlsllib/Math Operations/Sqrt'
            'hdlsllib/Math Operations/Reciprocal'
            'hdlsllib/Math Operations/Math Function'
            'hdlsllib/Math Operations/Increment Stored Integer'
            'hdlsllib/Math Operations/Decrement Stored Integer'
            'hdlsllib/Math Operations/Real-Imag to Complex'
            'hdlsllib/Math Operations/Unary Minus'
            'hdlsllib/Math Operations/Sqrt'
            'hdlsllib/Continuous/VariableTransport Delay'
            'hdlsllib/Continuous/VariableTime Delay'
            'hdlsllib/Continuous/Transport Delay'
            'hdlsllib/Sinks/StopSimulation'
            'hdlsllib/Sinks/To File'                              % Signal logging conflicts in TACC?
            'hdlsllib/Discrete/First-OrderHold'
            'hdlsllib/Discrete/Memory'
            'hdlsllib/Math Operations/Algebraic Constraint'
            'hdlsllib/Math Operations/Matrix Concatenate' % Outputs 2d signal
            'hdlsllib/Math Operations/Vector Concatenate' % Outputs 2d signal
            'hdlsllib/Math Operations/Real-Imag To Complex' % Outputs complex signal
            'hdlsllib/Math Operations/Magnitude-Angle To Complex' % Outputs complex signal
            'hdlsllib/Math Operations/Signed Sqrt' % data type prop - float only
            'hdlsllib/Logic and Bit Operations/Interval Test Dynamic' % uses the `Data Type Duplicate` block
            'hdlsllib/Logic and Bit Operations/Bit Rotate'
            'hdlsllib/Logic and Bit Operations/Bits to Word'
            'hdlsllib/Logic and Bit Operations/Word to Bits'
        };
    
        % ALLOW LIST: LOOKS LIKE ALLOW_LIST IS NOT IMPLEMENTED.
    
        LOG_SOLVERS_USED = true;    % Log which solvers were used

        SAVE_SIGLOG_IN_DISC = true; % Persistently save logged signals in dic

        DELETE_MODEL = true;    % Delete the model from working directory after testing 
        
        REPORTSNEO_DIR = 'reportsneo';  % Reports will be stored in this directory
        
        STOP_IF_LISTED_ERRORS = true;  % If any of the errors from the list below occurs, break even if STOP_IF_ERROR == false.
        STOP_ERRORS_LIST = {};
%         STOP_ERRORS_LIST = {'hdlsllib:Engine:BlkWithPortInLoop'};
        
%         STOP_ERRORS_LIST = {'hdlsllib:Engine:SolverConsecutiveZCNum', 'hdlsllib:blocks:SumBlockOutputDataTypeIsBool'};

%         CONTINUE_ERRORS_LIST = {'SL:RandGen:TestTerminatedWithoutExceptions'};                      % Don't stop sgtest if these errors occur.
        CONTINUE_ERRORS_LIST = {'hdlsllib:Engine:ExtraModelrefNoncontSignal'};                      % Don't stop sgtest if these errors occur.
    
    
        % Subsystem/hierarchy model related
        
        HIERARCHY_NEW_MAX_ATTEMPT = 5;
        HIERARCHY_NEW_OLD_RATIO = {struct('name', 'new', 'num', 0.7)
            struct('name', 'old', 'num', 0.3)
        };
    
        % EMI Related
        
        EMI_TESTING = false;
        NUM_STATIC_EMI_VARS = 3;
        
        % Drawing specific
        
        NUM_BLOCKS_IN_A_ROW = 10;

        % Debugging Related
        
        PRINT_BLOCK_CONNECTION = false;
        PRINT_BLOCK_CONFIG = false;
        
        STOP_BEFORE_SIMULATION = false;  % To return abruptly before iterative simulations in the "Fix Errors" phase
        PRINT_TYPESMART = true; % Print debugging info regarding typesmart analysis
        
        % Don't change folllowing
        
        BLOCK_NAME_PREFIX = 'cfblk';
        
        SUBSYSTEM_FIX = true;
    
    end
    
    
    methods(Static)
      function print_warnings
                    
         if ~ cfg.SIMULATE_MODELS
            warning('Generated models were Not Simulated!');
         end
          
         if ~ cfg.LOG_SIGNALS
            warning('Signal Logging was not enabled!');
         end
         
         if ~ cfg.COMPARE_SIM_RESULTS
            warning('Comparison Framework was not run!');
         end
         
         
      end
    end
    
    methods
    end
    
end

