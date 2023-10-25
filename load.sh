echo "puerto:" $1 &&
ampy -p $1 ls &&
echo "sps" &&
ampy -p $1 put sps30/sps30.py &&
echo "main" &&
ampy -p $1 put main.py &&
echo "bme" &&
ampy -p $1 put bme280.py &&
echo "lib" &&
ampy -p $1 put datalog_lib.py &&
echo "info" &&
ampy -p $1 put info.py &&
echo "pmsa" &&
ampy -p $1 put pmsa003.py
