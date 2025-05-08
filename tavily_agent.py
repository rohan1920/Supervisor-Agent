import os
from dotenv import load_dotenv
from tavily import TavilyClient


# Load environment variables
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in .env file")

# Initialize Tavily client
client = TavilyClient(api_key=tavily_api_key)

# Study tips for different education levels
STUDY_TIPS = {
    "piaic": "Focus on hands-on projects in AI, blockchain, or cloud computing. Join PIAIC forums, attend live sessions, and practice coding daily (e.g., Python, TensorFlow).",
    "matric": "Create a study schedule for Math, Science, and English. Use past papers, focus on weak areas, and practice problems daily. NCERT books are key!",
    "fsc": "Prioritize Physics, Chemistry, and Biology/Math. Solve numericals, use reference books (e.g., Punjab Textbook Board), and practice past papers for board exams.",
    "bs": "Balance coursework and projects. For CS/engineering, master programming (Python, Java) and use GitHub for projects. Attend university workshops and read research papers.",
    "mphil": "Focus on research methodology and thesis writing. Use tools like Zotero for references, read recent journal articles, and discuss ideas with your supervisor."
}

# Advanced AI agent function
def study_agent(query, education_level=None):
    try:
        
        # Detect education level from query or input
        query_lower = query.lower()
        if education_level is None:
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
            else:
                education_level = "general"

        # Perform a search with Tavily
        response = client.search(
            query=query,
            search_depth="basic",  # Can be changed to "advanced" for deeper searches
            max_results=5
        )
        results = response.get("results", [])
        
        # Format response
        answer = f"Study Assistant Response (as of {current_time}):\n"
        answer += f"Query: {query}\n"
        if education_level != "general":
            answer += f"Education Level: {education_level.upper()}\n"
        
        # Add study tips if applicable
        if education_level in STUDY_TIPS:
            answer += f"Study Tips: {STUDY_TIPS[education_level]}\n\n"
        
        # Add search results
        if not results:
            answer += f"No web results found for '{query}'."
        else:
            answer += "Web Resources:\n"
            for idx, result in enumerate(results, 1):
                answer += f"{idx}. {result['title']} ({result['url']}):\n   {result['content'][:200]}...\n"
        
        return answer
    except Exception as e:
        return f"Error during search: {str(e)}"

# Interactive loop for user input
if __name__ == "__main__":
    print("Welcome to the PIAIC & Academic Study Assistant!")
    print("Enter your study-related query (e.g., 'PIAIC AI course', 'Matric Math tips', 'MPhil thesis help'). Type 'exit' to quit.")
    while True:
        query = input("Your query: ")
        if query.lower() == "exit":
            break
        print(study_agent(query))
        print("\nEnter another query or type 'exit'.")