# v 4.4
# Converts PCBP_name to proper CBP_name files

import sys
import textwrap
import subprocess
import os
import CBPCompile

# Reads PCBP.cfg file

flagDict = {}

# If one is none, give error and state what is none
# os.chdir(os.path.dirname(sys.argv[0]))
# print(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
# print(os.path.dirname(os.path.realpath(__file__)))

os.chdir(os.path.dirname(os.path.realpath(__file__)))


try:
    CFGSplitList = open('PCBP.ini', 'r').read().split('\n')
    for s in CFGSplitList:
        if '=' in s:
            CFGCalcList = s.split('=')
            if CFGCalcList[1] == 'True':
                flagDict[CFGCalcList[0]] = True
            elif CFGCalcList[1] == 'False':
                flagDict[CFGCalcList[0]] = False
            else:
                flagDict[CFGCalcList[0]] = CFGCalcList[1]
            if flagDict[CFGCalcList[0]] == '':
                print('ERROR: Missing value in name: {} in the PCBP.ini file:'.format(CFGCalcList[0]))
                sys.exit()
    # print(CFGSplitList)
    # print(flagDict)

except FileNotFoundError:
    print('ERROR: File could not be found: PCBP.ini')
    sys.exit()

except TypeError:
    print('ERROR: Unknown parsing error')
    sys.exit()

# CBPOutput = CBPStart_2.CBPOutput
# serverOption = CBPStart_2.serverOption

lenNumber = 32500
multiParseOption = False

regFilePath = flagDict['regFilePath']
CBPDirectory = flagDict['CBPDirectory']
PCBPIDirectory = flagDict['PCBPIDirectory']
PCBPTFilePath = flagDict['PCBPTFilePath']
CBPOutput = flagDict['CBPOutput']
serverOption = flagDict['serverOption']

regBaseFile = os.path.basename(flagDict['regFilePath'])

tpFlag = False

# Deletes the file before starting
open(PCBPTFilePath, 'w').close()

if regBaseFile[:6] == 'PCBPM_':
    # print('PCBPM_ True')
    multiParseOption = True
    CBPSplitList = []
    generalCompileList = []
    CBPOpen = None

    try:
        CBPSplitList = open(regFilePath, 'r').read().split('\n')
        # print(CBPSplitList)

        for i, s in enumerate(CBPSplitList):
            if s[:8] == '-tp True':
                tpFlag = True
                del CBPSplitList[i]
            elif s[:3] == '-tp':
                tpFlag = False
                del CBPSplitList[i]

        CBPOpen = True

    except FileNotFoundError:
        print('ERROR: File could not be found: {}'.format(regBaseFile))

    except TypeError:
        print('ERROR: Unknown parsing error while parsing {}')

    finally:
        if CBPOpen:
            open(regFilePath, 'r').close()
            print('File found: {}\n'.format(regBaseFile))

    for s in CBPSplitList:
        # print(s[:2])
        # Comments can be added on the PCBPM file using '//'
        if not s.isspace() and s and s[:2] != '//':
            # print('MARKER')
            # print(s)
            doc = CBPCompile.PCBPCompile(s)
            doc.generalCompile(CBPDirectory, PCBPIDirectory, serverOption, lenNumber, CBPOutput)
            doc.CBPTempFile(PCBPTFilePath, tpFlag)

if multiParseOption == False:
    # print('PCBPM_ False')
    doc = CBPCompile.PCBPCompile(regFilePath)
    doc.generalCompile(CBPDirectory, PCBPIDirectory, serverOption, lenNumber, CBPOutput)
    doc.CBPTempFile(PCBPTFilePath, tpFlag)
