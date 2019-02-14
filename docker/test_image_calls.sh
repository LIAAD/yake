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

curl -X POST "http://127.0.0.1:5000/yake/" -H "accept: application/json" -H "Content-Type: application/json" \
-d @- <<'EOF'
{
  "language": "en",
  "max_ngram_size": 2,
  "number_of_keywords": 10,
  "text": "
      Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague , but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner
    "
}
EOF

# test
docker run liaad/yake:latest -ti "Caffeine is a central nervous system (CNS) stimulant of the methylxanthine class.[10] It is the world's most widely consumed psychoactive drug. Unlike many other psychoactive substances, it is legal and unregulated in nearly all parts of the world. There are several known mechanisms of action to explain the effects of caffeine. The most prominent is that it reversibly blocks the action of adenosine on its receptor and consequently prevents the onset of drowsiness induced by adenosine. Caffeine also stimulates certain portions of the autonomic nervous system."
