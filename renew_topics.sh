topic=live_score

kafka/kafka_2.12-2.2.1/bin/kafka-topics.sh --zookeeper z-2.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-3.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-1.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181 --delete --topic $topic

kafka/kafka_2.12-2.2.1/bin//kafka-topics.sh --create --zookeeper z-2.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-3.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-1.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181 --replication-factor 1 --partitions 1 --topic $topic


topic=word_count

kafka/kafka_2.12-2.2.1/bin/kafka-topics.sh --zookeeper z-2.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-3.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-1.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181 --delete --topic $topic

kafka/kafka_2.12-2.2.1/bin//kafka-topics.sh --create --zookeeper z-2.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-3.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181,z-1.mskcluster.nn1not.c8.kafka.us-west-2.amazonaws.com:2181 --replication-factor 1 --partitions 1 --topic $topic
