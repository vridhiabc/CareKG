#To view all nodes
MATCH (n) RETURN n LIMIT 20 

#To view all nodes with their relationships
MATCH (n)-[r]-(m) RETURN n,r,m

#To view specific node with its relationships
MATCH (n {content: 'schizophrenia'})-[r]-(m) RETURN n,r,m

drug :
MATCH (n {content: 'buprenorphine'})-[r]-(m) RETURN n,r,m

disease :
MATCH (n {content: "cancer"})-[r]-(m) RETURN n,r,m

side_effect :
MATCH (n {content: "headache"})-[r]-(m) RETURN n,r,m

not available : Dengue
