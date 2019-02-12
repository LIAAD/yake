#!/usr/bin/env bash
YAKE_PORT="5000"

function wait_for_server_to_boot_on_port()
{
    local ip=$1
    local port=$2
    local text_to_find=$3

    if [[ $ip == "" ]]; then
      ip="127.0.0.1"
    fi
    local attempts=0
    local max_attempts=60

    echo "Waiting for server on $ip:$port to boot up..."
    response=$(curl -s $ip:$port)

	  until $(curl --output /dev/null --silent --head --fail http://$ip:$port) || [[ $response == *$text_to_find* ]] || (( $attempts > $max_attempts )) ; do
        ((attempts=attempts+1))
        echo "Waiting... ${attempts}/${max_attempts}"
        sleep 1;
        response=$(curl -s $ip:$port)
	  done

    if (( $attempts == $max_attempts ));
    then
        echo "Server on $ip:$port failed to start after $max_attempts"
    elif (( $attempts < $max_attempts ));
    then
        echo "Server on $ip:$port started successfully at attempt (${attempts}/${max_attempts})"
    fi
}

# get directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# get constants
source "$DIR/constants.sh"
docker run -d -p $YAKE_PORT:$YAKE_PORT "$YAKE_SERVER_IMAGE:$TAG"

wait_for_server_to_boot_on_port "127.0.0.1" "$YAKE_PORT" "<title>404 Not Found</title>"

curl 'http://127.0.0.1:5000/yake/' \
-XPOST \
-H 'Accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data "text=Coffee%20is%20a%20brewed%20drink%20prepared%20from%20roasted%20coffee%20beans%2C%20the%20seeds%20of%20berries%20from%20certain%20Coffea%20species.%20The%20genus%20Coffea%20is%20native%20to%20tropical%20Africa%20(specifically%20having%20its%20origin%20in%20Ethiopia%20and%20Sudan)%20and%20Madagascar%2C%20the%20Comoros%2C%20Mauritius%2C%20and%20R%C3%A9union%20in%20the%20Indian%20Ocean.%5B2%5D%20Coffee%20plants%20are%20now%20cultivated%20in%20over%2070%20countries%2C%20primarily%20in%20the%20equatorial%20regions%20of%20the%20Americas%2C%20Southeast%20Asia%2C%20Indian%20subcontinent%2C%20and%20Africa.%20The%20two%20most%20commonly%20grown%20are%20C.%20arabica%20and%20C.%20robusta.%20Once%20ripe%2C%20coffee%20berries%20are%20picked%2C%20processed%2C%20and%20dried.%20Dried%20coffee%20seeds%20(referred%20to%20as%20%22beans%22)%20are%20roasted%20to%20varying%20degrees%2C%20depending%20on%20the%20desired%20flavor.%20Roasted%20beans%20are%20ground%20and%20then%20brewed%20with%20near-boiling%20water%20to%20produce%20the%20beverage%20known%20as%20coffee.&language=en&max_ngram_size=4&number_of_keywords=10"

# test
docker run "$YAKE_IMAGE:$TAG" -ti "Caffeine is a central nervous system (CNS) stimulant of the methylxanthine class.[10] It is the world's most widely consumed psychoactive drug. Unlike many other psychoactive substances, it is legal and unregulated in nearly all parts of the world. There are several known mechanisms of action to explain the effects of caffeine. The most prominent is that it reversibly blocks the action of adenosine on its receptor and consequently prevents the onset of drowsiness induced by adenosine. Caffeine also stimulates certain portions of the autonomic nervous system."
