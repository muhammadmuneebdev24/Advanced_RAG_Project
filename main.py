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
        print(answer)


#changing 
if __name__ == "__main__":
    main()