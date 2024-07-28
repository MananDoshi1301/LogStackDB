export TEST_DB_FILENAME=db_testdata.txt

generate_data() {
  # > "$TEST_DB_FILENAME"

  words=("foo" "bar" "car" "apple" "banana")

  for i in {1..20}; do
    random_word=${words[$RANDOM % ${#words[@]}]}
    echo "$random_word, $i" >> "$TEST_DB_FILENAME"
  done
}

clear_data() {
  > "$TEST_DB_FILENAME"
}

if [ "$1" = "add_data" ]; then
  generate_data
fi

if [ "$1" = "clear_data" ]; then
  clear_data
fi