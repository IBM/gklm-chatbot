from langchain_milvus import Milvus
from langchain_ibm import WatsonxEmbeddings, WatsonxLLM
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from langchain.chains import RetrievalQA

def main(params):

    try:
        # IBM Watsonx API Credentials (replace with your credentials)
        IBM_API_KEY = ""
        IBM_PROJECT_ID = ""
        IBM_WATSONX_URL = ""
        MILVUS_URI = ""

        urls = [
            "https://www.ibm.com/docs/en/gklm/4.2?topic=services-add-user-group-rest-service",
            "https://www.ibm.com/docs/en/gklm/4.2?topic=overview-license-usage-metrics",
            "https://www.ibm.com/docs/en/gklm/4.2?topic=overview-master-key-in-master-key-store"
        ]

        model_id = ModelTypes.GRANITE_13B_INSTRUCT_V2


        embeddings = WatsonxEmbeddings(
                    model_id="ibm/slate-30m-english-rtrvr",
                    url=IBM_WATSONX_URL,
                    apikey=IBM_API_KEY,
                    project_id=IBM_PROJECT_ID,
                ) 

        vector_store = Milvus(
            collection_name="rag_web_watsonx",
            embedding_function=embeddings,
            connection_args={"MILVUS_": MILVUS_URI},
            auto_id=True,
            drop_old=True,  # Drop the old Milvus collection if it exists
        )

        documents = []
        for url in urls:
            loader = WebBaseLoader(url)
            # loader = UnstructuredURLLoader(urls=[url])
            data = loader.load()
            documents += data

        doc_id = 0
        for doc in documents:
            doc.page_content = " ".join(doc.page_content.split()) # remove white space
            doc.metadata["id"] = doc_id #make a document id and add it to the document metadata
            doc_id += 1


        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)

        # Split the documents into chunks using the text_splitter
        docs = text_splitter.split_documents(documents)

        ids = vector_store.add_documents(docs, batch_size=200)

        parameters = {
            GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS: 100,
            GenParams.STOP_SEQUENCES: ["<|endoftext|>"]
        }

        watsonx_granite = WatsonxLLM(
            model_id=model_id.value,
            url=IBM_WATSONX_URL,
            apikey=IBM_API_KEY,
            project_id=IBM_PROJECT_ID,
            params=parameters
        )


        qa = RetrievalQA.from_chain_type(llm=watsonx_granite, chain_type="stuff", retriever=vector_store.as_retriever())
        query = params["query"]
        response = qa.invoke(query)

        print('response', response)

        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 200,
            "body": {
                'response': response['result']
            },
        }
    
    except Exception as e:
        print('e', e)
        print(f"Failed to execute the API {str(e)}")
