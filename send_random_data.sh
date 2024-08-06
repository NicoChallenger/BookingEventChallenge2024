#!/bin/bash

# Function to generate a random date
generate_random_date() {
  start_date="2024-01-01"
  end_date="2024-12-31"

  # Convert start and end dates to seconds since epoch
  start_sec=$(date -j -f "%Y-%m-%d" "$start_date" "+%s")
  end_sec=$(date -j -f "%Y-%m-%d" "$end_date" "+%s")

  # Generate a random date in seconds since epoch using awk
  random_sec=$(awk -v min=$start_sec -v max=$end_sec 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')

  # Convert random date in seconds since epoch to YYYY-MM-DD format
  random_date=$(date -j -f "%s" "$random_sec" "+%Y-%m-%d")

  echo "$random_date"
}
# URL to send the POST request to
url="http://0.0.0.0:8000/events"

while true; do
  # Current timestamp in the required format
  current_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3Z")

  # Generate a random date
  random_date=$(generate_random_date)

  # Generate a random room_id as UUID
  room_id=$(uuidgen)

  # JSON payload
  json_data=$(cat <<EOF
{
  "hotel_id": 0,
  "timestamp": "$current_timestamp",
  "rpg_status": 1,
  "room_id": "$room_id",
  "night_of_stay": "$random_date"
}
EOF
  )
  echo "Sending data ..."
  # Send the POST request with curl
  curl -X POST -H "Content-Type: application/json" -d "$json_data" "$url"
  # Wait for 5 seconds before the next iteration
  echo ""
  sleep 5
done
