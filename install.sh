#!/bin/sh

echo "Choose your language. Insert just a number. \n1.English 2.Korean"
read number

if [ $number -eq 1 ]
then
    language="en"
elif [ $number -eq 2 ]
then
    language="ko"
else
    language="en"
fi

touch walkr/settings.ini

cat << EOF > walkr/settings.ini
[localization]
language: $language
EOF