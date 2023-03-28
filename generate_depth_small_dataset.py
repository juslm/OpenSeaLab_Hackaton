import zipfile


tiles=['D4','F3','F5','E4','E5','E3','F4','D5','D3','C2','C3','C4','C5','C6','D6','E6','F6','G6','G5','G3','G2','D2','E2','F2']
file2=open('data/depth_small.txt', 'w')
for i in tiles:
    with zipfile.ZipFile('data/depth_tiles_diluted/'+i+'_2020.txt.zip','r') as zip_ref:
        zip_ref.extractall("data/depth_tiles_diluted/")
    file1 = open('data/depth_tiles_diluted/'+i+'_2020.txt', 'r')
    Lines = file1.readlines()
    counter=0
    for line in Lines:
        counter+=1
        if counter%10==0:
            file2.write(line[:-2]+'\n')
    file1.close()
file2.close()