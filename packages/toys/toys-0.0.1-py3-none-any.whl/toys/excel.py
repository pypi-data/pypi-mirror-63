#depend
#import pandas as pd
#import os


# # var
# path_sourec='./source/'

# #rename and filter
# file_columns=['create_time','channel','server_id','role_id','ip']


def con_sheets(self,path_source,file_columns):
    self.example={'path_source':'path_dir','file_columns':'list'}

    import pandas as pd
    import os

    #read excel
    files=os.listdir(path_source)
    file_name=files[0]

    dic_data=pd.read_excel(path_source+file_name,sheet_name=None,header=None,dtype='object')

    #combine sheet 
    list_sheet=[]

    for sheet_name in dic_data:
        sheet=dic_data[sheet_name]
        list_sheet.append(sheet)

    df_data=pd.concat(list_sheet,axis=0,sort=False,ignore_index=True)

    #rename and filter
    df_data=df_data.rename(columns=dict(zip(range(len(file_columns)),file_columns)))

    df_data=df_data.dropna(how='all')
    df_data=df_data.loc[df_data[file_columns[0]]!=file_columns[0],:]
    
    return df_data