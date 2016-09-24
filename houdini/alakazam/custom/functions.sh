#check connections on ports
conncheck(){
  if [ ! -r root ]; then echo "Must be root!";else
    if [ ! $1 ];
      then echo "Need a port";
    else netstat -plant|grep $1|grep -oE "([0-9]{1,3}[\.]){3}[0-9]{1,3}"|sort|uniq -c|sort -nr|head -5;
    fi;
  fi;
}

#service uptime
suptime(){
  if [ ! -r root ]; then echo "Must be root!";else
  echo "Server uptime: $(uptime|awk -F',' '{print $1,$2}')";
  sqlup=$(mysqladmin version|grep Uptime|sed s/Uptime://);
  echo "MySQL uptime: $(echo $sqlup)";
  httpup=$(httpd fullstatus|grep uptime|sed 's/Server uptime://');
  echo "Apache uptime: $(echo $httpup)";fi
}

#a record only
ds(){
        if [ $# -eq 2 ]
         then
                dig +short $1 @$2
         else
                dig +short $1;
        fi
}

#name servers only
dsn() {
        if [ $# -eq 2 ]
         then
                dig +short NS $1 @$2
         else
                dig +short NS $1;
        fi
}

#converts timestamps with date
timestamp() {
  STAMP="$@"
  date -d "${STAMP}"
}
