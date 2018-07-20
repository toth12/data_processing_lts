import pdb

def create_dictionary_of_file_list(filelist):
    result={}
    
    for file in filelist:
        original_filename = file.split('/')[-1]
        rg_number=original_filename.split("_")[0]

        # find last occurrence of '.' and replace it with '*' 
        k = rg_number.rfind(".")
        mongo_rg = rg_number[:k] + "*" + rg_number[k+1:]

        #check if already in the list

        if mongo_rg not in result.keys():
            result[mongo_rg]=[file]


        else:
            
            result[mongo_rg].append(file)

    #make sure that transcripts are in correct order
    
    for element in result:
        if len(result[element])>1:
            position={}
            for f in result[element]:
                pos=f.split('/')[-1].split('_')[1][-1]
                position[int(pos)]=f
            possible_positions=sorted(position.keys())
            reordered=[position[i] for i in possible_positions]
            result[element]=reordered
            
    return result
