export TEST_DB_FILENAME=db_testdata.txt

generate_data() {
  > "$TEST_DB_FILENAME"
  local num_iterations=$1

  words=("foo" "bar" "car" "apple" "banana")

  for ((i=1; i<=num_iterations; i++)); do
    random_word=${words[$RANDOM % ${#words[@]}]}
    echo "$random_word, $i" >> "$TEST_DB_FILENAME"
  done
}

clear_data() {
  > "$TEST_DB_FILENAME"
}

if [ "$1" = "add_data" ]; then
  if [ -n "$2" ]; then
    generate_data "$2"
    echo "Data Generation Complete!" 
  else
    echo "Please provide the number of iterations."
  fi
fi

if [ "$1" = "clear_data" ]; then
  clear_data
fi