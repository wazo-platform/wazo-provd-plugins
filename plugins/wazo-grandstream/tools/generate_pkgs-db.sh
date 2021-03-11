#!/bin/bash

constructor="Grandstream"
products=(GXW4216 GXW4224 GXW4232 GXW4248)

dest_filename="pkgs.db"
echo $dest_filename
current_dir=$(pwd)
echo "CURRENT FOLDER: $current_dir"

if [ "$#" -ne 1 ]; then
    echo "specify firmware version"
    exit
fi

dir=$(mktemp --tmpdir -d gs-gxw42xx-fw-$1.XXXXX)
echo "TMP FOLDER: $dir"
cd $dir
touch $dest_filename

for i in "${products[@]}" 
do
 	NAME=$i
	echo "[pkg_$NAME-fw]" >> $dest_filename
	echo "description: Firmware for $constructor $i" >> $dest_filename
	echo "description_fr: Firmware pour $constructor $i" >> $dest_filename
	echo "version: $1" >> $dest_filename
	echo "files: $NAME-fw" >> $dest_filename
	echo "install: $constructor-fw" >> $dest_filename
	echo "" >> $dest_filename
done
echo "[install_$constructor-fw]" >> $dest_filename
echo "a-b: cp \$FILE1 firmware/" >> $dest_filename
echo "" >> $dest_filename

for i in "${products[@]}" 
do
	NAME=$i
	# FILE=snom$i-$1-SIP-r.bin
        FILE=Release_${i}_${1}.zip
        #URL=http://downloads.snom.com/fw/$1/bin/$FILE
        URL=http://firmware.grandstream.com/$FILE
	wget $URL
	SIZE=$(stat -c "%s" "$FILE")
	SHA1SUM=$(sha1sum "$FILE" | cut -f1 -d' ')

	echo "[file_$NAME-fw]" >> $dest_filename
	echo "url: $URL" >> $dest_filename
	echo "size: $SIZE" >> $dest_filename
	echo "sha1sum: $SHA1SUM" >> $dest_filename
	echo "" >> $dest_filename
done

cp $dest_filename $current_dir

