import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime

# Load environment variables
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in .env file")

# Initialize Tavily client
client = TavilyClient(api_key=tavily_api_key)

# Study tips for different education levels and subjects
STUDY_TIPS = {
    "piaic": {
        "ai": "Master Python and TensorFlow. Complete PIAIC assignments, build neural network projects, and explore Kaggle datasets.",
        "blockchain": "Learn Solidity and Ethereum. Practice smart contract development and study PIAIC’s blockchain syllabus.",
        "cloud": "Study AWS/GCP via PIAIC labs. Get certified (e.g., AWS Solutions Architect) and deploy a cloud project.",
        "general": "Focus on hands-on projects in AI, blockchain, or cloud computing. Join PIAIC forums and practice coding daily."
    },
    "matric": {
        "math": "Practice algebra and geometry daily. Use Matric past papers and NCERT exercises.",
        "science": "Focus on Physics/Chemistry concepts. Do experiments and memorize key formulas.",
        "english": "Improve grammar and essay writing. Read short stories and practice comprehension.",
        "general": "Create a study schedule for Math, Science, and English. Use past papers and NCERT books."
    },
    "fsc": {
        "physics": "Solve numericals and study concepts like mechanics. Use Punjab Textbook Board books.",
        "chemistry": "Memorize organic reactions and practice mole calculations. Use past papers.",
        "biology": "Study diagrams (e.g., human anatomy) and practice MCQs for board exams.",
        "math": "Focus on calculus and trigonometry. Solve F.Sc past papers.",
        "general": "Prioritize Physics, Chemistry, and Biology/Math. Solve numericals and practice past papers."
    },
    "bs": {
        "cs": "Master Python/Java, build projects on GitHub, and study algorithms (e.g., LeetCode).",
        "engineering": "Focus on core subjects (e.g., circuits for EE). Work on practical projects.",
        "general": "Balance coursework and projects. Attend university workshops and read research papers."
    },
    "mphil": {
        "research": "Learn research methodologies and statistical tools (e.g., SPSS). Read recent journals.",
        "thesis": "Use Zotero for references. Write clear objectives and discuss with your supervisor.",
        "general": "Focus on research methodology and thesis writing. Read journal articles."
    }
}

# Help menu
HELP_MENU = """
Study Assistant Help:
- Enter a query like 'PIAIC AI course', 'Matric Math tips', 'F.Sc Physics numericals', 'BS CS projects', or 'MPhil thesis help'.
- Specify education level (PIAIC, Matric, F.Sc, BS, MPhil) and subject (e.g., Math, AI) for tailored advice.
- Examples:
  - 'PIAIC blockchain syllabus'
  - 'Matric Science exam tips'
  - 'F.Sc Chemistry reactions'
  - 'BS Python programming'
  - 'MPhil research methods'
- Type 'help' to see this menu again.
- Type 'exit' to quit.
"""

# Advanced AI agent function
def study_agent(query):
    try:
        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle help command
        if query.lower() == "help":
            return HELP_MENU
        
        # Detect education level and subject
        query_lower = query.lower()
        education_level = "general"
        subject = "general"
        
        # Education level detection
        if "piaic" in query_lower:
            education_level = "piaic"
        elif "matric" in query_lower or "10th" in query_lower:
            education_level = "matric"
        elif "fsc" in query_lower or "intermediate" in query_lower or "12th" in query_lower:
            education_level = "fsc"
        elif "bs" in query_lower or "bachelor" in query_lower:
            education_level = "bs"
        elif "mphil" in query_lower or "master" in query_lower or "thesis" in query_lower:
            education_level = "mphil"
        
        # Subject detection
        if education_level == "piaic":
            if "ai" in query_lower:
                subject = "ai"
            elif "blockchain" in query_lower:
                subject = "blockchain"
            elif "cloud" in query_lower:
                subject = "cloud"
        elif education_level == "matric":
            if "math" in query_lower:
                subject = "math"
            elif "science" in query_lower:
                subject = "science"
            elif "english" in query_lower:
                subject = "english"
        elif education_level == "fsc":
            if "physics" in query_lower:
                subject = "physics"
            elif "chemistry" in query_lower:
                subject = "chemistry"
            elif "biology" in query_lower:
                subject = "biology"
            elif "math" in query_lower:
                subject = "math"
        elif education_level == "bs":
            if "cs" in query_lower or "computer science" in query_lower:
                subject = "cs"
            elif "engineering" in query_lower:
                subject = "engineering"
        elif education_level == "mphil":
            if "research" in query_lower:
                subject = "research"
            elif "thesis" in query_lower:
                subject = "thesis"
        
        # Perform a search with Tavily
        response = client.search(
            query=query,
            search_depth="advanced",  # Deeper search for better results
            max_results=5
        )
        results = response.get("results", [])
        
        # Format response
        answer = f"Study Assistant Response (as of {current_time}):\n"
        answer += f"Query: {query}\n"
        if education_level != "general":
            answer += f"Education Level: {education_level.upper()}\n"
        if subject != "general":
            answer += f"Subject: {subject.capitalize()}\n"
        
        # Add study tips
        tips = STUDY_TIPS.get(education_level, {}).get(subject, STUDY_TIPS.get(education_level, {}).get("general", ""))
        if tips:
            answer += f"Study Tips: {tips}\n\n"
        
        # Add search results
        if not results:
            answer += f"No web results found for '{query}'."
        else:
            answer += "Web Resources:\n"
            for idx, result in enumerate(results, 1):
                answer += f"{idx}. {result['title']} ({result['url']}):\n   {result['content'][:200]}...\n"
        
        # Save response to study_notes.txt
        with open("study_notes.txt", "a", encoding="utf-8") as f:
            f.write(f"[{current_time}] {answer}\n\n")
        
        return answer
    except Exception as e:
        return f"Error during search: {str(e)}"

# Interactive loop for user input
if __name__ == "__main__":
    print("Welcome to the PIAIC & Academic Study Assistant!")
    print(HELP_MENU)
    while True:
        query = input("Your query: ")
        if query.lower() == "exit":
            break
        print(study_agent(query))
        print("\nEnter another query, 'help', or 'exit'.")