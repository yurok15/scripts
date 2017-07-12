#!/bin/bash

 if [ -n "$1" ]; then
  echo "Converging server[s] $*"
   servers=( "$@" )
    echo "${#servers[@]} total"
    else
     echo 'We need at least 1 server to converge! give the servers as arguments. No mask supported yet, sorry'
      exit 1
      fi

       #if $password is set, use it. Otherwise read it now.
       if [ -z "$password" ]; then
        read -sp "input password" password
         echo
         fi

          for server in $*; do
          date
          echo -n "converging server ${server} - "
          export i=0
          for srv in ${servers[@]};do
           i=$((i+1))
            if [ "$srv" == "$server" ];then
              echo -n "${i}/"
               fi
               done
               echo $i

                echo 'spawn knife zero converge name:'${server}'
                set prompt "Enter your password:"
                interact -o -nobuffer -re $prompt return
                send "'${password}'\n"
                interact' > run.xp
                ( sleep 1; rm run.xp ) &
                /usr/bin/expect run.xp 2>&1| grep -vF -- "${password::4}"
                done
