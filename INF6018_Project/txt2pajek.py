import sys
import pandas as pd
"""
Creates Pajek file from Global Bilateral Migration dataset csv.
It can be easily modified to transform other datasets. 

The from and to node column names and a relationship column name have to be passed as parameters.
The nodes are identified by their indexes and the relations are coded through indexes. 

The csv file columns in a general form extracted frm the general csv file:

    From To Weight
    Jim John 1
    John George 3
    George Berta 4
    Jim George 3

The resulting pajek net file:

    *Vertices 4
    1 "Jim"
    2 "John"
    3 "George"
    4 "Berta"
    *Edges undirected / or *Arcs directed
    1 2 1
    2 3 3
    3 4 4
    1 3 3 

Program command line parameters:

    input_file: Name of the CSV File
    from_column: Name of From Column
    to_column: Name of To Column
    weight_column: Name of Weight Column
    gender_column: Name of the Gender Column
    gender_value: Gender value [ Female | Male | Total]
    output_file: Name of the output file (no extension) 
    n_migrated: Threshold of how many migrated (> 0)
    n_direction: Direction of comparison ["less than" | "more than"] with n_migrated
     
Returns:
    Pajek net file to output_file name

    
Example Call:
    python3 txt2pajek.py 53285608-4ef3-4458-9696-0b2c33ce95dd_Data.csv \
                        "Country Origin Name" \
                        "Country Dest Name"  \
                        "1960 [1960]"  \
                        "Migration by Gender Name" \ 
                        "Total"  \
                        "migration_total.net" \ 
                        1000  \
                        "more than" \
                        
Parameters to copy:
WDI_DS_original/Global_Bilateral_Migration/53285608-4ef3-4458-9696-0b2c33ce95dd_Data.csv "Country Origin Name" "Country Dest Name" "1960 [1960]" "Migration by Gender Name" "Total" "migration_total" 100000 "more than"

Increase or decrease threshold to obtain a small network. 
"""

if __name__ == "__main__":
    
    input_file=sys.argv[1]
    from_column=sys.argv[2]
    to_column=sys.argv[3]
    weight_column=sys.argv[4]
    gender_column=sys.argv[5]
    gender_value=sys.argv[6]
    output_file=sys.argv[7]
    n_migrated=sys.argv[8]
    n_direction=sys.argv[9]
    

    # read input file 
    df=pd.read_csv(input_file)
    #print(df.columns)
    # filter by gender
    df = df[df[gender_column] == gender_value ].copy()


    df_columns=df[[from_column, to_column, weight_column]].copy()
    df_columns.dropna(inplace=True)

    
    # remove rows with NaN values
    df_notnull_mask = df_columns.notnull().all(axis=1)
    df_columns=df_columns[df_notnull_mask].copy()

    # change the column to int
    #weight=df_columns[weight_column].astype('integer')
    #print(weight)

    # remove rows with non numeric weights 
    def checknum(x):
        if x.isnumeric():
            return(int(x))
        else:
            return(0)
        
    df_columns['weight_isnumeric']=[checknum(num) for num in df_columns[weight_column] ]
    df_columns = df_columns[(df_columns['weight_isnumeric'] != 0) ].copy()
    
    # Here filter either lower or higher
    if n_direction=="less than":
        df_columns = df_columns[ df_columns['weight_isnumeric'] <= int(n_migrated) ].copy()
    elif n_direction=="more than":
        df_columns = df_columns[ df_columns['weight_isnumeric'] >= int(n_migrated) ].copy()
    else:
        pass

    #print(df_columns.info())
    
    nodes=list(set(df_columns[from_column]).union(set( df_columns[to_column] ) ) )
 
    nodes_dict={}
    for index, elem in enumerate(nodes):
        nodes_dict[elem]=index+1
    
    n_nodes=len(nodes)
    
    # Create output
    fout=open(output_file+".net","w")
    
    outstr=f"*Vertices {n_nodes}"+"\n"
    print(outstr)
    fout.write(outstr)
    
    for node_label, node_id in nodes_dict.items():
        outstr=f"{node_id} \"{node_label}\""+"\n"
        print(outstr)
        fout.write(outstr) 
    
    n_arcs=len(df_columns)
    outstr=f"*Arcs {n_arcs}"+"\n"
    print(outstr)
    fout.write(outstr)

    # insert indexes instead of countries in the arcs part
    for i in df_columns.index :
        origin_key = df_columns.at[i, from_column]
        destination_key = df_columns.at[i, to_column]
        weight = df_columns.at[i, weight_column]

        origin=nodes_dict[origin_key]
        dest=nodes_dict[destination_key]
        outstr=f"{origin} {dest} {weight}"+"\n"
        print(outstr)
        fout.write(outstr)
    fout.close()

    # write the vertices to csv
    node_label=nodes_dict.keys()
    node_id=nodes_dict.values()
    df_vertices=pd.DataFrame({'node_id':node_id, 'node_label':node_label})
    print(df_vertices)
    df_vertices.to_csv(output_file+"_intermediate.csv", sep=" ")

    # write data frame to csv to be able to analyze with cytoscape
    df_columns.to_csv(output_file+"_cysimport.csv", sep="\t")

