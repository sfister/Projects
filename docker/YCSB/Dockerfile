from debian:sid
# http://blog.tryolabs.com/2012/06/25/connecting-sql-server-database-python-under-ubuntu/

run apt-get update 
run apt-get install -y \
   wget \
   curl 
run apt-get update 
run apt-get install -y \
   git
run apt-get install -y \
   default-jdk

run git clone https://github.com/brianfrankcooper/YCSB.git
run apt-get -y install maven
run cd /YCSB && mvn clean package

