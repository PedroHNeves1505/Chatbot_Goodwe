from .vector_store import vector_store

def retrive_generator(k=4):
    store = vector_store()
    
    return store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )