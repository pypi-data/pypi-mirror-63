# -*- coding: utf-8 -*-


# FuzzyClassificator - this program uses neural networks to solve classification problems,
# and uses fuzzy sets and fuzzy logic to interpreting results.
# Copyright (C) 2017, Timur Gilmullin
# e-mail: tim55667757@gmail.com


# Main runner. See help for usages. CLI-interaction supported.


import argparse

from PyBrainLearning import *
from FuzzyRoutines import *
from FCLogger import *


def Version(onlyPrint=False):
    """
    Return current version of FuzzyClassificator build
    """
    import pkg_resources  # part of standart setuptools

    try:
        version = pkg_resources.get_distribution('FuzzyClassificator').version

    except Exception:
        return 'unknown'

    if onlyPrint:
        FCLogger.level = 50
        print(version)

    return version


# Constants and Global variables:

__version__ = Version()  # set version of current FuzzyClassificator build

ethalonsDataFile = 'ethalons.dat'  # File with ethalon data samples.
candidatesDataFile = 'candidates.dat'  # File with candidates data samples.
neuroNetworkFile = 'network.xml'  # File with Neuro Network configuration.
reportDataFile = 'report.txt'  # Report file with classification analysis.
bestNetworkFile = 'best_nn.xml'  # Best network during the learns.
bestNetworkInfoFile = 'best_nn.txt'  # File with information about best network during the learns.

epochsToUpdate = 5  # Epochs between error status updated.

ignoreColumns = []  # List of ignored columns in input files.
ignoreRows = [1]  # List of ignored rows in input files.
sepSymbol = '\t'  # Separator symbol.

reloadNetworkFromFile = False  # Reload or not Neuro Network from file before usage.
noFuzzyOutput = False  # Show results with fuzzy values if False, otherwise show real values.
showExpected = False  # Show expected results in Classify mode. WARNING! Use only if your dat-file contains columns with expected results to avoid errors!


def ParseArgsMain(notAPI=True):
    """
    Function get and parse command line keys.
    """
    parser = argparse.ArgumentParser()  # command-line string parser

    parser.description = 'FuzzyClassificator version: {}. This program uses neural networks to solve classification problems, and uses fuzzy sets and fuzzy logic to interpreting results. FuzzyClassificator provided under the MIT License.'.format(__version__)
    parser.epilog = 'See examples on GitHub: https://devopshq.github.io/FuzzyClassificator/'

    parser.add_argument('-v', '--version', action='store_true', help='Show current version of FuzzyClassificator.')

    parser.add_argument('-l', '--debug-level', type=str, help='Use 1, 2, 3, 4, 5 or DEBUG, INFO, WARNING, ERROR, CRITICAL debug info verbosity, INFO (2) by default.')
    parser.add_argument('-e', '--ethalons', type=str, help='File with ethalon data samples, ethalons.dat by default.')
    parser.add_argument('-c', '--candidates', type=str, help='File with candidates data samples, candidates.dat by default.')
    parser.add_argument('-n', '--network', type=str, help='File with Neuro Network configuration, network.xml by default.')
    parser.add_argument('-r', '--report', type=str, help='Report file with classification analysis, report.txt by default.')
    parser.add_argument('-bn', '--best-network', type=str, help='Copy best network to this file, best_nn.xml by default.')
    parser.add_argument('-bni', '--best-network-info', type=str, help='File with information about best network, best_nn.txt by default.')

    parser.add_argument('-ic', '--ignore-col', type=str, help='Column indexes in input files that should be ignored. Use only dash and comma as separator numbers, other symbols are ignored. Example (no space after comma): 1,2,5-11')
    parser.add_argument('-ir', '--ignore-row', type=str, help='Row indexes in input files that should be ignored. Use only dash and comma as separator numbers, other symbols are ignored. 1st raw always set as ignored. Example (no space after comma): 2,4-7')
    parser.add_argument('-sep', '--separator', type=str, help='Separator symbol in raw data files. SPACE and TAB are reserved, TAB used by default.')
    parser.add_argument('--no-fuzzy', action='store_true', help='Do not show fuzzy results, only real. False by default.')
    parser.add_argument('--show-expected', action='store_true', help='Show expected results in Classify mode. WARNING! Use only if your dat-file contains columns with expected results!')
    parser.add_argument('--reload', action='store_true', help='Reload network from file before usage, False by default.')
    parser.add_argument('-u', '--update', type=int, help='Update error status after this epochs time, 5 by default. This parameter affected training speed.')

    parser.add_argument('--learn', type=str, nargs='+', help='Start program in learning mode with options (no space after comma): config=<inputs_num>,<layer1_num>,<layer2_num>,...,<outputs_num> epochs=<int_number> rate=<float_num> momentum=<float_num> epsilon=momentum=<float_num> stop=momentum=<float_num>')
    parser.add_argument('--classify', type=str, nargs='+', help='Start program in classificator mode with options (no space after comma): config=<inputs_num>,<layer1_num>,<layer2_num>,...,<outputs_num>')

    cmdArgs = parser.parse_args()
    if notAPI and not cmdArgs.version and ((cmdArgs.learn and cmdArgs.classify) or (not cmdArgs.learn and not cmdArgs.classify)):
        parser.print_help()
        sys.exit()

    return cmdArgs


def LMStep1CreatingNetworkWithParameters(**kwargs):
    """
    This function realize Learning mode step:
    1. Creating PyBrain network instance with pre-defined config parameters.
    **kwargs are console parameters with user-define values.
    Function returns instance of PyBrain network.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 1. Creating PyBrain network instance with pre-defined config parameters.')

    # Create default config:
    config = ()  # network configuration
    epochs = 10  # epochs of learning
    rate = 0.05  # learning rate
    momentum = 0.01  # momentum of learning
    epsilon = 0.05  # epsilon used to compare the distance between the two vectors (may be with fuzzy values)
    stop = 5  # stop parameter

    # Updating config:
    if 'config' in kwargs.keys():
        try:
            # Parsing Neural Network Config parameter that looks like "config=inputs,layer1,layer2,...,outputs":
            config = tuple(int(par) for par in kwargs['config'].split(','))  # config for FuzzyNeuroNetwork

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Incorrect neural network config! Parameter config must looks like tuple of numbers: config=inputs,layer1,layer2,...,outputs')

    if 'epochs' in kwargs.keys():
        try:
            epochs = int(kwargs['epochs'])

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Epoch parameter might be an integer number greater or equal 1!')

    if 'rate' in kwargs.keys():
        try:
            rate = float(kwargs['rate'])

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Rate parameter might be a float number greater than 0 and less or equal 1!')

    if 'momentum' in kwargs.keys():
        try:
            momentum = float(kwargs['momentum'])

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Momentum parameter might be a float number greater than 0 and less or equal 1!')

    if 'epsilon' in kwargs.keys():
        try:
            epsilon = float(kwargs['epsilon'])

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Epsilon parameter might be a float number greater than 0 and less or equal 1!')

    if 'stop' in kwargs.keys():
        try:
            stop = float(kwargs['stop'])

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Stop parameter might be a float number greater than 0 and less or equal 100!')

    fNetwork = FuzzyNeuroNetwork()  # create network

    if noErrors:
        try:
            fNetwork.networkFile = neuroNetworkFile
            fNetwork.rawDataFile = ethalonsDataFile
            fNetwork.reportFile = reportDataFile
            fNetwork.bestNetworkFile = bestNetworkFile
            fNetwork.bestNetworkInfoFile = bestNetworkInfoFile
            fNetwork.config = config
            fNetwork.epochsToUpdate = epochsToUpdate

            if ignoreColumns:
                fNetwork.ignoreColumns = ignoreColumns  # set up ignored columns

            if ignoreRows:
                fNetwork.ignoreRows = ignoreRows  # set up ignored rows

            if sepSymbol:
                fNetwork.separator = sepSymbol  # set up separator symbol between columns in raw data files

            if epochs >= 0:
                fNetwork.epochs = epochs  # set up epochs of learning

            if rate:
                fNetwork.learningRate = rate  # set up learning rate parameter

            if momentum:
                fNetwork.momentum = momentum  # set up momentum of learning parameter

            if epsilon:
                fNetwork.epsilon = epsilon  # set up epsilon parameter

            if stop:
                fNetwork.stop = stop  # set up stop parameter

            FCLogger.debug('Instance of fuzzy network initialized with parameters:')
            FCLogger.debug('    {}'.format(kwargs))
            FCLogger.debug('File with ethalons data: {}'.format(os.path.abspath(fNetwork.rawDataFile)))
            FCLogger.debug('File for saving Neuronet: {}'.format(os.path.abspath(fNetwork.networkFile)))
            FCLogger.debug('Classification Report file: {}'.format(os.path.abspath(fNetwork.reportFile)))
            FCLogger.debug('For measurements used fuzzy scale:')

            for line in str(fNetwork.scale).split('\n'):
                FCLogger.debug(line)

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Failed to initialize the fuzzy network!')

    if noErrors:
        return fNetwork

    else:
        return None


def LMStep2ParsingRawDataFileWithEthalons(fNetwork):
    """
    This function realize Learning mode step:
    2. Parsing raw data file with ethalons.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 2. Parsing raw data file with ethalons.')

    fNetwork.ParseRawDataFile()

    if not fNetwork.rawData or not fNetwork.rawDefuzData:
        noErrors = False

    return noErrors


def LMStep3PreparingPyBrainDataset(fNetwork):
    """
    This function realize Learning mode step:
    3. Preparing PyBrain dataset.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 3. Preparing PyBrain dataset.')

    fNetwork.PrepareDataSet()

    if not fNetwork.dataSet:
        noErrors = False

    return noErrors


def LMStep4InitializePyBrainNetworkForLearning(fNetwork):
    """
    This function realize Learning mode step:
    4. Initialize empty PyBrain network for learning or reading network configuration from file.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 4. Initialize empty PyBrain network for learning or reading network configuration from file.')

    if reloadNetworkFromFile:
        fNetwork.LoadNetwork()  # reload old network for continuing training

    else:
        fNetwork.CreateNetwork()

    if not fNetwork.network:
        noErrors = False

    return noErrors


def LMStep5CreatingPyBrainTrainer(fNetwork):
    """
    This function realize Learning mode step:
    5. Creating PyBrain trainer.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 5. Creating PyBrain trainer.')

    fNetwork.CreateTrainer()

    if not fNetwork.trainer:
        noErrors = False

    return noErrors


def LMStep6StartsLearningAndSavingNetworkConfigurationToFile(fNetwork):
    """
    This function realize Learning mode step:
    6. Starts learning and saving network configuration to file.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    FCLogger.info(sepShort)
    FCLogger.info('Step 6. Starts learning and saving network configuration to file.')

    noErrors = fNetwork.Train()  # train and receive finish status

    return noErrors


def LearningMode(**inputParameters):
    """
    Main function to work with input learn data and prepare neural network.
    Learning mode contain steps:
    1. Creating PyBrain network instance with pre-defined config parameters.
    2. Parsing raw data file with ethalons.
    3. Preparing PyBrain dataset.
    4. Initialize empty PyBrain network for learning or reading network configuration from file.
    5. Creating PyBrain trainer.
    6. Starts learning and saving network configuration to file.
    """
    successFinish = False  # success Learning Mode finish flag

    FCLogger.info(sepLong)
    FCLogger.info('FuzzyClassificator version: {}'.format(__version__))
    FCLogger.info('Learning mode activated.')
    FCLogger.info('Log file: {}'.format(os.path.abspath(fileLogHandler.baseFilename)))

    fNetwork = LMStep1CreatingNetworkWithParameters(**inputParameters)

    if fNetwork:
        if LMStep2ParsingRawDataFileWithEthalons(fNetwork):
            if LMStep3PreparingPyBrainDataset(fNetwork):
                if LMStep4InitializePyBrainNetworkForLearning(fNetwork):
                    if LMStep5CreatingPyBrainTrainer(fNetwork):
                        if LMStep6StartsLearningAndSavingNetworkConfigurationToFile(fNetwork):
                            successFinish = True

    if successFinish:
        FCLogger.info(sepShort)
        FCLogger.info('Successful finish all Learning steps.')

        fNetwork.ClassificationResults(fullEval=True, needFuzzy=not(noFuzzyOutput))

    else:
        FCLogger.info(sepShort)
        FCLogger.critical('Learning finished with some errors!')

    FCLogger.info('Learning mode deactivated.')

    return successFinish


def CMStep1CreatingPyBrainNetwork(**kwargs):
    """
    This function realize Classifying mode step:
    1. Creating PyBrain network instance.
    Function returns instance of PyBrain network.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 1. Creating PyBrain network instance.')

    fNetwork = None
    config = ()  # network configuration

    if 'config' in kwargs.keys():
        try:
            # Parsing Neural Network Config parameter that looks like "config=inputs,layer1,layer2,...,outputs":
            config = tuple(int(par) for par in kwargs['config'].split(','))  # config for FuzzyNeuroNetwork

        except Exception:
            noErrors = False
            FCLogger.error(traceback.format_exc())
            FCLogger.error('Incorrect neural network config! Parameter config must looks like tuple of numbers: config=inputs,layer1,layer2,...,outputs')

    try:
        fNetwork = FuzzyNeuroNetwork()  # create network

        fNetwork.config = config
        fNetwork.networkFile = neuroNetworkFile
        fNetwork.rawDataFile = candidatesDataFile
        fNetwork.reportFile = reportDataFile

        if ignoreColumns:
            fNetwork.ignoreColumns = ignoreColumns  # set up ignored columns

        if ignoreRows:
            fNetwork.ignoreRows = ignoreRows  # set up ignored rows

        if sepSymbol:
            fNetwork.separator = sepSymbol  # set up separator symbol between columns in raw data files

        FCLogger.debug('Instance of fuzzy network initialized with parameters:')
        FCLogger.debug('{}'.format(kwargs))
        FCLogger.debug('File with candidates data: {}'.format(os.path.abspath(fNetwork.rawDataFile)))
        FCLogger.debug('File for saving Neuronet: {}'.format(os.path.abspath(fNetwork.networkFile)))
        FCLogger.debug('Classification Report file: {}'.format(os.path.abspath(fNetwork.reportFile)))
        FCLogger.debug('For measurements used fuzzy scale:')

        for line in str(fNetwork.scale).split('\n'):
            FCLogger.debug(line)

    except Exception:
        noErrors = False
        FCLogger.error(traceback.format_exc())
        FCLogger.error('Failed to initialize the fuzzy network!')

    if noErrors:
        return fNetwork

    else:
        return None


def CMStep2ParsingRawDataFileWithCandidates(fNetwork):
    """
    This function realize Classifying mode step:
    2. Parsing raw data file with candidates.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 2. Parsing raw data file with candidates.')

    fNetwork.ParseRawDataFile()

    if not fNetwork.rawData or not fNetwork.rawDefuzData:
        noErrors = False

    return noErrors


def CMStep3LoadingTrainedNetworkFromNetworkConfigurationFile(fNetwork):
    """
    This function realize Classifying mode step:
    3. Loading trained network from network configuration file.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns True if all operations with neural network finished successful.
    """
    noErrors = True  # successful flag
    FCLogger.info(sepShort)
    FCLogger.info('Step 3. Loading trained network from network configuration file.')

    fNetwork.LoadNetwork()  # reload old network for continuing training

    if not fNetwork.network:
        noErrors = False

    return noErrors


def CMStep4ActivatingNetworkForAllCandidateInputVectors(fNetwork):
    """
    This function realize Classifying mode step:
    4. Activating network for all candidate input vectors.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function returns result of classification.
    """
    FCLogger.info(sepShort)
    FCLogger.info('Step 4. Activating network for all candidate input vectors.')

    results = fNetwork.ClassificationResults(fullEval=True, needFuzzy=not(noFuzzyOutput), showExpectedVector=showExpected)

    return results


def CMStep5InterpretingResults(fNetwork, results, fuzzyOutput=True):
    """
    This function realize Classifying mode step:
    5. Interpreting results.
    fNetwork is a PyBrain format neural network, created at 1st step.
    Function creates Classification Report File.
    """
    FCLogger.info(sepShort)
    FCLogger.info('Step 5. Interpreting results.')

    noErrors = fNetwork.CreateReport(results, fuzzyOutput)  # create report file

    return noErrors


def ClassifyingMode(**inputParameters):
    """
    Main function to work with input learn data and prepare neural network.
    Classifying mode contains steps:
    1. Creating PyBrain network instance.
    2. Parsing raw data file with candidates.
    3. Loading trained network from network configuration file.
    4. Activating network for all candidate input vectors.
    5. Interpreting results.
    """
    successFinish = False  # success Classifying mode finish flag

    FCLogger.info(sepLong)
    FCLogger.info('FuzzyClassificator version: {}'.format(__version__))
    FCLogger.info('Classificator mode activated.')
    FCLogger.info('Log file: {}'.format(os.path.abspath(fileLogHandler.baseFilename)))

    fNetwork = CMStep1CreatingPyBrainNetwork(**inputParameters)

    if fNetwork:
        if CMStep2ParsingRawDataFileWithCandidates(fNetwork):
            if CMStep3LoadingTrainedNetworkFromNetworkConfigurationFile(fNetwork):
                classificateResult = CMStep4ActivatingNetworkForAllCandidateInputVectors(fNetwork)
                if classificateResult:
                    if CMStep5InterpretingResults(fNetwork, classificateResult, not(noFuzzyOutput)):
                        successFinish = True

    if successFinish:
        FCLogger.info(sepShort)
        FCLogger.info('Successful finish all Classifying steps.')

    else:
        FCLogger.info(sepShort)
        FCLogger.critical('Classifying finished with some errors!')

    FCLogger.info('Classificator mode deactivated.')

    return successFinish


def Main(learnParameters=None, classifyParameters=None):
    """
    Main function for classification routines.
    learnParameters and classifyParameters are dictionaries with the same parameters as used in CLI. Examples:
    learnParameters = {"config": "3,3,2,2", "epochs": 100, "rate": 0.5, "momentum": 0.5, "epsilon": 0.75, "stop": 1}
    classifyParameters = {"config": "3,3,2,2"}
    If parameters are not defined then CLI-parameters are used.
    """
    global ethalonsDataFile
    global candidatesDataFile
    global neuroNetworkFile
    global reportDataFile
    global bestNetworkFile
    global bestNetworkInfoFile
    global ignoreColumns
    global ignoreRows
    global sepSymbol
    global noFuzzyOutput
    global showExpected
    global reloadNetworkFromFile
    global epochsToUpdate

    notAPI = False if learnParameters or classifyParameters else True  # check if API or CLI work mode
    args = ParseArgsMain(notAPI)  # parse another CLI parameters if they was
    exitCode = 0

    try:
        if args.version:
            Version(onlyPrint=True)  # Show current version of FuzzyClassificator

        if args.debug_level:
            SetLevel(args.debug_level)  # set up FCLogger level

        if args.ethalons:
            ethalonsDataFile = args.ethalons  # raw data for learning

        if args.candidates:
            candidatesDataFile = args.candidates  # raw data for classify

        if args.network:
            neuroNetworkFile = args.network  # file with neural network configuration

        if args.report:
            reportDataFile = args.report  # report file with classification analysis

        if args.best_network:
            bestNetworkFile = args.best_network  # file with best network

        if args.best_network_info:
            bestNetworkInfoFile = args.best_network_info  # file with information about best network

        if args.ignore_col:
            ignoreColumns = DiapasonParser(args.ignore_col)

        if args.ignore_row:
            ignoreRows = DiapasonParser(args.ignore_row)

        if args.separator:
            sepSymbol = args.separator  # separator symbol: TAB, SPACE or another

        if args.no_fuzzy:
            noFuzzyOutput = True

        if args.show_expected:
            showExpected = True

        if args.reload:
            reloadNetworkFromFile = args.reload  # reload neural network from given file before usage

        if args.update:
            epochsToUpdate = args.update  # epochs before error status updating

        #  Execute Learning mode if API or CLI used:
        if learnParameters:
            exitCode = int(not(LearningMode(**learnParameters)))

        elif args.learn:
            exitCode = int(not(LearningMode(**dict(kw.split('=') for kw in args.learn))))

        #  Execute Classifying mode if API or CLI used:
        else:
            if classifyParameters:
                exitCode = int(not(ClassifyingMode(**classifyParameters)))

            elif args.classify:
                exitCode = int(not(ClassifyingMode(**dict(kw.split('=') for kw in args.classify))))

    except Exception:
        FCLogger.error(traceback.format_exc())
        FCLogger.info('FuzzyClassificator work finished with exitCode = 1')
        FCLogger.info(sepLong)

    FCLogger.info('FuzzyClassificator work finished with exitCode = {}'.format(exitCode))
    FCLogger.info(sepLong)

    if notAPI:
        DisableLogger(fileLogHandler)
        sys.exit(exitCode)

    else:
        return exitCode


if __name__ == "__main__":
    Main()
