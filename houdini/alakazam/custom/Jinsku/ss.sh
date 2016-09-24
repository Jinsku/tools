#!/bin/bash
##########################
## Jinsku - Brett/Trent	##
##########################
## (Work in Progress)
## Dependencies
# -Clamscan
# -Maldetect
# -cPanel (as of now)
## Functions
# -Single user
# -All users

user=${1};
opt=${2};

function scan {
	mkdir /home/${user}/.security &> /dev/null;
	slt=$(date +%s);
	echo -e "\e[1m[\e[32m+\e[0m\e[1m]\e[0m Scanning ${user}...";
	echo -e "======Clamscan======\n" >> /home/${user}/.security/sslog.${slt};
	clamscan -i -r /home/${user} >> /home/${user}/.security/sslog.${slt};
	echo -e "\n======Maldet======\n\n" >> /home/${user}/.security/sslog.${slt};
	id=$(maldet -a /home/${user}/ | sed -n "s|^.*maldet --report ||p");
	cat /usr/local/maldetect/sess/session.${id} >> /home/${user}/.security/sslog.${slt};
	echo -e "\e[1m[\e[32m+\e[0m\e[1m]\e[0m Scan complete"
	echo -e "Log available at: /home/${user}/.security/sslog.${slt}";
}

echo -e "security.sh\t\tadmin@krux.us\n\n";
if [ $# -eq 0 ]
	then
		echo -e "[\e[1;31m!\e[0m\e[1m]\e[0m No user supplied";
	else
		case "${user}" in
			-a)
				echo -e "[*] Scanning all users...\nThis may take some time.\n";
				users=(); 
				for i in $(find /var/cpanel/users/ -type f | sed -s "s|/var/cpanel/users/||"); do 
					users+=($i); done;
				for user in ${users[@]}; do
					scan $user; done;
			;;
			*)
				scan
			;;
		esac
fi
