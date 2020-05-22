#
import os
import numpy as np
import cv2

annotated_Textdata=rf'E:\vott_output\model_data\2007_val.txt'

#1度に全行を１行ずつ読み込む
with open(annotated_Textdata) as f:
    lines = f.readlines()  
f.close()

#1行ごとに処理する
for s in lines:   #各行に関して繰り返す
    print('')
    abc=s.split() #SPACE区切り毎のリスト path box,class box,class...... 
    term=abc[0]   #０番目の区切りは画像のパス文字列
    print(term)
    if len(abc)==1: #画像はあるけどアノテーションされていない行はlistの要素数が１個なので無視
            continue
    for c in range(1,len(abc)):#要素１以降の区切りは、座標+classの繰り返し.
        WIDTH=320
        anno=abc[c].split(',')
        #for ad in range(5):
        print('befor Xmin ',anno[0],'  Ymin ',anno[1],'  Xmax ',anno[2],'  Ymax ',anno[3],'  class ',anno[4])
        Xmin=anno[0]
        Ymin=anno[1]
        Xmax=anno[2]
        Ymax=anno[3]
        class_number=anno[4]

        #print('new box coordinate')
        anno[0]=str(WIDTH-int(Xmax))  #画像反転後のボックスの座標変換　左右反転なのでXmin,Xmaxのみ計算
        anno[2]=str(WIDTH-int(Xmin))
        print('after Xmin ',anno[0],'  Ymin ',anno[1],'  Xmax ',anno[2],'  Ymax ',anno[3],'  class ',anno[4])
        abc[c]=','.join(anno)
        print('abc[c]=',abc[c])#座標データをカンマで連結
        
    new_annotation_data=' '.join(abc) #annotationデータをspaceで連結
    print('new_annotation_data=',new_annotation_data)#
    print('')
