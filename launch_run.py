from Server import Server
import csv
import multiprocessing
import os
current_directory = os.path.dirname(os.path.realpath(__file__))

def main(scope, prepare = False):
    size = float(len(scope))
    if prepare:
        new_scope = prepare_input(scope)
    else:
        new_scope = scope

    if len(new_scope)>=50:
        pool = multiprocessing.Pool(50)
    else:
        pool = multiprocessing.Pool(len(new_scope))
        
    future_list = pool.imap_unordered(launch, new_scope)
    count = 0
    for future in future_list:
        try:
            print("Completed "+future)
            count+=1
            print("Completed {0}%".format(count*100/size))
        except:
            pass

def launch(input_tuple):
    lsm_name = input_tuple[0]
    lsm_ip = input_tuple[1]
    target = input_tuple[2]
    #print(target)
    session = Server(lsm_name, lsm_ip)
    #try:
	#session.connect() 
	#session.upload_code_file(current_directory+"/Lib/PLD.zip", "pld.zip")
	#session.extract_remote_code(session.get_remote_file(), "PLD") 
	#session.upload_input_file(current_directory+"/Lib/"+target, "Input.csv")  
	#session.run("start.py", session.get_remote_folder()) 
	#session.download([(session.get_remote_folder()+"/LOGS",current_directory+'/Report/'),(session.get_remote_folder()+"/STATUS",current_directory+'/Status/')]) 
	#session.close_and_clean(session.get_remote_folder())
	#return "Done running on {0}".format(lsm_name)
    #except Exception as e:
	#print(e)
	#return "Error Running Script at {0}".format(lsm_name)
    return "Done running on {0}".format(lsm_name) if session.connect() and session.upload_code_file(current_directory+"/Lib/PLD.zip", "pld.zip") and session.extract_remote_code(session.get_remote_file(), "PLD") and session.upload_input_file(current_directory+"/Lib/"+target, "Input.csv")  and session.run("start.py", session.get_remote_folder()) and session.download([(session.get_remote_folder()+"/LOGS",current_directory+'/Report/'),(session.get_remote_folder()+"/STATUS",current_directory+'/Status/')]) and session.close_and_clean(session.get_remote_folder()) else "Error Running Script at {0}".format(lsm_name) 
    
   

def prepare_input(scope):
    input_list = list()
    for key, value in scope.items():
        fname = key
        f = open(os.path.join("Lib", fname), "wb")
        fc = csv.writer(f)
        ip = None
        for row in value:
            ip = row[0]
            fc.writerow(row[1])
        input_list.append((key, ip, fname))
        f.close()
    return input_list

if __name__ == '__main__':
    input_file = "Input.csv"
    inp = input("By default this tool take Input.csv as Input. Enter to continue or give Input file name: ")
    if inp.strip() != "":
        input_file = inp
    f = open(input_file, 'rb')
    fc = csv.reader(f)
    header = next(fc)
    scope = dict()
    try:
        for row in fc:
            if row[0].strip() in scope:
                scope[row[0].strip()].append((row[1], row[2:]))
            else:
                scope[row[0].strip()] = [(row[1], row[2:])]
    except IndexError:
        print ("Invalid Input")
    f.close()
    main(scope, True)
    
