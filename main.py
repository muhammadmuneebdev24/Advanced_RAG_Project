from source.llm import get_answer
from source.retreiver import retrieve_chunks

def main():

    print("PDF Chatbot is ready!")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nAsk your question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # --------------------------------
        # DEBUG: Show retrieved chunks
        # --------------------------------
        results = retrieve_chunks(question)

        print("\n\n===== RETRIEVED CHUNKS =====")

        for i, (doc, score) in enumerate(results, 1):

            print("\n==============================")
            print(f"RESULT {i}")
            print(f"Score: {score}")
            print(f"Page: {doc.metadata.get('page')}")
            print(f"Title: {doc.metadata.get('chunk_title')}")
            print("==============================")

            print(doc.page_content[:1000])

        answer = get_answer(question)

        print("\nAnswer:")
        print("--------------------")
        print(answer["answer"])

        print("\nSources:")

        seen = set()

        for source in answer["sources"]:

            key = (source["source"], source["page"])

            if key in seen:
                continue

            seen.add(key)

            print(f"Title : {source['title']}")
            print(f"File  : {source['source']}")
            print(f"Page  : {source['page'] + 1}/{source['total_pages']}")
            print()
    

if __name__ == "__main__":
    main()

