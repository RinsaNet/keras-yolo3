# augmentation by contrust and blitness
import os
import numpy as np
import cv2

def adjust(img, alpha, beta):
    # 積和演算を行う。
    dst = alpha * img + beta
    # [0, 255] でクリップ（配列内の値を制限）し、uint8 型（８ビット整数０～２５５）にする。
    return np.clip(dst, 0, 255).astype(np.uint8)

def gamma_correction(image,gamma):  
    lookup_table = np.zeros((256, 1), dtype = 'uint8')  
    for loop in range(256):  
        # γテーブルを作成  
        lookup_table[loop][0] = 255 * pow(float(loop)/255, 1.0/gamma)  
    return  cv2.LUT(image, lookup_table)  


def _main():
    annotated_Textdata=rf'E:\DeepLearningProgramBackup\siitake_zentai_many1817mai\model_data\2007_val.txt'
    augmented_Textdata=rf'E:\DeepLearningProgramBackup\siitake_zentai_many1817mai\model_data\new_2007_val.txt'#開始時は不要
    augmented_images_directry=rf'E:\DeepLearningProgramBackup\siitake_zentai_many1817mai\augmented_JPEG_val'#開始時は不要
    os.makedirs(augmented_images_directry)
    BIAS=[-30,-15,12,30] #画像変換する際のバイアス（明るさ）の変更値

    #1度に全行を１行ずつ読み込む
    with open(annotated_Textdata) as f:
       lines = f.readlines()  
    f.close()

    count = 0
    with open(annotated_Textdata) as f:
       for line in f:
            count += 1
    f.close()

    #1行ごとに処理する
    image_no=0        #処理の進捗状況　処理行数カウンター
    for s in lines:   #各行に関して繰り返す
        image_no+=1
        abc=s.split() #SPACE区切り毎のリスト path box,class box,class...... 
        term=abc[0]   #０番目の区切りは画像のパス文字列
        if len(abc)==1: #画像はあるけどアノテーションされていない画像は無視
            continue
        try:
            #******************  オリジナルデータの読み込み、保存
            #画像の読み込み
            im_rgb=cv2.imread(term)
            #cv2.imshow('RGB',im_rgb)#表示
            #元画像を拡張ディレクトリへコピー
            original_file_name=os.path.basename(term)#オリジナル画像のファイル名
            abc[0]=augmented_images_directry+'\\'+original_file_name #拡張ディレクトリ＋オリジナル画像ファイル名
            cv2.imwrite(abc[0],im_rgb) #拡張ディレクトリへオリジナル画像を保存
            with open(augmented_Textdata,"a",encoding="utf-8") as g: #拡張後のアノテーションデータファイル(text)への書込み
                g.write(' '.join(abc))                               #リストabcをSPACE区切りでテキストファイルへ書き込む
                g.write("\n")                                        #改行コードの書込み
            g.close()

            #******************  拡張データの生成、保存
            #print('augmented image path=',abc[0])
            im_gray = cv2.cvtColor(im_rgb, cv2.COLOR_BGR2GRAY)
            base_mean=np.mean(im_gray)
           
            print("\r{0}".format(image_no),'/',count,)#'  ',term,'  　平均輝度=',int(base_mean), end='') 
            #pro_bar = ('=' * image_no) + (' ' * (count - image_no))
            #print('\r[{0}] {1}%'.format(pro_bar, image_no / count * 100.), end='')

            if base_mean<=50:
                gamma=[1.2,1.4,1.6,1.8]
            if 50<base_mean<=200:
                gamma=[0.8,1.2,1.4,1.6]
            if 200<base_mean<=255:
                gamma=[0.6,0.8,1.2,1.4]

            for g in gamma:
                im_gamma1=gamma_correction(im_rgb,g)
                new_file_name=original_file_name.replace('.jpg','gamma'+str(int(10*g))+'.jpg')  #画像pathの書き換え
                new_full_path=augmented_images_directry+'\\'+new_file_name
                abc[0]=new_full_path                                        #リスト中の画像パスの書き換え
                cv2.imwrite(new_full_path,im_gamma1)#拡張された画像の保存
                with open(augmented_Textdata,"a",encoding="utf-8") as g: #拡張後のアノテーションデータ(text)の書込み
                    g.write(' '.join(abc))                               #リスト変数abcをSPACE区切りでファイルgへ書き込む
                    g.write("\n")                                        #改行コードの書込み
                g.close()
            #cv2.destroyAllWindows()
        except FileNotFoundError:
            print('File not found')
            sys.exit()

if __name__ == '__main__':
    _main()
