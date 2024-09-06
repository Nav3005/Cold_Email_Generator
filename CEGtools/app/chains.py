import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
    ### SCRAPED TEXT FROM WEBSITE
    {page_data}
    #### Instruction
    the scraped text is from careers page of a website.
    your job is to extract necessary information relevant to job posting and return it in a JSON format container
    obtain the following keys : 'role','experience','skills' ans 'description'.
    ### Valid JSON (NO PREAMBLE)
    """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """   ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Raj, a senior business development executive at NexGen Solutions. NexGen Solutions is a leading AI & Software Consulting company focused on driving business innovation through advanced technology solutions. 
            With years of expertise, NexGen has helped numerous organizations streamline their processes, achieve scalability, and reduce operational costs. 
            Your task is to craft a cold email to the client based on the job description above, outlining how NexGen Solutions can meet their specific needs.
            Be sure to incorporate the most relevant case studies from the following links to highlight NexGen's portfolio: {link_list}
            Remember, you are Raj, Senior BDE at NexGen Solutions. 
            Avoid providing a preamble.
            ### EMAIL (NO PREAMBLE) """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))