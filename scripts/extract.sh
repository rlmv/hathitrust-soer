 #!/bin/bash


#./extract SOURCEDIR TARGETDIR

cd $1;
ls | grep .txt | while read fname; do 
    cp $fname ../$2/$1.$fname; 
done

