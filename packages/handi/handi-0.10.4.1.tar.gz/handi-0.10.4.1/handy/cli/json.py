import sys

from handy.jzon.handler import load,save
from handy.dict.mixedict import delkey, findkey, isin, rmempty, replkey, replvalue
from ._constants import msg_file_not_found

msg_help_chkey = "Written by junying, 2019-04-29 \
                 \nComment: to check if the query key exists or not in the file.\
                 \nUsage: chkey [keyname] [inpath]"
def chKey():
    if len(sys.argv) < 3: print(msg_help_chkey); return
    try: indata = load(sys.argv[2])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    if not isin(indata,sys.argv[1]): print("no found!")
    else: print("found!!!")
    
msg_help_delkey = "Written by junying, 2019-04-29 \
                  \nComment: to delete a specific key in a json file.\
                  \nUsage: delkey [key] [inpath] [outpath]"

from ._constants import msg_no_output, yes_symbols, no_symbols,print_symbols,int_symbols

def delKey():
    if len(sys.argv) < 3: print(msg_help_delkey); return
    elif len(sys.argv) == 3:
        answer = raw_input(msg_no_output) if sys.version_info[0] == 2 else input(msg_no_output)
        if not answer or any(symbol in answer[0] for symbol in yes_symbols): outpath=sys.argv[2]
        elif any(symbol in answer[0] for symbol in no_symbols): return
        else: outpath = answer
    else: outpath = sys.argv[3]
    try: indata = load(sys.argv[2]); key = sys.argv[1]
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    delkey(indata,key); rmempty(indata); save(indata,outpath)

msg_help_findkey = "Written by junying, 2019-05-09 \
                   \nComment: return the value of a specific key in a json file.\
                   \nUsage: findkey [keyname] [inpath]"
def findKey():
    if len(sys.argv) < 3: print(msg_help_findkey); return
    try: indata = load(sys.argv[2])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    if not isin(indata,sys.argv[1]): print("no found!")
    else:
        for value in findkey(indata,sys.argv[1]): print(value)

msg_help_printkey = "Written by junying, 2019-05-09 \
                   \nComment: print content of list with a specific key as requested values.\
                   \nUsage: printkey [keyname] [inpath] [subkey1] [subkey2] "
# This function is developed for htdf production export purpose.
def printKey():
    if len(sys.argv) < 4: print(msg_help_printkey); return
    try: indata = load(sys.argv[2])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    if not isin(indata,sys.argv[1]): print("no found!")
    else:
        for value in findkey(indata,sys.argv[1]):
            if not isinstance(value,list): print("the corresponding value is not list!");break
            for item in value:
                if not isinstance(item,dict): continue
                output=""
                for index in range(3,len(sys.argv)):
                    subkey = sys.argv[index]
                    if not isin(item,subkey): continue
                    subvalue=findkey(item,subkey)
                    try:
                        output+=" %s"%str(subvalue)
                    except:
                        continue
                print(output)
                
msg_help_rmempty = "Written by junying, 2019-04-29 \
                   \nComment: remove keys with the empty values. \
                              and to humanize it.\
                   \nUsage: rmempty [inpath] [outpath]"
            
def rmEmpty():
    if len(sys.argv) < 2: print(msg_help_rmempty); return
    elif len(sys.argv) == 2:
        answer = raw_input(msg_no_output) if sys.version_info[0] == 2 else input(msg_no_output)
        if not answer or any(symbol in answer[0] for symbol in yes_symbols): outpath=sys.argv[1]
        elif any(symbol in answer[0] for symbol in no_symbols): return
        else: outpath = answer
    else: outpath = sys.argv[2]
    # load
    try: indata = load(sys.argv[1])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    # process
    rmempty(indata)
    # save
    save(indata,outpath)

msg_help_rmempty = "Written by junying, 2019-04-29 \
                   \nComment: beautify a json file human-readable.\
                   \nUsage: beautifyjson [inpath] [outpath]"
def beautify():
    if len(sys.argv) < 2: print(msg_help_rmempty); return
    elif len(sys.argv) == 2:
        answer = raw_input(msg_no_output) if sys.version_info[0] == 2 else input(msg_no_output)
        if not answer or any(symbol in answer[0] for symbol in yes_symbols): outpath=sys.argv[1]
        elif any(symbol in answer[0] for symbol in no_symbols): return
        else: outpath = answer
    else: outpath = sys.argv[2]
    # load
    try: indata = load(sys.argv[1])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    # save
    save(indata,outpath)    

msg_help_replkey = "Written by junying, 2019-08-05 \
                   \nComment: set the value of a specific key as A.\
                   \nUsage: replkey [key] [value] [inpath] [outpath/symbol]\
                   \nSymbols: Yes[y,Y], No[n,N], Print[p,P], Int[i,I]"
                 
def replKey():
    if len(sys.argv) < 4: print(msg_help_replkey); return
    elif len(sys.argv) == 4:
        answer = raw_input(msg_no_output) if sys.version_info[0] == 2 else input(msg_no_output)
        if not answer or any(symbol in answer[0] for symbol in yes_symbols): outpath=sys.argv[3]
        elif any(symbol in answer[0] for symbol in no_symbols): return
        else: outpath = answer
    elif len(sys.argv[4]) == 1: answer=sys.argv[4];outpath=sys.argv[3]
    else: outpath = sys.argv[4]
    # load
    try: indata = load(sys.argv[3])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    # process
    if answer and any(symbol in answer[0] for symbol in int_symbols):
        replkey(indata,sys.argv[1],int(sys.argv[2]))
    else: replkey(indata,sys.argv[1],sys.argv[2])
    # save
    if answer and any(symbol in answer[0] for symbol in print_symbols): print(indata); return
    else: save(indata,outpath)
    
msg_help_replvalue = "Written by junying, 2019-08-05 \
                    \nComment: replace the value of a specific key from A to B.\
                    \nUsage: replvalue [key] [value(src)] [value(dest)] [inpath] [outpath/symbol]"
                 
def replValue():
    if len(sys.argv) < 5: print(msg_help_replvalue); return
    elif len(sys.argv) == 5:
        answer = raw_input(msg_no_output) if sys.version_info[0] == 2 else input(msg_no_output)
        if not answer or any(symbol in answer[0] for symbol in yes_symbols): outpath=sys.argv[4]
        elif any(symbol in answer[0] for symbol in no_symbols): return
        else: outpath = answer
    elif len(sys.argv[5]) == 1: answer=sys.argv[5];outpath=sys.argv[4]
    else: outpath = sys.argv[5]
    # load
    try: indata = load(sys.argv[4])
    except: return "No JSON object could be decoded"
    if not indata: print(msg_file_not_found); return
    # process
    replvalue(indata,sys.argv[1],sys.argv[2],sys.argv[3])
    # save
    if answer and any(symbol in answer[0] for symbol in print_symbols): print(indata); return
    else: save(indata,outpath)