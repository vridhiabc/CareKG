# CareKG - A Medical Knowledge Graph

* Building a Knowledge Graph for Biomedical Science on Neo4j, from the data acquired through SPARQL using Wikidata Query Service.

<h2 >
<a> Starting Neo4j </a> </h2>

<pre>
<code>
Download Neo4j using any Browser
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

<h2 >
<a> data collection </a> </h2>

Collect the Entities and Relationships between Drugs and Diseases from Wikidata Medicine by SPARQL queries at https://query.wikidata.org/
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
<a>Visualizing the Knowledge Graph in the Neo4j Platform </a> </h2>

<h3>
<a>Start the Neo4j Server</a> </h3>
<pre>
<code>
In command prompt write the following:
cd neo4j-community-3.5.12
neo4j console
</code>
</pre>


<h3>
<a>Ingest the data into Neo4j </a> </h3>
<pre>
<code>
python MedKG_knowledge_graph.py

</code>
</pre>

<h2>
<a>Frontend for Tabular Visualization of Entities </a> </h2>
<pre>
<code>
python MedKG_display.py

</code>
</pre>

