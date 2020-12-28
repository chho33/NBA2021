from pyspark import SparkContext
import re
import boto3
import json
import sys
from datetime import datetime

stop_words = ['i',
 'me',
 'my',
 'myself',
 'we',
 'our',
 'ours',
 'ourselves',
 'you',
 'your',
 'yours',
 'yourself',
 'yourselves',
 'he',
 'him',
 'his',
 'himself',
 'she',
 'her',
 'hers',
 'herself',
 'it',
 'its',
 'itself',
 'they',
 'them',
 'their',
 'theirs',
 'themselves',
 'what',
 'which',
 'who',
 'whom',
 'this',
 'that',
 'these',
 'those',
 'am',
 'is',
 'are',
 'was',
 'were',
 'be',
 'been',
 'being',
 'have',
 'has',
 'had',
 'having',
 'do',
 'does',
 'did',
 'doing',
 'a',
 'an',
 'the',
 'and',
 'but',
 'if',
 'or',
 'because',
 'as',
 'until',
 'while',
 'of',
 'at',
 'by',
 'for',
 'with',
 'about',
 'against',
 'between',
 'into',
 'through',
 'during',
 'before',
 'after',
 'above',
 'below',
 'to',
 'from',
 'up',
 'down',
 'in',
 'out',
 'on',
 'off',
 'over',
 'under',
 'again',
 'further',
 'then',
 'once',
 'here',
 'there',
 'when',
 'where',
 'why',
 'how',
 'all',
 'any',
 'both',
 'each',
 'few',
 'more',
 'most',
 'other',
 'some',
 'such',
 'no',
 'nor',
 'not',
 'only',
 'own',
 'same',
 'so',
 'than',
 'too',
 'very',
 's',
 't',
 'can',
 'will',
 'just',
 'don',
 'should',
 'now']



if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.exit(-1)
    
    sc = SparkContext(appName="NBAWordCount")
    textfile = sc.textFile(sys.argv[1])
    occurences = textfile.flatMap(lambda line: line.lower()\
                                               .replace(",", " ")\
                                               .replace(".", " ")\
                                               .split(" "))\
                          .map(lambda word : (word, 1))\
                          .reduceByKey(lambda a,b: a+b)\
                          .map(lambda a: (a[1], a[0]))\
                          .filter(lambda x: len(x[1])>2)\
                          .filter(lambda x: not bool(re.match("^\[", x[1])))\
                          .filter(lambda x: x[1] not in stop_words)\
                          .sortByKey(False)
    
    #format_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    #occurences.saveAsTextFile("{0}/{1}".format(sys.argv[2], format_time))

    result = occurences.collect()[:30]
    result = [{"x": d[1], "value": d[0]} for d in result]
    print(result)
    result = json.dumps(result)
    client = boto3.client('s3')
    client.put_object(Body=result.encode('utf-8'), 
                      Bucket='nba.website', 
                      Key='assets/NBAWordCount.json')

    sc.stop()
