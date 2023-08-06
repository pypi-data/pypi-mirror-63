#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit   /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
#docker exec -u befi8957 -it webis-datascience-image-befi8957 bash -l -c 'cd; exec /opt/spark/bin/spark-submit --deploy-mode cluster --py-files /home/yamenajjour/git/topic_ontologies/deploy/topic-ontologies-dep.zip --executor-memory 2G --driver-memory 4G /home/yamenajjour/git/topic_ontologies/topic_modeling/model_corpus_args_me_cluster.py'
import sys
sys.path.insert(0,"/home/yamenajjour/git/topic-ontologies/")

from pyspark.sql import SparkSession
import argument_esa_model.esa_top_n_terms
import pickle
import codecs
from conf.configuration import *
set_cluster_mode()


spark = SparkSession.builder.appName('topic-ontologies').config('master','yarn').getOrCreate()
args_me = spark.read.format('csv').option('header','true').option('delimiter',',')
spark_context= spark.sparkContext

def dict_to_list(dictionary):
    vector  = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])
    pickled = codecs.encode(pickle.dumps(vector), "base64").decode()
    return pickled

URI = spark_context._gateway.jvm.java.net.URI
Path = spark_context._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem = spark_context._gateway.jvm.org.apache.hadoop.fs.FileSystem
FsPermission = spark_context._gateway.jvm.org.apache.hadoop.fs.permission.FsPermission
fs = FileSystem.get(URI("hdfs://betaweb020.medien.uni-weimar.de:8020"), spark_context._jsc.hadoopConfiguration())
fs.listStatus(Path('/user/befi8957'))

def project_documents(topic_ontology):
    def project_document(argument):
        import nltk
        nltk.data.path.append('/mnt/ceph/storage/data-in-progress/topic-ontologies/nltk/')
        set_cluster_mode()
        path_corpus = get_path_source("ontology-"+topic_ontology)
        path_word2vec_model = get_path_topic_model('word2vec','word2vec')
        path_word2vec_vocab = get_path_vocab('word2vec')
        vector = argument_esa_model.esa_top_n_terms.model_topic(path_corpus,path_word2vec_model,path_word2vec_vocab,argument,1000)
        return dict_to_list(vector)

    path_documents = get_path_preprocessed_documents('sample')
    path_document_vectors= get_path_document_vectors('sample',topic_ontology,'word2vec-esa-1000').replace(".csv","")
    documents_df  = spark.read.format("csv").option("header", "true").option("delimiter", "|", ).option('quote', '"').load(path_documents)
    documents = documents_df.select("document").rdd.map(lambda r: r[0]).repartition(100)
    ids = (documents_df.select("document-id").rdd.map(lambda r: r[0])).repartition(100)
    vectors = documents.map(lambda document:project_document(document))
    ids_with_vectors=vectors.zip(ids)
    FileSystem.mkdirs(fs,Path(path_document_vectors),FsPermission(77777))
    ids_with_vectors.saveAsTextFile(path_document_vectors)
project_documents('wikipedia')
project_documents('debatepedia')
project_documents('strategic-intelligence')