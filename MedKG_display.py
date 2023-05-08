from flask import Flask, json,request,render_template,url_for,redirect


app= Flask(__name__ )

@app.route("/")
def home():
    return("hello")

@app.route('/index',methods=["GET","POST"])
def search():
    if request.method=="POST":
        query=request.form["query"].lower()
        print(query)
        if query=='':
            return render_template("empty.html")
            
        node = [json.loads(line) for line in open('node.json\part-00000-c1c5f4a1-74a2-4b7d-87f0-848f925a2372-c000.json', 'r', encoding='utf-8')]
        res=[]
        
        for i in node:
            if i['node_content']== query:
                qid=i['node_id']
                qtype=i['node_type']
                i['node_id']='http://www.wikidata.org/entity/'+i['node_id']
                res.append(i)
                print("Searched Enity:", i)
                print("")
        if not res:
            return render_template("not.html",search = query)

        relation = [json.loads(line) for line in open('relation.json\part-00000-09e53901-13ba-4f99-ad23-40d371515c12-c000.json', 'r', encoding='utf-8')]
        qlist=[]
        for j in relation:
            if j['subject_id']== qid :
                qlist.append(j['object_id'])
            elif j['object_id']== qid:
                qlist.append(j['subject_id'])
        reslist=[]
        for k in qlist:
            for l in node:
                if l['node_id']== k:
                    l['node_id']='http://www.wikidata.org/entity/'+l['node_id']
                    reslist.append(l)
        
        dislist=[]
        sidlist=[]
            
        if qtype == "drug":
            for r in reslist:
                if r['node_type'] =="disease":
                    dislist.append(r)
                elif r['node_type'] =="side_effect":
                    sidlist.append(r)
            sidlist= [dict(t) for t in {tuple(d.items()) for d in sidlist}]
            print("Diseases which can be cured:")
            print(dislist)
            print("Side effects of Drug:")
            print(sidlist)
            return render_template("index.html", data1=res, data2=dislist, data3=sidlist)
        
        elif qtype == "disease" or qtype == "side_effect":
            print("Related Drugs:")    
            print(reslist)
            return render_template("index.html", data1=res, data2=reslist)
    
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug="True" , port=9989)
