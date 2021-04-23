import os
import pandas as pd
import statistics as st
data2 = []

def extract_feature(folder):
    stdv = []
    rrt = []
    md = []
    emosi = ['kaget','marah','santai','senang']
    dirs = os.listdir(folder)
    count = 0
    root = 'Feature_extract'
    print(len(dirs))
    for i in emosi:
        for j in range(2,int(len(dirs)/4)+2):
            df = pd.read_csv(folder+'/'+i+str(j)+'_filtered.csv')
            data1 = list(df.iloc[:,2])
            print(len(data1))
            #data2 = list(df.iloc[:,4])            
            stdv1 = st.stdev(data1)
            rrt1 = st.mean(data1)
            md1 = st.median(data1)
            stdv.append(stdv1)
            rrt.append(rrt1)
            md.append(md1)
            # stdv2 = st.sdev(data2)
            # rrt2 = st.mean(data2)
            # md2 = st.median(data2)

        namafile = i+'_extracted.csv'
        #d_t = list(zip(stdv1,rrt1,md1))
        finaldirs = os.path.join(root,namafile)
        df1 = pd.DataFrame({'STDEV' : stdv,'AVG' : rrt,'MDN' : md})
        df1.to_csv(finaldirs,mode='w+')
        print(finaldirs)
        stdv.clear()
        rrt.clear()
        md.clear()
    print('Selesai !')

extract_feature('Data_filter')
