from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from Run import user_portal
import pandas as pd
from bs4 import BeautifulSoup
import requests
from Ready.Final_Reccomend import search,visualize_data 
import time
import matplotlib
matplotlib.use('Agg') 


app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Empty response with "No Content" status

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase3"
app.config["SECRET_KEY"] = "mysecret"
mongo = PyMongo(app)

# ------------------- AI Chatbot Initialization -------------------

def initialize_llm():
    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.3-70b-versatile"
    )
    return llm

def create_vector_db():
    loader = DirectoryLoader("info/", glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_db = FAISS.from_documents(texts, embeddings)
    vector_db.save_local("./faiss_index3")  # Save FAISS index

    print("✅ FAISS vector DB created and data saved.")

    return vector_db

def setup_qa_chain(vector_db, llm):
    """Set up the retrieval-based QA system using FAISS and LLM."""
    retriever = vector_db.as_retriever()

    prompt_template = """
    You are an AI assistant that provides **short and precise answers**.  

    **Rules:**  
    - Answer in **one or two sentences only**.  
    - only some details, explanations, or formatting.  
    - If no relevant context is found, use general knowledge to answer and give precise details.  

    **Context (if available):**  
    {context}  

    **User Question:**  
    {question}  

    **Short Answer:**  
    """


    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT, "document_variable_name": "context"}
    )
print("🟢 Initializing Chatbot...")

llm=initialize_llm()
db_path = "./faiss_index3"
if os.path.exists(db_path):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
else:
    vector_db = create_vector_db()

# Initialize QA chain
qa_chain = setup_qa_chain(vector_db, llm)
# ------------------- Flask Routes -------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        
        if action == "signup":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            contact = request.form["contact"]

            existing_user = mongo.db.users.find_one({"username": username})
            if existing_user:
                flash("Username already exists!", "danger")
                return redirect(url_for("index"))

            hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({
                "username": username, 
                "email": email, 
                "password": hashed_password, 
                "contact": contact
            })
            flash("Signup successful! Please login.", "success")
        
        elif action == "login":
            username = request.form["username"]
            password = request.form["password"]

            user = mongo.db.users.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                session["user_id"] = str(user["_id"])
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid username or password!", "danger")

    return render_template("index.html")
@app.route('/store_search', methods=['POST'])
def store_search():
    data = request.json
    search_query = data.get("query")

    if search_query:
        mongo.db.search_query.insert_one({"query": search_query})
        return jsonify({"message": "Search query saved!"}), 200
    else:
        return jsonify({"error": "Invalid query"}), 400
    
    
# @app.route("/dashboard", methods=["GET", "POST"])
# def dashboard():
#     if "user_id" not in session:
#         flash("Please login first!", "warning")
#         return redirect(url_for("index"))

#     products = []  # Initialize products to avoid UnboundLocalError

#     if request.method == "POST":
#         username = session.get("user_id")  # Get logged-in user
#         data = request.get_json()  # Get JSON data

#         search_data = data.get("search_data")  # Search input
#         # url = "http://127.0.0.1:5000/dashboard"
#         # data = requests.get(url)
        
#         # soup = BeautifulSoup(data.text,'html.parser')
#         # search_data = soup.find('input',{'id':'product-input'})
#         # print(search_data)
#         # # if not search_data:
#         # #     return jsonify({"error": "Missing search data"}), 400
        
#         search_obt_data = data.get("search_products")  # Obtained product results

#         if not search_obt_data:
#             return jsonify({"error": "Missing search results"}), 400

#         # Debugging: Log received data
#         print("Received search data:", search_data)
#         print("Received search products:", search_obt_data)

#         # Store in MongoDB
#         mongo.db.search_query.insert_one({
#             "username": username,
#             "search_data": search_data,
#             "search_obt_data": search_obt_data
#         })
#         s = mongo.db.search_query.find_one(
#     {"username": username},  # Filter by logged-in user
#     {"_id": 0, "search_data": 1},  # Return only search_data
# )

#         if s and "search_data" in s:
#             print(s["search_data"])
#             user_portal(s['search_data'])
        
#             try:
#                 df = pd.read_csv(s["search_data"]+'.csv')  # Load CSV file
#                 for i in range(df.shape[0]):  # Correct the iteration over range
#                     products.append(list(df.iloc[i]))
#                     print(products)
#             except FileNotFoundError:
#                 return jsonify({"error": "CSV file not found"}), 400
#             except Exception as e:
#                 return jsonify({"error": str(e)}), 500
#         else:
#             print("No search data found")  # This will print something like {'search_data': 'laptop'}



#         return jsonify({"message": "Search stored successfully!"}), 200

#     return render_template("dashboard.html", products=products)  # Now products is always defined

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Please login first!"}), 401

    products = []

    if request.method == "POST":
        data = request.get_json()
        if not data or "search_data" not in data:
            return jsonify({"error": "Missing search data"}), 400

        search_data = data["search_data"]
        username = session.get("user_id")

        # Store search data in MongoDB
        
        # mongo.db.search_query.insert_one({
        #     "username": username,
        #     "search_data": search_data
        # })

        # print(f"Search query '{search_data}' stored for user '{username}'.")
        user_portal(search_data)
        time.sleep(5)
        search(search_data)
        # Load product data from CSV
        # csv_filename = f"{search_data}_croma.csv"
        

        df = pd.read_csv(search_data+'_croma.csv')
        df2=pd.read_csv(search_data+'_vijay.csv')
        df3=pd.read_csv(search_data+'_poojara.csv')
        # df2["Rating"] = 'N/A'
        print('DF',df)
        print('DF2',df2)
        print('DF3',df3)
        products=pd.concat([df,df2,df3],ignore_index=True,axis=0)
        products=products.values.tolist()
        print(products)
        store_obj_data = [{"name": item[0], "price": item[1]} for item in products]
        # print('STOREE OBJECT DATA:::',store_obj_data)
        mongo.db.search_query.insert_one({
                "username": username,
                "search_data": search_data,
                "store_obj_data": store_obj_data
            })

        return jsonify({"message": "Search stored successfully!", "products": products}), 200

    return render_template('dashboard.html', products=products)


@app.route('/compare-products',methods=['GET','POST'])
def compare_products():
    return render_template('chart.html')
@app.route("/trending-deals")
def trending_deals():
    if "user_id" not in session:
        return jsonify({"error": "Please login first!"}), 401  # Ensure user is logged in
    
    username = session["user_id"]
    
    # Fetch last 5 search queries of the user
    user_searches = mongo.search_query.find({"username": username}).sort("_id", -1).limit(5)
    
    top_searches = [search["search_data"] for search in user_searches if "search_data" in search]
    
    print("User's Top 5 Search Queries:", top_searches)  # Print in console for debugging
    
    return render_template("trending_deals.html", top_searches=top_searches)



@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("index"))


@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_query = data.get("message", "")

    if not user_query:
        return jsonify({"reply": "Please enter a valid question."})
    response = qa_chain.run(user_query).replace("##", "").replace("*", "").replace("\n", " ")
    print(response)
    return jsonify({"reply": response})

# ------------------- Run Flask App -------------------
if __name__ == "__main__":
    app.run(port=7005,debug=True)
