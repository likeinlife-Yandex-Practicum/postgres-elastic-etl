indexes=("movie" "person" "genre")
types=("analyzer" "mapping" "data")
es_host="127.0.0.1:9200"
directory="dumps"

len=3
mkdir ${directory}

for index in ${indexes[@]}
do
    for ((i=0; i<$len; i++))
    do
        es_index=http://${es_host}/${index}
        type=${types[i]}
        file_name=${index}.$((i+1)).${type}.json
        path_to_file=${directory}/${file_name}
        elasticdump --input=${es_index} --output=${path_to_file} --type=${type}
    done
done