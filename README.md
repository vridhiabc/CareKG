# CareKG - A Medical Knowledge Graph

* Building a Knowledge graph for biomedical Science on neo4j, from the data of Wikidata, by SPARQL querying.

<h2 >
<a> Installation </a> </h2>

installation of Neo4j
<pre>
<code>
wget http://neo4j.com/artifact.php?name=neo4j-community-3.5.12-unix.tar.gz
tar -xf 'artifact.php?name=neo4j-community-3.5.12-unix.tar.gz'
cd neo4j-community-3.5.12
bin/neo4j start
</code>
</pre>

go to url
<pre>
<code>
http://localhost:7474/

bolt://localhost:7687
user name:neo4j
password neo4j
</code>
</pre>

<h2>
<a> installation of pyspark and neo4j package </a> </h2>

<pre>
<code>
pip3 install pyspark
pip3 install neo4j
</code>
</pre>

<h2>
<a> download this package </a> </h2>
<pre>
<code>
git clone https://github.com/gaoyuanliang/covid19_knowledge_graph.git
cd covid19_knowledge_graph
</code>
</pre>

<h2 >
<a> data collection </a> </h2>

collect the entities and relationships of drug-disease from wikibase by SPARQL queries at https://query.wikidata.org/
<pre>
<code>
SELECT DISTINCT ?disease ?diseaseLabel ?drug ?drugLabel 
WHERE
{
  VALUES ?toggle { true false }
  ?disease wdt:P699 ?doid;
           wdt:P2176 ?drug.
  ?drug rdfs:label ?drugLabel.
    FILTER(LANG(?drugLabel) = "en").
  ?disease rdfs:label ?diseaseLabel.
    FILTER(LANG(?diseaseLabel) = "en").
}

</code>
</pre>

<h2>
<a>building knowledge graph at neo4j </a> </h2>

<h3 >
<a>Starting the neo4j server </a> </h3>
<pre>
<code>
neo4j-community-5.3.0\bin - neo4j console

</code>
</pre>

<h3>
<a>ingest the data into neo4j </a> </h3>
<pre>
<code>
python MedKG_knowledge_graph.py

</code>
</pre>

<h2>
<a>Website for tabular visualization of entities </a> </h2>
<pre>
<code>
python MedKG_display.py

</code>
</pre>

