from graph import app_graph

def main():
    print("\nDebales AI Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ")

        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        result = app_graph.invoke({
            "question": question,
            "route": "",
            "rag_context": "",
            "serp_context": "",
            "final_answer": ""
        })

        print("\nRoute Used:", result["route"])
        print("\nAssistant:")
        print(result["final_answer"])
        print("\n" + "-" * 70 + "\n")

if __name__ == "__main__":
    main()