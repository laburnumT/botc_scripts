#!/bin/bash

set -euo pipefail

to_sort="$(jq <"${1}")"
full_sorted="$(
        curl -s "https://script.bloodontheclocktower.com/data/roles.json" \
                | jq '[.[].id]'
)"

sorted_chars="$(
        jq '.full - (.full - .to_sort)' <<EOF
{
        "full": ${full_sorted},
        "to_sort": $(jq 'del(.[0])' <<<"${to_sort}")
}
EOF
)"

echo "{ \"old\": [$(jq '.[0]' <<<"${to_sort}")], \"new\": ${sorted_chars}}" \
        | jq '.old += .new | .old' >"${1}"
