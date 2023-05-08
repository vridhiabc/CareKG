import re
from MedKG_neo4j import *
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkSession.builder.getOrCreate()    
sqlContext = SQLContext(sc)

def extract_wiki_id(input):
	check = re.search(r'\/(?P<entity>[A-Z\d]+)$', input)
	if check is None:
		return None
	grps=check.group('entity')
	return grps

udf_extract_wiki_id = udf(extract_wiki_id, StringType())

def conver_entity_type_to_neo4j_format(input):
	input = input.strip()
	input = re.sub(r'^[^a-z]+', '', input)
	input = re.sub(r'[^a-z]+$', '', input)
	return re.sub(r'[^a-z]+', '_', input)

udf_conver_entity_type_to_neo4j_format = udf(conver_entity_type_to_neo4j_format, StringType())

def conver_entity_name_to_neo4j_format(input):
	input = input.strip()
	return re.sub(r'\'', '\\\'', input)

udf_conver_entity_name_to_neo4j_format = udf(conver_entity_name_to_neo4j_format, StringType())


sqlContext.read.format('csv').option('header', 'true').load('datasetsideeffect.csv').registerTempTable('query')

sqlContext.sql(u"""
	SELECT DISTINCT disease AS node_id, diseaseLabel AS node_content, dis_type AS node_type
	FROM query
	UNION ALL 
	SELECT DISTINCT drug AS node_id, drugLabel AS node_content, drug_type AS node_type
	FROM query
	""").write.mode('Overwrite').json('temp')

sqlContext.read.json('temp').registerTempTable('temp')

sqlContext.sql(u"""
	SELECT node_id, 
	COLLECT_SET(node_content)[0] AS node_content,
	COLLECT_SET(node_type)[0] AS node_type
	FROM temp
	WHERE node_id IS NOT NULL
	GROUP BY node_id
	""")\
.withColumn('node_id', udf_extract_wiki_id('node_id'))\
.withColumn('node_type', udf_conver_entity_type_to_neo4j_format('node_type'))\
.withColumn('node_content', udf_conver_entity_name_to_neo4j_format('node_content'))\
.write.mode('Overwrite').json('node.json')

ingest_node_json2neo4j(
	bolt_url = 'bolt://localhost:7687',
	bolt_username = 'neo4j',
	bolt_password = 'neo4j1234',
	input_json = 'node.json',
	sqlContext = sqlContext,
	delect_neo4j = True)

sqlContext.sql(u"""
	SELECT DISTINCT disease AS subject_id,
	dis_type AS subject_type,
	drug AS object_id,
	drug_type AS object_type,
	rp AS relation
	FROM query
	WHERE disease IS NOT NULL 
	AND drug IS NOT NULL 
	AND dis_type IS NOT NULL
	AND drug_type IS NOT NULL
      AND rp IS NOT NULL
	""")\
.withColumn('subject_id', udf_extract_wiki_id('subject_id'))\
.withColumn('object_id', udf_extract_wiki_id('object_id'))\
.withColumn('subject_type', udf_conver_entity_type_to_neo4j_format('subject_type'))\
.withColumn('object_type', udf_conver_entity_type_to_neo4j_format('object_type'))\
.withColumn('relation', udf_conver_entity_type_to_neo4j_format('relation'))\
.write.mode('Overwrite').json('relation.json')

ingest_relation_json2neo4j(
	bolt_url = 'bolt://localhost:7687',
	bolt_username = 'neo4j',
	bolt_password = 'neo4j1234',
	input_json = 'relation.json',
	sqlContext = sqlContext,
	delect_neo4j = False)