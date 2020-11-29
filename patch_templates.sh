#!/bin/sh

mv templates/rus_bold.svg templates/ru_bold.svg
mv templates/rus_light.svg templates/ru_light.svg

sed -i'' -e "s/&#x412;&#x43b;&#x430;&#x434; &#x413;&#x43e;&#x441;&#x442;&#x438;&#x449;&#x435;&#x432;/PLACE_NAME_HERE/" templates/ru_bold.svg
sed -i'' -e 'image id="image2"/image id="image2" transform="translate(0 -10)"/' templates/ru_bold.svg

sed -i'' -e "s/Vlad Gostishchev/PLACE_NAME_HERE/" templates/en_bold.svg
sed -i'' -e 'image id="image2"/image id="image2" transform="translate(0 -10)"/' templates/en_bold.svg
