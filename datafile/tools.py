#! /usr/bin/python
# coding: utf-8
#
# License
#

#from IPython.display import clear_output


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    #clear_output(wait=True)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()



def process_dict(dict, callback):
    for k, v in dict.items():
        if hasattr(v, 'items'):
            process_dict(v, callback)
        else:
            callback(k, v)

def print_dict(d, indent=1):
   for key, value in d.items():
      print('-' * indent +'> '+ str(key))
      if isinstance(value, dict):
         print_dict(value, indent+4)
      #else:
      #   print(':' * (indent+2) + str(len(value)))



