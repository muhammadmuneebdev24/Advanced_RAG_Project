from source.llm import get_answer


def main():

    print("PDF Chatbot is ready!")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nAsk your question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = get_answer(question)

        print("\nAnswer:")
        print("--------------------")
        print(answer["answer"])

        print("\nSources:")

        seen = set()

        for source in answer["sources"]:

            # Unique key = PDF file + page number
            key = (source["source"], source["page"])

            if key in seen:
                continue

            seen.add(key)

            print(f"Heading : {source['heading']}")
            print(f"File  : {source['source']}")
            print(f"Page  : {source['page'] + 1}/{source['total_pages']}")
            print()


if __name__ == "__main__":
    main()

