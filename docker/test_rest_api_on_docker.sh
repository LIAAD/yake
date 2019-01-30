#!/usr/bin/env bash
YAKE_PORT="5000"

function wait_for_server_to_boot_on_port()
{
    local ip=$1
    local port=$2

    if [[ $ip == "" ]]; then
      ip="127.0.0.1"
    fi
    local attempts=0
    local max_attempts=60

    echo "Waiting for server on $ip:$port to boot up..."

    response=$(curl -s $ip:$port)
    echo $response

	until $(curl --output /dev/null --silent --head --fail http://$ip:$port) || [[ $attempts > $max_attempts ]]; do
        attempts=$((attempts+1))
        echo "waiting... (${attempts}/${max_attempts})"
        sleep 1;
	done

    if (( $attempts == $max_attempts ));
    then
        echo "Server on $ip:$port failed to start after $max_attempts"
    elif (( $attempts < $max_attempts ));
    then
        echo "Server on $ip:$port started successfully at attempt (${attempts}/${max_attempts})"
    fi
}

wait_for_server_to_boot_on_port "127.0.0.1" "$YAKE_PORT"

curl "http://127.0.0.1:5000/yake/v2/extract_keywords?max_ngram_size=3&number_of_keywords=30" \
  --header "Content-Type: \"application/x-www-form-urlencoded\"" \
  --header "Accept: \"application/json\"" \
  --request "POST" \
  --data "{\"content\":\"Caffeine is a central nervous system (CNS) stimulant of the methylxanthine class.[10] It is the world\'s most widely consumed psychoactive drug. Unlike many other psychoactive substances, it is legal and unregulated in nearly all parts of the world. There are several known mechanisms of action to explain the effects of caffeine. The most prominent is that it reversibly blocks the action of adenosine on its receptor and consequently prevents the onset of drowsiness induced by adenosine. Caffeine also stimulates certain portions of the autonomic nervous system.\"}"
