#!/bin/sh

rm -rf dist
rm -rf {SnowSQL/build,SnowSQL/dist}
rm -rf {SnowSQL_Sqlite/build,SnowSQL_Sqlite/dist}
rm -rf {SnowSQL_Mysql/build,SnowSQL_Mysql/dist}

echo "Build SnowSQL..."
cd SnowSQL
python setup.py bdist_wheel
cd ..

echo "Build SnowSQL-Mysql"
cd SnowSQL_Mysql
python setup.py bdist_wheel
cd ..

echo "Build SnowSQL-Sqlite"
cd SnowSQL_Sqlite
python setup.py bdist_wheel
cd ..

mkdir dist
cp SnowSQL/dist/* dist/
cp SnowSQL_Mysql/dist/* dist/
cp SnowSQL_Sqlite/dist/* dist/
