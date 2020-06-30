#!/bin/bash

snom_products=(D120 D305 D315 D335 D345 D375 D385 D712 715 D717 725 D735 D745 D765 D785)

dest_filename="pkgs.db"
echo $dest_filename
current_dir=$(pwd)
echo "CURRENT FOLDER: $current_dir"

if [ "$#" -ne 1 ]; then
    echo "specify firmware version"
    exit
fi

dir=$(mktemp --tmpdir -d snom-fw-$1.XXXXX)
echo "TMP FOLDER: $dir"
cd $dir
touch $dest_filename

for i in "${snom_products[@]}"
do
    NAME=$i
    if [[ ${i:0:1} == "D" ]]; then
        NAME="${i:1}"
    fi
    echo "[pkg_$NAME-fw]" >> $dest_filename
    echo "description: Firmware for Snom $i" >> $dest_filename
    echo "description_fr: Firmware pour Snom $i" >> $dest_filename
    echo "version: $1" >> $dest_filename
    echo "files: $NAME-fw" >> $dest_filename
    echo "install: snom-fw" >> $dest_filename
    echo "" >> $dest_filename
done

echo "[pkg_uxm-fw]" >> $dest_filename
echo "description: Firmware for Snom Extension USB Module UXM D3/D7" >> $dest_filename
echo "description_fr: Micrologiciel pour module d'extension USB Snom UXM D3/D7" >> $dest_filename
echo "version: 2.1.1" >> $dest_filename
echo "files: uxm-fw" >> $dest_filename
echo "install: snom-fw" >> $dest_filename
echo "" >> $dest_filename

echo "[install_snom-fw]" >> $dest_filename
echo "a-b: cp \$FILE1 firmware/" >> $dest_filename
echo "" >> $dest_filename

echo "[file_uxm-fw]" >> $dest_filename
echo "url: http://downloads.snom.com/snomUXM-2.1.1.bin" >> $dest_filename
echo "size: 96560" >> $dest_filename
echo "sha1sum:9c4e07185ca6eb863858edf23147ab8576f94c4a" >> $dest_filename
echo "" >> $dest_filename

for i in "${snom_products[@]}"
do
    NAME=$i
    if [[ ${i:0:1} == "D" ]]; then
        NAME="${i:1}"
    fi

    FILE=snom$i-$1-SIP-r.bin
    URL=http://downloads.snom.com/fw/$1/bin/$FILE
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
