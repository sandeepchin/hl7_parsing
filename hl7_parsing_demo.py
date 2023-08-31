
# Program to demonstrate parsing of hl7 file.
# The format used is VXU 2.5.1 which is a Vaccine Message
# Author: Sandeep Chintabathina

# Libraries needed
import hl7
import pandas as pd

#Function to gather multiple race codes and place in dictionary
def get_race_codes(record,data):
    race_str = str(record.segment('PID')[10])
    # Split repetitions
    tokens = race_str.split('~')
    # Process each race str
    for i in range(0,len(tokens)):
        if (len(tokens[i])>0):
            tokens2 = tokens[i].split('^')
            data['patient_race_code_'+str(i+1)] = tokens2[0]
            data['patient_race_name_'+str(i+1)] = tokens2[1]
    return data

#Function to gather phone and email data
def get_phone_email(record,data):
    phone_str = str(record.segment('PID')[13])
    #Split repetitions
    tokens = phone_str.split('~')
    #Process phone numbers
    for i in range(0,len(tokens)-1):
        area_code=ph_num=''
        if len(tokens[i])>0:
            tokens2 = tokens[i].split('^')
            if tokens2[2]=='PH' or tokens2[2]=='CP':
                area_code ='('+tokens2[5]+')'
                ph_num = tokens2[6]
        data['patient_phone_'+str(i+1)] = area_code+ph_num
    
    #Process email
    tokens2=tokens[i+1].split('^')
    email=''
    if len(tokens2)>2 and tokens2[2]=='Internet':
        email = tokens2[3]
    data['patient_email'] = email
    
    return data
    '''
    #Less generic solution
    area_code=ph_num=''
    if record['PID.13.1.6']!='':
        area_code ='('+record['PID.13.1.6']+')'
        ph_num = record['PID.13.1.7']
    data['patient_phone_1'] = area_code+ph_num
    
    area_code=ph_num=''
    if record['PID.13.2.6']!='':
        area_code ='('+record['PID.13.2.6']+')'
        ph_num = record['PID.13.2.7']
    data['patient_phone_2'] = area_code+ph_num
    
    email=''
    if record['PID.13.3.4']!='':
        email = record['PID.13.3.4']
    data['patient_email'] = email
    return data
    '''
    

# Function to create a dictionary from a hl7 container message
def create_dict(record):
    data={}
    # Pick fields of interest
    data['sending_application']=record['MSH.3.1']
    data['sending_facility']=record['MSH.4.1']
    data['receiving_facility']=record['MSH.6.1']
    data['message_time']=record['MSH.7.1']
    data['message_type'] = record['MSH.9.1']
    data['message_control_id']=record['MSH.10.1']
    data['version_id']=record['MSH.12.1']
    data['patient_id'] = record['PID.3.1']
    data['patient_id_type']=record['PID.3.1.5']
    data['patient_last_name']=record['PID.5.1.1']
    data['patient_first_name']=record['PID.5.1.2']
    data['patient_dob']=record['PID.7.1']
    data['patient_sex']=record['PID.8.1']
    #Get multiple race codes
    data = get_race_codes(record,data)
    data['patient_street_address']=record['PID.11.1.1']
    data['patient_city']=record['PID.11.1.3']
    data['patient_county_code'] = record['PID.11.1.9']
    data['patient_state']=record['PID.11.1.4']
    data['patient_zip']=record['PID.11.1.5']
    data['patient_country']=record['PID.11.1.6']
    #Get patient contact ph and email
    data = get_phone_email(record,data)
    data['patient_ethnicity_code']=record['PID.22.1.1']
    data['patient_ethnicity']=record['PID.22.1.2']
    return data
    

def main(data):
    tokens = data.split('MSH|^~\&|')
    count = 0
    # First token is empty string - so ignore it
    #Store records in a list
    records=[]
    for i in range(1,len(tokens)):
        message = 'MSH|^~\&|'+tokens[i]
        record = hl7.parse(message.replace('\n','\r'))
        count+=1
        #print(record['PID.5.1.2']+' '+record['PID.5.1.1'])
        # Unable to convert hl7 container object into a dictionary directly
        # So creating a custom dictionary instead
        some_dict = create_dict(record)
        records.append(some_dict)
    
    print("Parsed",count,'records')
    # Convert to a dataframe and output in tabular format
    df=pd.DataFrame(records)
    df.to_csv('tabular_output.csv',index=False,columns=records[0].keys())
    print('Done writing to file')
    
if __name__=='__main__':
    fp = open('sample_hl7_01.hl7')
    data = fp.read()
    main(data)
    
# End of program