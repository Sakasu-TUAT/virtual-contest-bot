# 日本語フォントファイルのダウンロード
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip

# zipファイルを展開
unzip IPAexfont00401.zip

# フォルダ作成/展開したファイルを移動
mkdir /usr/share/fonts/ipa
mv IPAexfont00401/*.ttf /usr/share/fonts/ipa/
# フォントファイルの再読み込み
fc-cache -fv

# 対象フォントが読み込まれているかチェック(明朝とかがあればOKです)
fc-list | grep IPA

# zipファイルの削除
rm -f IPAexfont00401.zip