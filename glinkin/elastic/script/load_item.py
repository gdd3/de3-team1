from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import argparse
import json


def read_json(input_file, index_name="item", doc_type_name="default"):
    for line in open(input_file):
        json_line = json.loads(line)

        yield {
            "_index": index_name,
            "_type": doc_type_name,
            "_id": json_line["itemid"],
            "_source": {
                "name": json_line["attr1"],
                "annotation": json_line.get("attr0"),
            },
        }


def load(es, input_file, chunk_size):
    return bulk(es, read_json(input_file), chunk_size=chunk_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file_path")
    parser.add_argument("chunk_size", nargs="?", default=1000)
    args = parser.parse_args()

    es = Elasticsearch(hosts=["localhost:9200"], timeout=5000)

    count, _ = load(es, args.json_file_path, args.chunk_size)
    print(f"Load {count} items")
