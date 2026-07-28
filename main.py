from source.llm import get_answer


def main():

    print("PDF Chatbot is ready!")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nAsk your question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        result = get_answer(question)

        print("\nAnswer:")
        print("-" * 60)
        print(result["answer"])

        print("\nReferences:")
        print("-" * 60)

        for source in result["sources"]:

            print(f"Heading : {source['heading']}")
            print(f"Page    : {source['page'] + 1}")
            print()


if __name__ == "__main__":
    main()