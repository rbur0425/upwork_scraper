#!/opt/homebrew/bin/bash

# List of queries
queries=("laravel" "php" "clickfunnels" "funnel builder" "product manager" "program manager" "software project manager")

# List of arguments
args=("--top-rated-plus" "--top-rated" "--rising-talent")

# Loop through each query
for query in "${queries[@]}"; do
    # Loop through each argument
    for arg in "${args[@]}"; do
        python main.py -q "$query" -num_pages 3 $arg
    done
done
