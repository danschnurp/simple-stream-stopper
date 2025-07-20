import os


from test_playground.tests import test_enhanced_algorithm, benchmark_algorithm

if __name__ == "__main__":
    test_enhanced_algorithm()
    print("\n" + "=" * 50 + "\n")
    benchmark_algorithm()

    if ".env" not in  os.listdir("./"):
        print("\n\n\n NOTE: \n"
              "for realistic streaming playground the .env file with huggingface token needs to be loaded... see: .env.example")
        exit(0)

    from test_playground.real_streaming_api import test_stopwords, advanced_test_stopwords, demo_comparison

    # Basic test
    print("=== BASIC STOP WORD FILTERING ===")
    test_stopwords()

    print("\n=== ADVANCED FILTERING ===")
    advanced_test_stopwords()

    print("\n=== COMPARISON DEMO ===")
    demo_comparison()